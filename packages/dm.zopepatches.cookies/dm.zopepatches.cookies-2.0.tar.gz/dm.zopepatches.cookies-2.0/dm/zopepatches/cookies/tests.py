from unittest import TestCase, skipIf

from ZPublisher.HTTPResponse import HTTPResponse

from . import httponly, rfc2965 # activate extensions
from . import _find_unquoted_sc, _find_params, _process, \
     string_param, quoted_string_param, boolean_param, sequence_param

class Tests(TestCase):
  def test_patching(self):
    r = HTTPResponse()
    # Note: Zope 2.12 will support "http_only" instead
    r.setCookie('c', 'cv', httponly=True)
    self.assertEqual(r._cookie_list(), [('Set-Cookie', 'c="cv"; httponly')])
    r.setCookie('c', 'cv', httponly=False)
    self.assertEqual(r._cookie_list(), [('Set-Cookie', 'c="cv"')])

  def test_case_normalization(self):
    r = HTTPResponse()
    r.setCookie('c', 'cv', hTtPoNlY=True)
    self.assertEqual(r._cookie_list(), [('Set-Cookie', 'c="cv"; httponly')])
    
  def test_find_unquoted_sc(self):
    s = 'c="cv; ux"; P1; P2=2'
    i = _find_unquoted_sc(s, 0)
    self.assertEqual(i, 10)
    i = _find_unquoted_sc(s, 11)
    self.assertEqual(i, 14)
    i = _find_unquoted_sc(s, 15)
    self.assertEqual(i, -1)

  def test_find_params(self):
    s = 'c="cv; ux"; P1; P2=2'
    self.assertEqual(list(_find_params(s)), ['p1', 'p2'])

  def test_dont_touch_handled(self):
    s = 'c="cv"; HttpOnly=x'
    cl = [("Set-Cookie", cv) for cv in ['', s]]
    _process(dict(httponly=True), cl, 0)
    _process(dict(httponly=True), cl, 1)
    self.assertEqual(cl[0][1], '; httponly')
    self.assertEqual(cl[1][1], s)

  def test_types(self):
    self.assertEqual(string_param('n', 'a'), 'n=a')
    self.assertEqual(string_param('n', 'a b'), 'n="a b"')
    self.assertEqual(string_param('n', 'a,b'), 'n="a,b"')
    # with RFC 6265, inclusion into double quotes no longer quotes ";"
    #  RFC 2047 quoting is now required
    #self.assertEqual(string_param('n', 'a;b'), 'n="a;b"')
    self.assertEqual(quoted_string_param('n', 'a'), 'n="a"')
    self.assertEqual(boolean_param('n', True), 'n')
    self.assertEqual(boolean_param('n', False), '')
    self.assertEqual(sequence_param('n', (1,2,3)), 'n="1,2,3"')

  def test_rfc6265(self):
    self.assertEqual(string_param("n", u";"), "n==?utf-8?q?=3B?=")
    self.assertEqual(string_param("n", u"=?utf-8?B?Ow==?="), "n==?utf-8?B?Ow==?=")
    if unicode is not None: # Py2
      with self.assertRaises(ValueError): string_param("n", ";")
      with self.assertRaises(ValueError): string_param("n", "\n")



# Python 2/3 compatibility
try: unicode
except NameError: unicode = None # Python 3

@skipIf(unicode is not None, "Python 3 only")
class Py3Tests(TestCase):
  def test_bytes(self):
    with self.assertRaises(TypeError): string_param("n", b"")
