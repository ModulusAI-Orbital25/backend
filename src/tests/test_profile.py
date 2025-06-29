def test_register(client):
    response = client.post(
        "/profile/register",
        json={
            "username": "test",
            "password": "testpassword",
        },
    )

    assert response.json["redirect"] == "/"
