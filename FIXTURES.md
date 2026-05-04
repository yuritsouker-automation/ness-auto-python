# Pytest Fixtures Documentation

## Available Fixtures

### `base_url`
**Scope:** Session (shared across all tests)
**Type:** String
**Value:** `"https://www.demoblaze.com/"`

Usage:
```python
def test_example(self, base_url):
    assert base_url == "https://www.demoblaze.com/"
```

---

### `logged_in_page`
**Scope:** Function (fresh for each test)
**Type:** `Page` (Playwright page object)
**Returns:** Authenticated page with logged-in user session

**What it does:**
1. Loads credentials from `data/credentials.json`
2. Creates `HomePage` and `LoginPage` objects
3. Navigates to the home page
4. Performs login with loaded credentials
5. Validates that login was successful
6. Returns the authenticated page

**Usage:**
```python
def test_search_and_add_to_cart(self, logged_in_page: Page):
    home_page = HomePage(logged_in_page)
    urls = home_page.search_items_by_name_under_price("Phones", 500, 3)
    # ... test continues with authenticated session
```

**Benefits:**
- ✅ Eliminates login boilerplate from tests
- ✅ DRY principle - reusable across multiple tests
- ✅ Automatic validation of login success
- ✅ Clean separation of concerns

---

## How Fixtures Work

### Fixture Resolution Order

When a test requests a fixture:
```python
def test_example(self, logged_in_page: Page):
    # Pytest looks up 'logged_in_page' fixture
    # Finds it in conftest.py
    # Executes it and passes result to test
```

### Fixture Scope

| Scope | Behavior | Use Case |
|---|---|---|
| `function` | New instance per test | Default; test isolation |
| `class` | One per test class | Shared within class |
| `module` | One per module | Heavy setup (DB, browsers) |
| `session` | One for entire session | Read-only data, constants |

---

## Adding New Fixtures

### Example: `authenticated_cart_page`
```python
@pytest.fixture
def authenticated_cart_page(logged_in_page: Page):
    """
    Fixture that provides an authenticated session on the cart page.
    Extends the logged_in_page fixture.
    """
    home_page = HomePage(logged_in_page)
    home_page.navigate()  # Ensure on home page
    # Could navigate to cart or add some items
    return logged_in_page
```

### Using Fixture Composition
```python
# In your test
def test_cart_operations(self, authenticated_cart_page: Page):
    # Already logged in and ready to test cart
    pass
```

---

## Current Test Usage

### `test_login`
- **Fixture:** None (tests login itself)
- **Flow:** Navigate → Login → Validate → Logout

### `test_search_and_add_to_cart`
- **Fixture:** `logged_in_page` ✓
- **Flow:** Fixture handles login → Search → Add to cart → Verify

---

## Fixture Best Practices

✅ **DO:**
- Use fixtures for common setup (auth, navigation, data loading)
- Keep fixtures focused and single-purpose
- Use descriptive fixture names
- Document what the fixture does
- Compose fixtures for reusability

❌ **DON'T:**
- Make fixtures do too much (violates single responsibility)
- Use fixtures to hide test logic
- Create hard dependencies between fixtures without good reason
- Ignore fixture scope implications

---

## Debugging Fixtures

### List all available fixtures
```bash
pytest --fixtures
```

### Run test with fixture debugging
```bash
pytest -v --setup-show tests/test_end_to_end.py
```

### Output:
```
test_end_to_end.py::TestValidateEndToEnd::test_search_and_add_to_cart[chromium]
    SETUP    F fixture 'logged_in_page' (function scope)
    test_search_and_add_to_cart ...
    TEARDOWN F fixture 'logged_in_page' (function scope)
```

---

## Related Configuration

- **conftest.py** - Fixture definitions
- **pytest.ini** - Test configuration
- **data/credentials.json** - User credentials used by `logged_in_page`

---

## Migration Guide

### Before (Manual Login Each Test)
```python
def test_example(self, page: Page):
    credentials = load_credentials()
    home_page = HomePage(page)
    login_page = LoginPage(page)
    home_page.navigate()
    login_page.login(credentials["username"], credentials["password"])
    login_page.validate_logged_in(credentials["username"])
    
    # Now test logic...
```

### After (Using Fixture)
```python
def test_example(self, logged_in_page: Page):
    home_page = HomePage(logged_in_page)
    
    # Now test logic...
```

**Result:** ~10 lines of setup code eliminated, tests more readable and maintainable

---

## Next Steps

Consider adding fixtures for:
1. `product_under_price` - Search products and return URLs
2. `items_in_cart` - Add items to cart and return results
3. `cart_page` - Navigate to cart with logged-in session
4. `admin_user` - Fixture with admin credentials
5. `test_data_cleanup` - Cleanup after tests complete

---

**Last Updated:** May 4, 2026
**Framework Version:** 1.0.0

