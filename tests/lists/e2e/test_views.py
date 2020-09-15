import json


def test_list_create_view(test_client, api_test_user):
    # given ... a list name
    list_data = {
        'name': 'Wedding lists'
    }

    # given ... a valid API token in request header
    token_key = api_test_user.tokens[0].key
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token_key}'
    }

    # when ... an user attempt to create a gift list
    response = test_client.post(
        '/api/lists/',
        data=json.dumps(list_data),
        headers=headers
    )

    # then ... API endpoint should return 201 along with new list data
    new_list_data = response.get_json()
    assert response.status_code == 201
    assert new_list_data['name'] == list_data['name']
