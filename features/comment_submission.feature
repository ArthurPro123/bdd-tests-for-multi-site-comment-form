
Feature: Comment Form Submission on Multiple Sites

  As a tester
  I want to validate comment form behavior across multiple websites
  So that the form works consistently across all implementations

  Background:
    Given I have access to comment forms on all configured sites



  @smoke
  Scenario Outline: Submit form with all required fields filled successfully on <site>

    When I navigate to the comment form on "<site>"
    And I fill in the comment form with:
      | field     | value                                         |
      | username  | Test Username Comm                            |
      | content   | This is a test comment from an automated test |

    And I submit the form
    Then I should see success message "Your comment has been posted"

    Examples:
      | site     |
      | snatches |
      | services |
      | f-guitar |



  @smoke
  Scenario Outline: Submit empty comment form shows validation errors on <site>

    When I navigate to the comment form on "<site>"
    And I submit the empty form
    Then I should see an error message displayed
		And I should see the following validation errors:
		| field                | error                                      |
		| Your Alias or Name   | Your Alias or Name                         |
		| Comments             | Comments                                   |
		| Submission Challenge | Submission Challenge                       |

    Examples:
      | site     |
      | snatches |
      | services |
      | f-guitar |



  @regression
  Scenario Outline: Submit form with missing username shows error on <site>
    When I navigate to the comment form on "<site>"
    And I fill in the comment form with:
      | field     | value         |
      | username  |               |
      | content   | Test comment  |
    And I submit the form
    Then I should see an error message displayed
    And I should see field error "Your Alias or Name"
    Examples:
      | site     |
      | snatches |
      | services |
      | f-guitar |



  @regression
  Scenario Outline: Submit form with missing comment content shows error on <site>
    When I navigate to the comment form on "<site>"
    And I fill in the comment form with:
      | field     | value        |
      | username  | Test User    |
      | content   |              |
    And I submit the form
    Then I should see an error message displayed
    And I should see field error "Comments"
    Examples:
      | site     |
      | snatches |
      | services |
      | f-guitar |



  @regression
  Scenario Outline: Submit form with incorrect challenge answer shows error on <site>
    When I navigate to the comment form on "<site>"
    And I fill in the comment form with:
      | field     | value         |
      | username  | Test User     |
      | content   | Test comment  |
      | challenge | wrong_answer  |
    And I submit the form
    Then I should see an error message displayed
    And I should see field error "Submission Challenge"
    Examples:
      | site     |
      | snatches |
      | services |
      | f-guitar |
