import sys

import pytest
from pytest_bdd import scenarios, given, when, then
from flask import Flask
from flask.testing import FlaskClient
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Adjust the path to your app module if necessary
from app import create_app


# Load the feature file
scenarios("../features/test_login.feature")

flask_app = create_app()


@pytest.fixture
def client():
    flask_app.testing = True
    with flask_app.test_client() as client:
        yield client


@given("the application is running")
def app_running():
    assert flask_app is not None


@given("a user is registered with valid credentials")
def register_user(client: FlaskClient):
    response = client.post(
        "/register",
        data={"username": "valid_user", "password": "valid_pass"},
    )
    assert response.status_code == 200
    assert b"Registration successful!" in response.data


@when("I submit valid login credentials")
def submit_valid_login(client: FlaskClient):
    response = client.post(
        "/login", data={"username": "valid_user", "password": "valid_pass"}
    )
    pytest.response = response


@when("I submit invalid login credentials")
def submit_invalid_login(client: FlaskClient):
    response = client.post(
        "/login", data={"username": "invalid_user", "password": "wrong_pass"}
    )
    pytest.response = response


@then("I should see a success message")
def check_success_message():
    assert pytest.response.status_code == 200
    assert b"Login Successful!" in pytest.response.data


@then("I should see an error message")
def check_error_message():
    assert pytest.response.status_code == 200
    assert b"Invalid username or password." in pytest.response.data
