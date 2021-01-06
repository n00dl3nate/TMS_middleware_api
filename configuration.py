class Conf:

    def __init__(self):

        self.authentication={'client_id': 'tellme',\
                             'client_secret': 'l5rdyzzsiizq519bvmfrd6k11tn68s2v6mtiabfplvhzah',
                             'user': 'dimitrios.michelakis@improvementservice.org.uk',
                             'pass': 'papaki1981',\
                             'scope': ['tellme']}
        self.root_urls = {'token_url': 'https://www.tellmescotland.gov.uk/oauth2/token',
                          'api_url': 'https://www.tellmescotland.gov.uk/api/v1/'}

        self.request_urls = {'notices': self.root_urls['api_url']+'notices.json?limit=100000',
                             'organisations': self.root_urls['api_url']+'organisations.json',
                             'notices_types': self.root_urls['api_url']+'notice_types.json',}

        self.url_parameters = {'notices':[':id', 'offset', 'limit', 'archived', 'from', 'to', 'orid', 'ntid'],
                               'organisations':[':id', 'offset', 'limit'],
                               'notice_types':[':id', 'offset', 'limit']}


        self.files = {'download_log': 'download_data.log'}