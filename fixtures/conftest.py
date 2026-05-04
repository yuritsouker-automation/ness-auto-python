import pytest
import os
import json
from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page
from utils.report_config import ReportConfig

BASE_URL = os.getenv("HOME_URL", "https://www.demoblaze.com/")


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the application under test."""
    return BASE_URL


@pytest.fixture
def logged_in_page(page: Page):
    """
    Fixture that provides a logged-in user session.
    Loads credentials from data/credentials.json, authenticates the user,
    and validates the login before returning the page object.

    :param page: Playwright page object (provided by pytest-playwright)
    :return:     Authenticated page object ready for testing
    """
    from pages.home_page import HomePage
    from pages.login_page import LoginPage

    # Load credentials from JSON file
    credentials_file = Path(__file__).resolve().parent.parent / "data" / "credentials.json"
    with open(credentials_file, "r") as f:
        credentials = json.load(f)

    username = credentials["username"]
    password = credentials["password"]

    # Navigate to home page and perform login
    home_page = HomePage(page)
    login_page = LoginPage(page)

    last_error = None
    for _ in range(2):
        try:
            home_page.navigate()
            login_page.login(username, password)
            login_page.validate_logged_in(username)
            last_error = None
            break
        except Exception as exc:
            last_error = exc
            page.goto(BASE_URL)
            page.wait_for_timeout(1500)

    if last_error is not None:
        raise last_error

    # Return the authenticated page
    return page


@pytest.fixture
def clear_cart(logged_in_page: Page):
    """Ensure cart is empty and return a CartPage instance for test use."""
    from pages.cart_page import CartPage

    cart_page = CartPage(logged_in_page)
    cart_page.clear_cart()
    return cart_page


@pytest.fixture(autouse=True)
def take_screenshot_on_failure(page, request):
    """Automatically take a screenshot on test failure."""
    yield

    if request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False:
        ReportConfig.ensure_reports_dir()
        screenshot_dir = os.path.join(ReportConfig.REPORTS_DIR, "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(screenshot_dir, f"failure_{timestamp}_{request.node.name}.png")
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Make test result available to fixtures."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)




