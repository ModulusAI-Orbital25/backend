def test_current_profile(client, auth):
    auth.register()

    response = client.get("/profile", follow_redirects=True)

    assert response.status_code == 200
    assert response.json["name"] == "test"


def test_other_profile(client, auth):
    assert auth.register().status_code == 200
    assert auth.register("test2", "password").status_code == 200

    response = client.get("/profile/1", follow_redirects=True)
    assert response.status_code == 200
    assert response.json["name"] == "test"
