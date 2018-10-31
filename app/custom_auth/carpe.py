"""
CAPPE GIS Portal OAuth2 backend
"""
from social_core.backends.oauth import BaseOAuth2


class CARPEOAuth2(BaseOAuth2):
    name = 'carpe'
    ID_KEY = 'username'
    AUTHORIZATION_URL = 'https://gis.forest-atlas.org/portal/sharing/rest/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://gis.forest-atlas.org/portal/sharing/rest/oauth2/token'
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('expires_in', 'expires_in')
    ]

    def get_user_details(self, response):
        """Return user details from CARPE GIS Portal account"""
        return {'username': response.get('username'),
                'email': response.get('email'),
                'fullname': response.get('fullName'),
                'first_name': response.get('firstName'),
                'last_name': response.get('lastName')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json(
            'https://gis.forest-atlas.org/portal/sharing/rest/community/self',
            params={
                'token': access_token,
                'f': 'json'
            }
        )
