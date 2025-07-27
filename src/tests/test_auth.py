def test_register(auth):
    response = auth.register()

    assert response.json["redirect"] == "/"


def test_register_twice(auth):
    auth.register()
    response = auth.register("test", "hunter2")

    assert response.status_code == 500


def test_not_logged_in(client):
    response = client.get("/me")
    assert response.json["logged_in"] == False


def test_logged_in(client, auth):
    auth.register()

    response = client.get("/me")
    assert response.json["logged_in"] == True
    assert response.json["username"] == "test"


def test_double_register(client, auth):
    assert auth.register().status_code == 200
    assert auth.register("test2", "password").status_code == 200

    response = client.get("/me")
    assert response.status_code == 200
    assert response.json["username"] == "test2"
