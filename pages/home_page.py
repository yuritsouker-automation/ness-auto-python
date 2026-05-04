import os
from playwright.sync_api import Page


class HomePage:
    URL = os.getenv("HOME_URL", "https://www.demoblaze.com/")

    # Locators
    PRODUCT_CARDS_XPATH = "//div[@id='tbodyid']//div[contains(@class,'card-block')]"
    PRODUCT_TITLE_LINK = "h4.card-title a"
    PRODUCT_PRICE = "h5"
    NEXT_PAGE_BUTTON = "#next2"

    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        """Navigate to the DemoBlaze home page."""
        self.page.goto(self.URL)

    def search_items_by_name_under_price(self, query: str, max_price: float, limit: int = 5) -> list:
        """
        Search for products by category name and return up to `limit` product URLs
        whose price is less than or equal to `max_price`.

        Evaluates only the currently visible page and returns up to `limit`
        qualifying items without navigating pagination.

        :param query:     Category name to click (e.g. "Phones", "Laptops").
        :param max_price: Maximum allowed price (inclusive).
        :param limit:     Maximum number of product URLs to return (default 5).
        :return:          List of absolute product URLs satisfying the price condition.
        """
        collected: list = []

        # Click the category link whose visible text matches `query`
        self.page.click(f"text={query}")
        self.page.wait_for_timeout(1500)

        # Wait for at least one product card to be present on the current page
        self.page.wait_for_selector(self.PRODUCT_CARDS_XPATH, state="attached")
        self.page.wait_for_timeout(500)

        cards = self.page.query_selector_all(self.PRODUCT_CARDS_XPATH)

        for card in cards:
            if len(collected) >= limit:
                break

            price_el = card.query_selector(self.PRODUCT_PRICE)
            title_el = card.query_selector(self.PRODUCT_TITLE_LINK)

            if not price_el or not title_el:
                continue

            # Price text is e.g. "$360" — strip the dollar sign and convert
            price_text = price_el.inner_text().replace("$", "").replace(",", "").strip()
            try:
                price = float(price_text)
            except ValueError:
                continue

            if price <= max_price:
                href = title_el.get_attribute("href") or ""
                # Build absolute URL when only a relative path is returned
                if href.startswith("http"):
                    full_url = href
                else:
                    full_url = self.URL.rstrip("/") + "/" + href.lstrip("/")
                collected.append(full_url)


        return collected


