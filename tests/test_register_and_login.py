import os

import redis
import requests


def test_register_and_login():
    test_data = {"email": "test@test.com", "password": "pa55word"}

    response = requests.post("http://0.0.0.0:5000/login/", data=test_data)
    assert response.status_code == 400

    response = requests.post("http://0.0.0.0:5000/register/", data=test_data)
    assert response.status_code == 200

    response = requests.post("http://0.0.0.0:5000/login/", data=test_data)
    assert response.status_code == 200

    response = requests.post("http://0.0.0.0:5000/logout/", data=test_data)
    assert response.status_code == 200
