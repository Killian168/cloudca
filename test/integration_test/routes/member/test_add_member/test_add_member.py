from test.test_fixtures.fixtures import Fixtures

import requests

MEMBER_RESOURCE = "member"


def test_add_member(get_api_url):
    url = get_api_url(resource=MEMBER_RESOURCE, route="addMember")
    member = Fixtures.get_member_no_id()

    response = requests.post(url, data=member)

    print(response)
