


def test_get_all_post(authorized_client):
    """
    Test that we can get all posts
    """
    response = authorized_client.get('/sqlalchemy')
    print(response.json)
    assert response.status_code == 200

