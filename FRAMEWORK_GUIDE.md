# Automation Framework - Quick Reference

## Project Structure

```
ness-auto-python/
├── pages/
│   ├── __init__.py
│   ├── home_page.py        # Product search & cart operations
│   └── login_page.py       # Authentication operations
├── tests/
│   ├── __init__.py
│   └── test_end_to_end.py  # Test suite
├── utils/
│   ├── __init__.py
│   └── report_config.py    # Reporting utilities
├── data/
│   └── credentials.json    # Test credentials
├── reports/                # Generated test reports & screenshots
├── conftest.py            # Pytest fixtures & hooks
├── pytest.ini             # Pytest configuration
├── manage_reports.sh      # Report management helper
└── venv/                  # Virtual environment
```

## Page Objects

### LoginPage (`pages/login_page.py`)
**Methods:**
- `login(username, password)` - Perform login
- `validate_logged_in(expected_username)` - Verify login success
- `logout()` - Perform logout
- `get_welcome_user_locator()` - Get welcome message element

**Locators:**
- `LOGIN_NAV_BUTTON` - "#login2"
- `USERNAME_INPUT` - "#loginusername"
- `PASSWORD_INPUT` - "#loginpassword"
- `LOGIN_SUBMIT_BUTTON` - "button[onclick='logIn()']"
- `WELCOME_USER_LINK` - "#nameofuser"
- `LOGOUT_BUTTON` - "#logout2"

### HomePage (`pages/home_page.py`)
**Methods:**
- `navigate()` - Go to home page
- `search_items_by_name_under_price(query, max_price, limit=5)` - Search products by category and price
- `add_items_to_cart(urls)` - Add products to cart with screenshots

**Locators:**
- `PRODUCT_CARDS_XPATH` - "//div[@id='tbodyid']//div[contains(@class,'card-block')]"
- `PRODUCT_TITLE_LINK` - "h4.card-title a"
- `PRODUCT_PRICE` - "h5"
- `NEXT_PAGE_BUTTON` - "#next2"

## Test Cases

### TestValidateEndToEnd
Located in `tests/test_end_to_end.py`

**test_login**
- Navigate to DemoBlaze
- Login with credentials from `data/credentials.json`
- Verify welcome message
- Logout and verify

**test_search_and_add_to_cart**
- Search for phones under $500
- Add up to 3 items to cart
- Capture screenshots for each add
- Verify all items added successfully

## Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test class
python -m pytest tests/test_end_to_end.py::TestValidateEndToEnd

# Run specific test method
python -m pytest tests/test_end_to_end.py::TestValidateEndToEnd::test_login

# Run with verbose output
python -m pytest -v

# Run with specific browser
python -m pytest --browser chromium

# Run headless (no browser UI)
python -m pytest --browser chromium -p no:head
```

## Reports

### HTML Report
- **Location:** `reports/report.html`
- **Generated:** Automatically after each test run
- **Contents:**
  - Test results summary
  - System metadata
  - Test execution timeline
  - Pass/Fail statistics

### Cart Screenshots
- **Location:** `reports/cart_screenshots/`
- **Format:** PNG images
- **Naming:** `cart_{index}_{timestamp}.png`

### Report Management
```bash
./manage_reports.sh open      # Open HTML report
./manage_reports.sh clean     # Delete all reports
./manage_reports.sh generate  # Run tests and generate fresh reports
```

## Test Data

### Credentials (`data/credentials.json`)
```json
{
  "username": "yuri.tsouker+1@gmail.com",
  "password": "Qa123456"
}
```

To update credentials, modify this file (will be used by all tests).

## Key Features

✅ **Page Object Model**
- Centralized locator management
- Reusable page methods
- Easy maintenance

✅ **Automatic Reporting**
- HTML reports with metadata
- Screenshot capture on failures
- Test timeline tracking

✅ **Screenshot Logging**
- Captured after cart additions
- Timestamped for traceability
- Organized in dedicated folders

✅ **Error Resilience**
- Graceful error handling
- Detailed error messages
- Non-blocking variant selections

✅ **Flexible Search**
- Category-based product search
- Price filtering
- Pagination support
- Configurable result limits

## Configuration

### pytest.ini
Controls test execution:
- Browser: Chromium
- Mode: Headed (with UI)
- Verbosity: High
- Report: Auto-generated HTML

### conftest.py
Provides:
- Base URL fixture
- Screenshot on failure
- Test metadata capture

## Extending the Framework

### Add New Page Object
```python
# pages/product_page.py
from playwright.sync_api import Page

class ProductPage:
    URL = "https://www.demoblaze.com/prod.html"
    
    # Locators
    TITLE = "h2"
    PRICE = ".price"
    
    def __init__(self, page: Page):
        self.page = page
    
    def get_title(self):
        return self.page.query_selector(self.TITLE).inner_text()
```

### Add New Test
```python
# tests/test_products.py
from pages.product_page import ProductPage

class TestProducts:
    def test_product_details(self, page):
        product = ProductPage(page)
        product.navigate()
        assert product.get_title() == "Product Name"
```

## Troubleshooting

| Issue | Solution |
|---|---|
| Tests timeout | Reduce limits in `search_items_by_name_under_price()` |
| Screenshots not saving | Ensure `reports/` directory is writable |
| Locators not found | Verify site hasn't changed, use inspector tool |
| Variant selection fails | Check if elements are visible/enabled first |

## Dependencies

- **playwright** (1.59.0+) - Browser automation
- **pytest** (9.0.3+) - Test framework
- **pytest-html** (4.2.0+) - HTML reporting
- **pytest-playwright** (0.7.2+) - Pytest integration

## Performance Benchmarks

| Operation | Time |
|---|---|
| Single search query | ~2-3 seconds |
| Add to cart (1 item) | ~3-4 seconds |
| Full test run (2 tests) | ~20 seconds |
| Screenshot capture | ~200-300ms |

## Next Steps

1. Add more test scenarios (checkout flow, payment, etc.)
2. Implement data-driven testing with CSV/Excel
3. Add API layer for test data setup
4. Integrate with CI/CD pipeline
5. Add cross-browser testing support
6. Implement visual regression testing

---

**Last Updated:** May 4, 2026
**Framework Version:** 1.0.0

