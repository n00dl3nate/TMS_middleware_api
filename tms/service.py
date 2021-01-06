import sys
sys.path.insert(0, '../')

from tms.base import Configuration
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
import requests
import json
import ast

class SetUp(Configuration):
    """
    This class supports setting up the client before requesting data from the TMS REST API. This includes acquiring a
    token to assist with OAuth2 authentication and creating the header which is necessary to be used for any REST API
    request.
    """

    def __init__(self):
        Configuration.__init__(self)

        self.token_url = self.get_configuration_for('service', 'token_url')
        self.username = self.get_configuration_for('service', 'username')
        self.password = self.get_configuration_for('service', 'password')
        self.client_id = self.get_configuration_for('service', 'client_id')
        self.client_secret = self.get_configuration_for('service', 'client_secret')
        self.scope = ast.literal_eval(self.get_configuration_for('service', 'scope'))
        self.api_url = self.get_configuration_for('service', 'api_url')

    def get_token(self):
        """(None) -> str
        This REST API is using OAuth2 for authentication. Multiple OAuth2 authentication flows are supported. The quickest
        flow supported is the "Resource Owner Password Credentials Grant flow". To authentication using OAuth2 in Python
        this method is using the modules "oauthlib" and "requests_oauthlib" which need to be installed prior using this
        method. In order to authenticate with this oauth2 flow you need the following information:
        Resource Owner Name, Resource Owner Password, Client Identification, Client Secret, Access Token URI, and Scope.
        >>>get_token()
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        """

        self.oauth = OAuth2Session(client=LegacyApplicationClient(client_id=self.client_id))
        self.data = self.oauth.fetch_token(
            token_url=self.token_url,
            username=self.username,
            password=self.password,
            client_id=self.client_id,
            client_secret=self.client_secret)

        self.token = str(self.data[u'access_token'])
        return self.token

    def create_header(self,token):
        """(None) -> dict
        Returns a dictionary which includes the data needed for making a request to the TMS REST API using requests.
        In the example provided below the 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' represents the token.
        >>>create_header()
        {'Authorization': 'Bearer xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}
        """

        self.header  = {'Authorization': 'Bearer %s' % (token)}
        return self.header


class RestRequests(Configuration):

    def __init__(self, headers):

        Configuration.__init__(self)
        self.headers = headers

    def get(self, url):
        r = requests.get(url, headers=self.headers)
        return {'data': json.loads(r.content),
                'status_code': r.status_code}
        # if r.status_code == 200:
        #     return {'data':json.loads(r.content),
        #             'status_code':r.status_code}
        # else:
        #     return r
