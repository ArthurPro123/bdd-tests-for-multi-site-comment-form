
"""
Page Object Model for comment form interactions across multiple sites.
Encapsulates selectors, actions, and validation logic for the comment form.
"""

from playwright.sync_api import Page


class CommentFormPage:
    """Page object for comment form operations."""
    
    def __init__(self, page: Page, site_config: dict):
        """Initialize page object with site-specific selectors."""
        self.page = page
        self.config = site_config
        self.username_field_selector = f"{site_config['username_field_selector']}"
        self.content_field_selector = f"{site_config['content_field_selector']}"
        self.challenge_field_selector = f"{site_config['challenge_field_selector']}"
        self.submit_button_selector = site_config['submit_button_selector']
        
        # Optional selectors with defaults
        self.form_selector = site_config.get('form_selector')
        self.error_container_selector = site_config.get('error_container_selector')
        self.error_list_selector = site_config.get('error_list_selector')
        self.success_container_selector = site_config.get('success_container_selector', '.main-message--success')
        self.success_text = site_config.get('success_message', 'Your comment has been posted')

    def navigate(self):
        """Navigate to site URL and wait for form to load."""
        self.page.goto(self.config['url'], wait_until='networkidle')
        self.page.wait_for_selector(self.form_selector)

    def get_captcha_answer(self) -> str:
        """Extract captcha question from page, compute and return answer."""
        captcha_question = self.page.text_content(".form__submission-challenge-question-container")
        word_to_num = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
        }
        words = captcha_question.lower().split()
        return str(word_to_num.get(words[0], 0) + word_to_num.get(words[2], 0))

    def fill_username(self, username: str):
        """Fill username field. Empty string clears the field."""
        self.page.fill(self.username_field_selector, username or "")

    def fill_content(self, content: str):
        """Fill comment content field. Empty string clears the field."""
        self.page.fill(self.content_field_selector, content or "")

    def fill_challenge(self, answer: str = None):
        """Fill challenge field. Auto-calculates answer if not provided."""
        if not answer:
            answer = self.get_captcha_answer()
        self.page.fill(self.challenge_field_selector, answer)

    def submit_form(self):
        """Submit form and wait for response."""
        self.page.click(self.submit_button_selector)

    def submit_empty_form(self):
        """Submit form without waiting (used for validation testing)."""
        self.page.click(self.submit_button_selector)

    def is_error_displayed(self) -> bool:
        """Check if error message is visible (3 second timeout)."""
        try:
            self.page.wait_for_selector(f"{self.error_container_selector}:not([style*='display: none'])", timeout=3000)
            return True
        except:
            return False

    def get_error_messages(self) -> list:
        """Extract and return list of validation error messages."""
        try:
            self.page.wait_for_selector(self.error_list_selector, timeout=3000)
            return [link.text_content().strip().replace('•', '').strip() 
                    for link in self.page.query_selector_all(f"{self.error_list_selector} li a")]
        except:
            return []

    def is_success_message_displayed(self) -> bool:
        """Check if success message is displayed."""
        try:
            self.page.wait_for_selector(self.success_container_selector, timeout=3000)
            return self.success_text.lower() in self.page.text_content(self.success_container_selector).lower()
        except:
            return False
