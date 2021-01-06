from tms.service import *
from tms.base import Configuration
import json
import pprint

def main():

    c = Configuration()
    client = SetUp()
    token = client.get_token()
    header = client.create_header()
    rest = RestRequests(token, header)

    # Get all notices
    url = c.get_configuration_for('service', 'notices')
    data = rest.get(url)
    print(data)


    # Get all organisations
    url = c.get_configuration_for('service', 'organisations')
    data = rest.get(url)
    print(data)

    # Get all notice types
    url = c.get_configuration_for('service', 'notice_types')
    data = rest.get(url)
    print(data)


if __name__ == "__main__":
    main()
