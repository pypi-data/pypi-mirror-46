"""Module for handling authentication"""
import requests

class AuthException(Exception):
    """AuthException class."""

    def __init__(self, msg, **kwargs):
        """Initialize AuthException class."""
        super().__init__(msg)
        self.kwargs = kwargs


class AuthFailedException(Exception):
    """AuthFailedException class."""
    pass


class AuthContext:
    """AuthContext class."""
    def __init__(self, api_host):
        """Initialize AuthContext class."""
        self.api_host = api_host
        self.auth_token = None
        self.authenticated = False
        self.last_credentials = None

    def auth(self, **kwargs):
        """
        Authenticate with various options.
              email, password, realm_id           : authenticate as user
              api_key                             : authenticate with api_key obtained in admin area
              app_id or app_name, app_secret      : authenticate with app_secret as app. App secrets
                                                    are shared as docker secrets.
              realm_id                            : authenticate as world.
        """
        self.auth_token = None
        self.authenticated = False
        self.last_credentials = kwargs
        if 'email' in kwargs and 'password' in kwargs and 'realm_id' in kwargs:
            self._auth_user(email=kwargs['email'], password=kwargs['password'], realm_id=kwargs['realm_id'])
        elif 'api_key' in kwargs:
            self._auth_api_key(api_key=kwargs['api_key'])
        elif ('app_id' in kwargs or 'app_name' in kwargs) and 'app_secret' in kwargs:
            self._auth_app(app_secret=kwargs['app_secret'], app_id=kwargs.get('app_id', None), app_name=kwargs.get('app_name', None))
        elif 'realm_id' in kwargs:
            self._auth_world(realm_id=kwargs['realm_id'])
        else:
            raise Exception("no valid auth parameters")

    def _auth_world(self, realm_id):
        """Authenticate as world. No credentials/token needed."""
        req = requests.post(
            self._auth_url(),
            data={
                'type': 'world',
                'realm_id': realm_id},
            timeout=5)
        self._evaluate_response(req)

    def _auth_user(self, email, password, realm_id):
        """Authenticate with user credentials."""
        req = requests.post(
            self._auth_url(),
            data={
                'type': 'user',
                'realm_id': realm_id,
                'email': email,
                'password': password},
            timeout=5)
        self._evaluate_response(req)

    def _auth_app(self, app_secret, app_id=None, app_name=None):
        """Authenticate with user credentials."""
        if app_id is not None and app_name is not None:
            raise ValuerError('Only app_id or app_name should be set')
        data = {
            'type': 'app',
            'app_secret': app_secret
        }
        if app_id is not None:
            data['app_id'] = app_id
        if app_name is not None:
            data['app_name'] = app_name

        req = requests.post(
            self._auth_url(),
            data=data,
            timeout=5)
        self._evaluate_response(req)

    def _auth_api_key(self, api_key):
        """Authenticate as with api_key."""
        req = requests.post(
            self._auth_url(),
            data={
                'type': 'api_key',
                'api_key': api_key},
            timeout=5)
        self._evaluate_response(req)

    def _evaluate_response(self, req):
        """Evaluating response from auth server and setting internal api_key."""
        if req.status_code == 403:
            raise AuthFailedException()

        if req.status_code != 200:
            self.authenticated = False
            raise AuthException('Could not authenticate, incorrect status_code', status_code=req.status_code)

        req_json = req.json()
        if 'ERROR' in req_json:
            self.authenticated = False
            raise AuthException('Could not authenticate', error=req_json['ERROR'])

        if 'auth_token' not in req_json:
            self.authenticated = False
            raise AuthException('Could not authenticate, no auth_token in req_son', req_json=req_json)

        self.auth_token = req_json['auth_token']
        self.authenticated = True

    def _auth_url(self):
        """Return API url."""
        return self.api_host + '/auth/auth'
