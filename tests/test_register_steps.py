import pytest
from pytest_bdd import scenarios, given, when, then
from flask.testing import FlaskClient
from app import create_app

# Load the feature file
scenarios("../features/test_register.feature")

flask_app = create_app()


@pytest.fixture
def client():
    flask_app.testing = True
    with flask_app.test_client() as client:
        yield client


@given("the application is running")
def app_running():
    assert flask_app is not None


@given('a user is already registered with the username "existing_user"')
def register_existing_user(client: FlaskClient):
    response = client.post(
        "/register",
        data={"username": "existing_user", "password": "password123"},
    )
    assert response.status_code == 200
    assert b"Registration successful!" in response.data


@when("I submit valid registration details")
def submit_valid_registration(client: FlaskClient):
    response = client.post(
        "/register",
        data={"username": "new_user", "password": "new_password"},
    )
    pytest.response = response


@when('I submit registration details with the username "existing_user"')
def submit_existing_user_registration(client: FlaskClient):
    response = client.post(
        "/register",
        data={"username": "existing_user", "password": "password123"},
    )
    pytest.response = response


@then("I should see a registration success message")
def check_registration_success_message():
    assert pytest.response.status_code == 200
    assert b"Registration successful!" in pytest.response.data


@then("I should see an error message")
def check_registration_error_message():
    assert pytest.response.status_code == 200
    assert b"Username already exists" in pytest.response.data
