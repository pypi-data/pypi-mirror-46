"""
@file
@brief Authentification part.
"""
import base64
import falcon
from ..args import encrypt_password, load_passwords


class AuthMiddleware:
    """
    Authentification. The name and secret comes from
    a file. The file must store encrypted password.
    """

    help_url = "http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/tutorial/first_rest_api.html"

    def __init__(self, source, algo="sha224"):
        """
        @param      source      filename or dataframe for encrypted password
        @param      algo        algorithm used to hash the passwords
        """
        if source is None:
            raise ValueError("source cannot be empty")
        self.allowed = load_passwords(source)
        self.algo = algo
        self.auth_header_prefix = 'Basic'

    def parse_auth_token_from_request(self, auth_header):
        """
        Parses and returns Auth token from the request header. Raises
        `falcon.HTTPUnauthoried exception` with proper error message
        """

        if not auth_header:
            raise falcon.HTTPUnauthorized(
                title='401 Unauthorized', description='Missing Authorization Header')

        parts = auth_header.split()

        if parts[0].lower() != self.auth_header_prefix.lower():
            raise falcon.HTTPUnauthorized(title='401 Unauthorized',
                                          description='Invalid Authorization Header: '
                                          'Must start with {0}'.format(self.auth_header_prefix))

        if len(parts) == 1:
            raise falcon.HTTPUnauthorized(
                title='401 Unauthorized',
                description='Invalid Authorization Header: Token Missing')
        if len(parts) > 2:
            raise falcon.HTTPUnauthorized(
                title='401 Unauthorized',
                description='Invalid Authorization Header: Contains extra content')

        return parts[1]

    def process_request(self, req, resp):
        """
        Processes an authentification request.

        @param  req     request
        @param  resp    unused
        """
        if req.scheme.lower() != 'https':
            raise falcon.HTTPBadRequest(title='HTTPS Required',
                                        description=('All requests must be performed via the HTTPS protocol. '
                                                     'Please switch to HTTPS and try again.'))

        auth = req.get_header('Authorization')
        token = self.parse_auth_token_from_request(auth_header=auth)
        try:
            token = base64.b64decode(token).decode('utf-8')
        except Exception:
            raise falcon.HTTPUnauthorized(title='401 Unauthorized',
                                          description='Invalid Authorization Header: Unable to decode credentials (1)')

        try:
            username, password = token.split(':', 1)
        except ValueError:
            raise falcon.HTTPUnauthorized(
                title='401 Unauthorized',
                description='Invalid Authorization: Unable to decode credentials (2)')

        if not self._token_is_valid(username, password):
            raise falcon.HTTPUnauthorized(
                "Authentication failed for '{0}'".format(username))

    def _token_is_valid(self, username, password):
        """
        Decides if it is valid or not.
        """
        if username not in self.allowed:
            return False
        enc = encrypt_password(password, algo=self.algo)
        return self.allowed[username] == enc
