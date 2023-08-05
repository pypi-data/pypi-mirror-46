"""RFC 2965 parameters.

Note: RFC 2965 specifies that 'Set-Cookie2' must be used to support
this type of cookies. While this module defines the cookie parameters,
it does not change the set cookie response header.
Therefore, these parameters may not be recognized by the browser.
"""

from dm.zopepatches.cookies import register_cookie_param

register_cookie_param("comment")
register_cookie_param("commenturl", 'quoted-string')
register_cookie_param("discard", 'boolean')
register_cookie_param("port", 'sequence')
register_cookie_param("version")

