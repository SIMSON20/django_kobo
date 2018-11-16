"""
ArcGIS Portal OAuth2 backend
"""
from social_core.backends.oauth import BaseOAuth2
from decouple import config

class PortalOAuth2(BaseOAuth2):
    name = 'portal'
    ID_KEY = 'username'
    AUTHORIZATION_URL = config('PORTAL_URL') + '/sharing/rest/oauth2/authorize'
    ACCESS_TOKEN_URL = config('PORTAL_URL') +'/sharing/rest/oauth2/token'
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('expires_in', 'expires_in')
    ]

    def get_user_details(self, response):
        """Return user details from ARCGIS Portal account"""
        return {'username': response.get('username'),
                'email': response.get('email'),
                'fullname': response.get('fullName'),
                'first_name': response.get('firstName'),
                'last_name': response.get('lastName')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json(
            config('PORTAL_URL') +'/sharing/rest/community/self',
            params={
                'token': access_token,
                'f': 'json'
            }
        )
