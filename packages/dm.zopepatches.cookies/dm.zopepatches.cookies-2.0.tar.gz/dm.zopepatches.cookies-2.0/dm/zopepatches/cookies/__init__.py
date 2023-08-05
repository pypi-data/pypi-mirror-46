"""Patches for Zope's cookie handling."""
from email.header import Header
from logging import getLogger
from re import compile

logger = getLogger('dm.zopepatches.cookies')


class Rfc2047(Header, object):
  def __init__(self, s, charset="utf-8"):
    super(Rfc2047, self).__init__(s, charset, 10000)


_parameter_registry = {}

def register_cookie_param(name, type='string', pname=None):
  name = name.lower()
  if pname is None: pname = name.replace('_','-')
  pname = pname.lower()
  type_registry[type] # ensure, "type" is known
  spec = (pname, type)
  kspec = _parameter_registry.get(name)
  if not (kspec is None or spec == kspec):
    raise ValueError('Inkompatible definition for cookie parameter %s: %s, %s'
                     % (name, spec, kspec)
                     )
  _parameter_registry[name] = spec


def string_param(name, value):
  value = _stringify(value)
  quote = False
  for c in value:
    if c.isspace() or c==',' or c==';': quote = True; break
  return "%s=%s" % (name, quote and '"%s"' % value or value)

def quoted_string_param(name, value):
  value = _stringify(value)
  return '%s="%s"' % (name, value)

def boolean_param(name, value):
  return value and name or ''

def sequence_param(name, value):
  return '%s="%s"' % (name, ','.join(map(_stringify, value)))


_rfc6265_safe = compile(r"\A[\x20-\x3A\x3C-\x7E]*\Z").match

def _stringify(value):
  """convert to a "native" string -- maybe `RFC2047` encoded.
  """
  if unicode is None:
    # Py 3
    if isinstance(value, bytes):
      raise TypeError("`bytes` cookie attribute values not supported")
    value = str(value)
    return value if _rfc6265_safe(value) else Rfc2047(value).encode()
  else:
    # Py 2
    if isinstance(value, unicode):
      # Py2's `email.header.Header`'s `encode` seems to do nothing for unicode
      return str(value) if _rfc6265_safe(value) else Rfc2047(value.encode("utf-8")).encode()
    value = str(value)
    if _rfc6265_safe(value): return value
    raise ValueError(
      "`%r` contains characters not allowed by RFC 6265 in cookie attribute values."
      "Please either use RFC 2047 encoding or convert to unicode."
      % value)


type_registry = dict(
  (type, globals()[type.replace('-', '_') + '_param'])
  for type in ('string', 'quoted-string', 'boolean', 'sequence')
  )


def _cookie_list(self):
  cl = self._dm_ori_cookie_list()
  for i, params in enumerate(self.cookies.values()): _process(params, cl, i)
  return cl


def _process(params, cookie_list, index):
  # Zope treats parameters case insensitive -- emulate
  params = dict((pn.lower(), pv) for (pn, pv) in params.items())
  # find parameters we may handle
  handle = set(p for p in params if p in _parameter_registry)
  if handle:
    # remove parameters that Zope meanwhile can handle itself
    ci = cookie_list[index]
    cookie_info = ci[1]
    for cp in _find_params(cookie_info):
      for p in handle:
        if _parameter_registry[p][0] == cp: handle.remove(p); break
    if handle:
      # process the remaining parameters
      add_info = []
      for p in handle:
        pn, tn = _parameter_registry[p]
        add_info.append(type_registry[tn](pn, params[p]))
      add_info = '; '.join(filter(None, add_info))
      if add_info:
        cookie_list[index] = ci[0], ci[1] + '; ' + add_info

def _find_unquoted_sc(s, i):
  """the index of the next unquoted semicolon in *s* following *i* or -1."""
  while True:
    next_sc = s.find(';', i)
    if next_sc < 0: return -1
    quote_start = s.find('"', i)
    if quote_start < 0 or next_sc < quote_start: return next_sc
    i = s.find('"', quote_start + 1) + 1
    if i == 0: return -1 # should not happen

def _find_params(cookie):
  """generate the parameters found in *cookie* definition."""
  i = 0; n = len(cookie)
  while i < n:
    param_start = _find_unquoted_sc(cookie, i) + 1
    if param_start <= 0: return
    param_end = _find_unquoted_sc(cookie, param_start)
    if param_end <= 0: param_end = n
    param = cookie[param_start:param_end]
    yield param.split('=', 1)[0].strip().lower()
    i = param_end

# patch HTTPResponse
from ZPublisher.HTTPResponse import HTTPResponse

HTTPResponse._dm_ori_cookie_list = HTTPResponse._cookie_list
HTTPResponse._cookie_list = _cookie_list

logger.info("HTTPResponse._cookie_list patched.")


# Python 2/3 compatibility
try: unicode
except NameError: unicode = None
