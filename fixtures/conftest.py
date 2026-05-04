import pytest
import os
import json
import base64
from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page
from utils.timeouts import MEDIUM

BASE_URL = os.getenv("HOME_URL", "https://www.demoblaze.com/")
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
VIDEOS_DIR = REPORTS_DIR / "videos"


def _safe_test_name(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_", ".") else "_" for ch in name)


def _capture_failure_artifacts(item):
    """Capture screenshot and video path from current page on failure."""
    page = getattr(item, "funcargs", {}).get("page")
    if page is None:
        return None, None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = _safe_test_name(item.name)

    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    screenshot_path = SCREENSHOTS_DIR / f"failure_{timestamp}_{safe_name}.png"
    page.screenshot(path=str(screenshot_path))

    video_path = None
    try:
        if page.video:
            video_path = page.video.path()
    except Exception:
        # Video path may not be ready in some edge cases.
        pass

    return str(screenshot_path), video_path


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the application under test."""
    return BASE_URL


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Enable Playwright video recording so failure videos can be attached to reports."""
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    return {
        **browser_context_args,
        "record_video_dir": str(VIDEOS_DIR),
        "record_video_size": {"width": 1280, "height": 720},
    }


@pytest.fixture
def logged_in_page(page: Page, request):
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
            page.wait_for_timeout(MEDIUM)

    if last_error is not None:
        # Capture setup-failure artifacts while page is still available.
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = _safe_test_name(request.node.name)
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        screenshot_path = SCREENSHOTS_DIR / f"failure_{timestamp}_{safe_name}.png"
        page.screenshot(path=str(screenshot_path))
        request.node._failure_screenshot = str(screenshot_path)

        try:
            if page.video:
                request.node._failure_video = page.video.path()
        except Exception:
            pass

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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Make test result available to fixtures."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if rep.failed:
        screenshot_path = getattr(item, "_failure_screenshot", None)
        video_path = getattr(item, "_failure_video", None)

        if not screenshot_path and not video_path:
            screenshot_path, video_path = _capture_failure_artifacts(item)

        if screenshot_path:
            print(f"Screenshot saved: {screenshot_path}")
        if video_path:
            print(f"Video saved: {video_path}")

        pytest_html = item.config.pluginmanager.getplugin("html")
        if pytest_html:
            extras = getattr(rep, "extras", [])

            if screenshot_path and os.path.exists(screenshot_path):
                with open(screenshot_path, "rb") as f:
                    screenshot_b64 = base64.b64encode(f.read()).decode("utf-8")
                extras.append(pytest_html.extras.image(screenshot_b64, mime_type="image/png", extension="png"))
                extras.append(pytest_html.extras.url(f"file://{screenshot_path}", name="Screenshot file"))

            if video_path and os.path.exists(video_path):
                extras.append(pytest_html.extras.url(f"file://{video_path}", name="Failure video"))

            rep.extras = extras




