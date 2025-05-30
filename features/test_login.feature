Feature: User Login
  As a user
  I want to log in to the application
  So that I can access my account

  Scenario: Successful login
    Given the application is running
    And a user is registered with valid credentials
    When I submit valid login credentials
    Then I should see a success message

  Scenario: Invalid login password
    Given the application is running
    And a user is registered with valid credentials
    When I submit invalid login password
    Then I should see an error message

  Scenario: Invalid login
    Given the application is running
    When I submit invalid login credentials
    Then I should see an error message
