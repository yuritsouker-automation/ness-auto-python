import json
import os
import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage


# ──────────────────────────────────────────────
# Helper: load credentials from the JSON file
# ──────────────────────────────────────────────
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "credentials.json")


def load_credentials() -> dict:
    """Read username and password from the credentials JSON file."""
    with open(DATA_FILE, "r") as f:
        return json.load(f)


# ──────────────────────────────────────────────
# End-to-end test class
# ──────────────────────────────────────────────
class TestValidateEndToEnd:
    """End-to-end tests for https://www.demoblaze.com/"""

    def test_login(self, page: Page):
        """
        Verify that a user can log in to DemoBlaze and the welcome message
        is displayed with the correct username.
        """
        # Load credentials from the JSON input file
        credentials = load_credentials()
        username = credentials["username"]
        password = credentials["password"]

        # Navigate to the home page and perform login via the Page Object
        home_page = HomePage(page)
        home_page.navigate()
        home_page.login(username, password)

        # Validate that the welcome element is visible and contains the username
        home_page.validate_logged_in(username)

        # Logout and validate the login button is visible again
        home_page.logout()

