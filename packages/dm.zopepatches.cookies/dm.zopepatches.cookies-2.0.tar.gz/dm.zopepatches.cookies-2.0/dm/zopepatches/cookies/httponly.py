"""support httponly parameter."""

from dm.zopepatches.cookies import register_cookie_param

register_cookie_param('httponly', 'boolean')
# name used by Zope 2.12
register_cookie_param('http_only', 'boolean', 'httponly')

