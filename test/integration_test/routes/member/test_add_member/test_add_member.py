import json
import test.integration_test.utils as utils
from test.test_fixtures.fixtures import Fixtures

import requests

MEMBER_RESOURCE = "member"
ADD_MEMBER_URL = utils.get_api_url(resource=MEMBER_RESOURCE, route="addMember")
DELETE_MEMBER_URL = utils.get_api_url(resource=MEMBER_RESOURCE, route="deleteMember")
GET_ALL_MEMBERS_URL = utils.get_api_url(resource=MEMBER_RESOURCE, route="getAllMembers")
GET_MEMBERS_BY_TEAM_URL = utils.get_api_url(resource=MEMBER_RESOURCE, route="getMembersByTeam")
UPDATE_MEMBER_URL = utils.get_api_url(resource=MEMBER_RESOURCE, route="updateMember")


def test_member():

    # Add member
    member = json.dumps({"Member": Fixtures.get_member_no_id()})
    add_member_response = requests.post(ADD_MEMBER_URL, data=member)
    expected_member = json.dumps({"message": Fixtures.get_member_no_id()})
    assert add_member_response.status_code == 200
    response_member = json.loads(add_member_response.content)
    del response_member["message"]["id"]
    assert response_member == json.loads(expected_member)

    # Check members
    all_members_response = requests.get(GET_ALL_MEMBERS_URL)
    assert all_members_response.status_code == 200
    expected_all_members_response = {
        "message": [json.loads(add_member_response.content)["message"]]
    }
    assert json.loads(all_members_response.content) == expected_all_members_response

    # Update member
    member_id = json.loads(add_member_response.content)["message"]["id"]
    expected_member_details = Fixtures.get_player_json(member_id, 1)
    updated_member_response = requests.patch(
        UPDATE_MEMBER_URL, data=json.dumps({"Member": expected_member_details})
    )
    assert updated_member_response.status_code == 200
    assert json.loads(updated_member_response.content) == {"message": expected_member_details}

    # Check members
    all_members_response = requests.get(GET_ALL_MEMBERS_URL)
    assert all_members_response.status_code == 200
    expected_member = json.loads(add_member_response.content)["message"]
    expected_member["player"]["season_appearances"] = 1
    expected_all_members_response = {"message": [expected_member]}
    assert json.loads(all_members_response.content) == expected_all_members_response

    # Delete member
    delete_member_response = requests.delete(
        DELETE_MEMBER_URL, data=json.dumps({"MemberId": member_id})
    )
    assert delete_member_response.status_code == 200
    assert json.loads(delete_member_response.content) == {
        "message": f"Successfully deleted Member with id: {member_id}"
    }

    # Check members
    all_members_response = requests.get(GET_ALL_MEMBERS_URL)
    assert all_members_response.status_code == 200
    expected_all_members_response = {"message": []}
    assert json.loads(all_members_response.content) == expected_all_members_response
