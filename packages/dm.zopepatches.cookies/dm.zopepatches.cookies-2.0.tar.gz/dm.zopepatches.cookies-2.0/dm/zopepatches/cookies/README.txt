This package patches the web application server Zope to improve its
cookie handling.

Currently, it defines ``register_cookie_param(`` *name*, *type*  ``='string'``, *pname*  ``=None)``
to define additional parameters recognized when cookies are generated.
*name* is the parameter given to Zope's ``setCookie`` method, *pname*
is the corresponding parameter name in the generated ``Set-Cookie`` response header.
If not specified, *pname* is derived from *name* by replacing ``_`` by ``-``.
*type* specifies this parameter's type. Currently defined values are
``'string'`` (normal string, quoted when it contains whitespace, comma or
semicolon), ``'quoted-string'`` (a string unconditionally quoted),
``'boolean'`` (boolean parameter, only the name and no value is generated), ``sequence`` (generates a quoted comma separated sequence).

**ATTENTION** `RFC 6265`__ has drastically simplified the ``Set-Cookie`` syntax
(over the now obsolete `RFC 2965`__):
it is no longer possible to quote ``;`` by
including it in a doubly quoted string. This means that ``;`` can no
longer be part of a cookie attribute value
(unless `RFC 2047`__ encoded).

__ https://tools.ietf.org/html/rfc6265#page-17
__ https://tools.ietf.org/html/rfc2965
__ https://tools.ietf.org/html/rfc2047


Import of ``dm.zopepatches.cookies.httponly`` provides for ``httponly``
support. It registers both ``httponly`` as well as ``http_only``.
The former is the spelling consistent with other cookie parameters, the
latter is the spelling used by Zope 2.12.


History
=======

2.0

  Made compatible with Python 3 and Zope [4].

  Made compatible with RFC 6025
