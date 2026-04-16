# web_interface_steps.py

"""
Step definitions for comment form testing across multiple sites.

This module contains Behave step implementations that interact with the
comment form page object and validate expected behaviors.
"""

from behave import given, when, then
from pages.comment_form_page import CommentFormPage

import colorama as color

# Initialize colorama for colored console output
color.init(autoreset=True)


@given('I have access to comment forms on all configured sites')
def step_load_configuration(context):
    """
    Verify access to all configured comment forms.
    
    Configuration is already loaded in environment.py's before_all hook.
    This step exists to satisfy the Gherkin background step.
    
    Args:
        context: Behave context containing sites_config and other shared data
    """
    pass  # Config already loaded, nothing to do


@when('I navigate to the comment form on "{site_name}"')
def step_navigate_to_site(context, site_name):
    """
    Navigate to the comment form on the specified site.
    
    Creates a new page in the current browser session and initializes
    the page object for the given site.
    
    Args:
        context: Behave context containing browser_session and sites_config
        site_name: Name of the site to navigate to (must exist in sites_config)
    """
    page = context.browser_session.new_page()
    context.current_form = CommentFormPage(page, context.sites_config[site_name])
    context.current_form.navigate()


@when('I fill in the comment form with')
def step_fill_form(context):
    """
    Fill the comment form with values from a data table.
    
    Expects a Gherkin data table with columns: field | value
    Supported fields: username, content, challenge
    
    If challenge field is empty, the captcha answer is auto-calculated.
    
    Args:
        context: Behave context containing current_form
    """
    challenge_value = None
    
    for row in context.table:
        field = row[0].strip()
        value = row[1].strip() if len(row.cells) > 1 else ""
        
        if field == 'username':
            context.current_form.fill_username(value)
        elif field == 'content':
            context.current_form.fill_content(value)
        elif field == 'challenge':
            challenge_value = value
    
    if challenge_value:
        context.current_form.fill_challenge(challenge_value)
    else:
        context.current_form.fill_challenge()


@when('I submit the form')
@when('I submit the empty form')
def step_submit_form(context):
    """
    Submit the comment form.
    
    Args:
        context: Behave context containing current_form
    """
    context.current_form.submit_form()


@then('I should see success message "{expected_text}"')
def step_check_success_message(context, expected_text):
    """
    Verify that a success message is displayed after form submission.
    
    Args:
        context: Behave context containing current_form
        expected_text: Expected success message text
    """
    assert context.current_form.is_success_message_displayed(expected_text), \
        f"Success message '{expected_text}' not displayed"


@then('I should see an error message displayed')
@then('I should see an error message containing "{expected_text}"')
def step_check_error_displayed(context, expected_text: str = None):
    """
    Verify that an error message is displayed after invalid form submission.
    If expected_text provided, also verify error message contains that text.
    Supports optional (s) pattern for singular/plural variations.
    
    Args:
        context: Behave context containing current_form
        expected_text: substring expected in the error message (optional)
    """
    assert context.current_form.is_error_message_displayed(expected_text), \
        "Error message not displayed or text mismatch"


@then('I should see the following validation errors')
def step_check_validation_errors(context):
    """
    Verify that specific validation error messages appear.
    
    Expects a Gherkin data table with columns: field | error
    Displays colored output showing expected vs actual errors.
    
    Args:
        context: Behave context containing current_form
    """
    error_messages = context.current_form.get_form_field_error_messages()
    
    print(f"{color.Fore.YELLOW}")

    print(f"\n{'='*50}")
    print(f"VALIDATION ERROR CHECK")
    print(f"{'='*50}")
    print(f"Actual errors found: {len(error_messages)}\n")
    
    for i, msg in enumerate(error_messages, 1):
        print(f"  {i}. {msg}")
    
    print(f"\nExpected errors:")
    
    for row in context.table:

        field = row[0].strip()
        expected = row[1].strip()

        # Check if expected error is in actual errors
        found = any(expected.lower() in msg.lower() for msg in error_messages)

        status = "✓" if found else "✗"

        print(f"  • {field}: '{expected}' ({status} Found: {found})")
        
        
        assert found, f"Field '{field}': Expected error '{expected}' not found"
    
    print(f"\n✅ All validation errors verified")

    print(f"{color.Style.RESET_ALL}")


@then('I should see field error "{field_label}"')
def step_check_field_error(context, field_label):
    """
    Verify that a specific field has a validation error.
    
    Args:
        context: Behave context containing current_form
        field_label: Label of the field expected to have an error
    """
    error_messages = context.current_form.get_form_field_error_messages()

    assert any(field_label.lower() in e.lower() for e in error_messages), \
        f"'{field_label}' not found in {error_messages}"
