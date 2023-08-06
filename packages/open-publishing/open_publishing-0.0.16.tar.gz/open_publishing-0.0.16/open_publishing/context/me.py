"""
Abstraction for the 'me' object.

The 'me' object describe the current authentication state
of an authenticated session.
"""

class Me():
    """Class for me object."""

    def __init__(self, context):
        """Initialize 'me' object."""
        res = context.gjp.get_me()
        self._user_name = res['user_name']
        self._user_id = res['user_id']
        self._realm_name = res['realm_name']
        self._realm_id = res['realm_id']
        self._app_name = res['app_name']
        self._app_id = res['app_id']

    @property
    def user_name(self):
        """Return user name."""
        return self._user_name

    @property
    def user_id(self):
        """Return user id."""
        return self._user_id

    @property
    def user_guid(self):
        """Return user GUID."""
        return 'user.{0}'.format(self._user_id)

    @property
    def app_name(self):
        """Return app name."""
        return self._app_name

    @property
    def app_id(self):
        """Return app id."""
        return self._app_id
    @property
    def realm_name(self):
        """Return realm name."""
        return self._realm_name

    @property
    def realm_id(self):
        """Return realm id."""
        return self._realm_id
