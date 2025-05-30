Feature: User Registration
  As a new user
  I want to register an account
  So that I can log in to the application

  Scenario: Successful registration
    Given the application is running
    When I submit valid registration details
    Then I should see a registration success message

  Scenario: Registration with an existing username
    Given the application is running
    And a user is already registered with the username "existing_user"
    When I submit registration details with the username "existing_user"
    Then I should see an error message
