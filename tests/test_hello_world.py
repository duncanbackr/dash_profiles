from flask import url_for


def test_hello_world(client):
    response = client.get(url_for('hello.world'))
    assert response.status_code == 200
    assert response.data == b'Hello, World!'
