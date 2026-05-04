import os
from playwright.sync_api import Page


class CartPage:
    HOME_URL = os.getenv("HOME_URL", "https://www.demoblaze.com/")

    # Locators
    CART_NAV_LINK = "#cartur"
    CART_TOTAL_VALUE = "#totalp"
    CART_DELETE_LINKS = "a[onclick^='deleteItem']"
    PRODUCT_TITLE = "h2"
    ADD_TO_CART_BUTTON = "text='Add to cart'"

    def __init__(self, page: Page):
        self.page = page

    def open_cart(self):
        """Open the shopping cart page."""
        self.page.click(self.CART_NAV_LINK)
        self.page.wait_for_url("**/cart.html")
        self.page.wait_for_load_state("domcontentloaded")

    def get_cart_total_amount(self) -> float:
        """Return the numeric cart total shown on the cart page."""
        total_locator = self.page.locator(self.CART_TOTAL_VALUE)
        if total_locator.count() == 0:
            return 0.0

        total_text = total_locator.inner_text().strip()
        numeric_text = "".join(ch for ch in total_text if ch.isdigit() or ch == ".")
        return float(numeric_text) if numeric_text else 0.0

    def clear_cart(self):
        """Remove all existing items from the cart so each test starts clean."""
        self.open_cart()
        self.page.wait_for_timeout(2000)

        # Run multiple cleanup passes because DemoBlaze cart rendering can lag.
        for _ in range(5):
            for _ in range(30):
                delete_links = self.page.locator(self.CART_DELETE_LINKS)
                delete_count = delete_links.count()
                if delete_count == 0:
                    break

                delete_links.first.click()
                self.page.wait_for_timeout(1200)

            self.page.reload(wait_until="domcontentloaded")
            self.page.wait_for_timeout(1800)

            remaining_delete_links = self.page.locator(self.CART_DELETE_LINKS).count()
            remaining_total = self.get_cart_total_amount()
            if remaining_delete_links == 0 and remaining_total == 0:
                break

        remaining_delete_links = self.page.locator(self.CART_DELETE_LINKS).count()
        remaining_total = self.get_cart_total_amount()
        if remaining_delete_links != 0 or remaining_total != 0:
            raise AssertionError(
                f"Failed to clear cart. Remaining delete links: {remaining_delete_links}, "
                f"remaining total: {remaining_total}"
            )

        self.page.goto(self.HOME_URL)
        self.page.wait_for_timeout(1000)

    def add_items_to_cart(self, urls: list) -> list:
        """
        Loop through product URLs and add items to cart, with screenshot logging.

        Attempts to select variants randomly if available (via radio buttons, checkboxes).
        For complex dropdown selects, they are skipped to avoid timeout issues.

        :param urls: List of product URLs to add to cart.
        :return:     List of dictionaries with product info and screenshot paths.
        """
        import os
        import random
        from datetime import datetime

        added_items = []

        self.page.on("dialog", lambda dialog: dialog.accept())
        self.clear_cart()

        for idx, url in enumerate(urls):
            try:
                # Navigate to product page
                self.page.goto(url)
                self.page.wait_for_load_state("domcontentloaded")
                self.page.wait_for_selector(self.PRODUCT_TITLE, state="visible")

                # Get product title
                title_elem = self.page.query_selector(self.PRODUCT_TITLE)
                product_title = title_elem.inner_text() if title_elem else f"Product {idx + 1}"

                # Attempt to select simple variants (radio buttons, checkboxes)
                try:
                    radio_groups = {}
                    radios = self.page.query_selector_all("input[type='radio']")
                    for radio in radios:
                        try:
                            group_name = radio.get_attribute("name") or ""
                            if group_name and group_name not in radio_groups:
                                group_radios = self.page.query_selector_all(f"input[type='radio'][name='{group_name}']")
                                if group_radios:
                                    random_radio = random.choice(group_radios)
                                    random_radio.click()
                                    self.page.wait_for_timeout(100)
                                    radio_groups[group_name] = True
                        except Exception:
                            pass

                    try:
                        qty_input = self.page.query_selector("input[type='number']")
                        if qty_input and qty_input.is_enabled():
                            qty_input.fill(str(random.randint(1, 3)))
                            self.page.wait_for_timeout(100)
                    except Exception:
                        pass
                except Exception:
                    pass

                add_cart_btn = self.page.locator(self.ADD_TO_CART_BUTTON).first
                if add_cart_btn.count() > 0:
                    add_cart_btn.click()
                    self.page.wait_for_timeout(1000)

                    screenshot_dir = os.path.join(os.path.dirname(__file__), "..", "reports", "cart_screenshots")
                    os.makedirs(screenshot_dir, exist_ok=True)

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshot_path = os.path.join(screenshot_dir, f"cart_{idx + 1}_{timestamp}.png")
                    self.page.screenshot(path=screenshot_path)

                    added_items.append(
                        {
                            "title": product_title,
                            "url": url,
                            "screenshot": screenshot_path,
                            "status": "added",
                        }
                    )

                    print(f"Added to cart: {product_title}")
                else:
                    added_items.append(
                        {
                            "title": product_title,
                            "url": url,
                            "status": "failed - button not found",
                        }
                    )
                    print(f"Failed to add: {product_title} (Add to cart button not found)")

            except Exception as e:
                added_items.append({"url": url, "status": f"error - {str(e)}"})
                print(f"Error processing {url}: {str(e)}")

        # Return to home page after processing
        self.page.goto(self.HOME_URL)
        self.page.wait_for_timeout(1000)

        return added_items

    def assert_cart_total_not_exceeds(self, budget_per_item: float, items_count: int) -> None:
        """
        Open the shopping cart, read the displayed total amount, and assert
        the total does not exceed budget_per_item * items_count.

        Also saves cart evidence artifacts (screenshot + JSON + HTML snapshot)
        under reports/cart_validation.

        :param budget_per_item: Maximum allowed amount per item.
        :param items_count:     Number of items for threshold calculation.
        """
        import json
        from datetime import datetime
        from pathlib import Path

        self.open_cart()
        self.page.wait_for_selector(self.CART_TOTAL_VALUE, state="visible")

        total_text = self.page.locator(self.CART_TOTAL_VALUE).inner_text().strip()
        total_amount = self.get_cart_total_amount()
        if not total_text:
            raise AssertionError("Cart total is empty")
        threshold = float(budget_per_item) * int(items_count)

        report_dir = Path(__file__).resolve().parent.parent / "reports" / "cart_validation"
        report_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        screenshot_path = report_dir / f"cart_{timestamp}.png"
        json_path = report_dir / f"cart_{timestamp}.json"
        html_path = report_dir / f"cart_{timestamp}.html"

        self.page.screenshot(path=str(screenshot_path), full_page=True)
        json_path.write_text(
            json.dumps(
                {
                    "timestamp": timestamp,
                    "cart_url": self.page.url,
                    "budget_per_item": float(budget_per_item),
                    "items_count": int(items_count),
                    "threshold": threshold,
                    "displayed_total_text": total_text,
                    "parsed_total": total_amount,
                    "passed": total_amount <= threshold,
                    "screenshot": str(screenshot_path),
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        html_path.write_text(self.page.content(), encoding="utf-8")

        assert total_amount <= threshold, (
            f"Cart total {total_amount} exceeds threshold {threshold} "
            f"(budget_per_item={budget_per_item}, items_count={items_count}). "
            f"Artifacts: {screenshot_path}, {json_path}, {html_path}"
        )

