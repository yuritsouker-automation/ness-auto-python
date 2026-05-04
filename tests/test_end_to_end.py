import json
from pathlib import Path
import pytest
from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.login_page import LoginPage


# ──────────────────────────────────────────────
# Helper: load test data from JSON files
# ──────────────────────────────────────────────
SEARCH_TEST_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "search_test_data.json"


def load_search_test_data() -> list:
    """Read search test data entries from the JSON input file."""
    with open(SEARCH_TEST_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


SEARCH_TEST_CASES = load_search_test_data()


def build_search_test_case_id(test_data: dict) -> str:
    """Build a readable pytest case id from a JSON test-data entry."""
    query = test_data["query"]
    max_price = test_data["max_price"]
    limit = test_data["limit"]
    budget_per_item = test_data["budget_per_item"]
    return f"{query}-max{max_price}-limit{limit}-budget{budget_per_item}"


# ──────────────────────────────────────────────
# End-to-end test class
# ──────────────────────────────────────────────
class TestValidateEndToEnd:
    """End-to-end tests for https://www.demoblaze.com/"""

    @pytest.mark.parametrize(
        "test_data",
        SEARCH_TEST_CASES,
        ids=[build_search_test_case_id(test_data) for test_data in SEARCH_TEST_CASES],
    )
    def test_search_and_add_to_cart(self, logged_in_page: Page, test_data: dict):
        """
        Verify that products can be searched by price and added to cart
        by a logged-in user.
        """
        home_page = HomePage(logged_in_page)
        cart_page = CartPage(logged_in_page)
        login_page = LoginPage(logged_in_page)

        query = test_data["query"]
        max_price = test_data["max_price"]
        limit = test_data["limit"]
        budget_per_item = test_data["budget_per_item"]

        try:
            urls = home_page.search_items_by_name_under_price(query, max_price, limit)
            print(
                f"\nTest data: query={query}, max_price={max_price}, limit={limit}, "
                f"budget_per_item={budget_per_item}"
            )
            print(f"Found {len(urls)} products to add to cart:")
            for url in urls:
                print(f"  - {url}")

            assert len(urls) > 0, f"No products found with the search criteria for query={query}"

            cart_results = cart_page.add_items_to_cart(urls)

            successful_adds = [item for item in cart_results if item.get("status") == "added"]
            print(f"\nSuccessfully added {len(successful_adds)} items to cart for query={query}")

            assert len(successful_adds) > 0, f"No items were successfully added to cart for query={query}"
            cart_page.assert_cart_total_not_exceeds(budget_per_item, len(successful_adds))
        finally:
            try:
                login_page.logout()
            except Exception as exc:
                print(f"Logout in finally failed: {exc}")
