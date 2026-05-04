# DemoBlaze Automation Framework

A Python-based test automation framework for [DemoBlaze](https://www.demoblaze.com/) using Playwright and Pytest.

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ness-auto-python.git
   cd ness-auto-python
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

4. **Configure environment** (optional)
   ```bash
   cp .env.example .env.local
   # Edit .env.local if testing against non-default URL
   ```

## 📋 Project Structure

```
ness-auto-python/
├── pages/                      # Page Object Models
│   ├── home_page.py           # Homepage - search functionality
│   ├── login_page.py          # Login page - authentication
│   └── cart_page.py           # Cart page - cart operations & validation
├── tests/                      # Test cases
│   └── test_end_to_end.py     # End-to-end test scenarios
├── fixtures/                   # Pytest fixtures
│   └── conftest.py            # Reusable test fixtures
├── data/                       # Test data
│   ├── credentials.json       # Login credentials
│   └── search_test_data.json  # Search query parameters
├── .github/workflows/          # GitHub Actions CI/CD
│   └── tests.yml              # Test workflow
├── .env.example               # Environment variables template
├── requirements.txt           # Python dependencies
└── pytest.ini                 # Pytest configuration
```

## 🧪 Running Tests

### Local Development (Headed Mode - with Browser UI)

```bash
# Run all tests with browser UI visible
python -m pytest tests -v --headed

# Run specific test with UI
python -m pytest tests/test_end_to_end.py::TestValidateEndToEnd::test_search_and_add_to_cart -v --headed
```

### Headless Mode (CI/CD - default)

```bash
# Run all tests headless (no browser UI)
python -m pytest tests -v

# Explicitly override to headless if pytest.ini has --headed
python -m pytest tests -o addopts="" -v
```

### Custom Environment

```bash
# Test against staging
HOME_URL=https://staging.demoblaze.com/ python -m pytest tests -v

# Test against local instance
HOME_URL=http://localhost:8000/ python -m pytest tests -v
```

## 📊 Test Reports

### Generate & View Local Report

```bash
# Run tests and generate HTML report
python -m pytest tests -v --html=reports/report.html --self-contained-html

# Open report in browser
open reports/report.html  # macOS
# xdg-open reports/report.html  # Linux
# start reports/report.html  # Windows
```

### GitHub Actions Reports

1. Go to **Actions** tab in your GitHub repository
2. Click the latest workflow run
3. Scroll to **Artifacts** section
4. Download desired artifact:
   - `pytest-report` — Main test report
   - `cart-validation` — Cart validation data
   - `test-screenshots` — Failure screenshots

### Example: Successful GitHub Run

- **Workflow run:** [Run #25318321544](https://github.com/yuritsouker-automation/ness-auto-python/actions/runs/25318321544/job/74220852982)
- **Main report artifact download:** [Artifact #6783147186](https://github.com/yuritsouker-automation/ness-auto-python/actions/runs/25318321544/artifacts/6783147186)
- **Cart validation artifact download:** [Artifact #6783147402](https://github.com/yuritsouker-automation/ness-auto-python/actions/runs/25318321544/artifacts/6783147402)

### Example: Failed GitHub Run

- **Workflow run:** [Run #25320954700](https://github.com/yuritsouker-automation/ness-auto-python/actions/runs/25320954700)

## ⚙️ Configuration

### Environment Variables

See [ENV_VARIABLES.md](ENV_VARIABLES.md) for complete documentation.

**Common variables:**
- `HOME_URL` — Base URL (default: `https://www.demoblaze.com/`)

**Example `.env.local`:**
```
HOME_URL=https://staging.demoblaze.com/
```

### Test Data

Edit `data/search_test_data.json` to add/modify test scenarios:

```json
[
  {
    "query": "Phones",
    "max_price": 500,
    "limit": 3,
    "budget_per_item": 500
  }
]
```

### Credentials

Update `data/credentials.json` with test account:

```json
{
  "username": "your-email@example.com",
  "password": "your-password"
}
```

## 📚 Documentation

- **[CI/CD Setup](CI_CD_SETUP.md)** — GitHub Actions workflow documentation
- **[Environment Variables](ENV_VARIABLES.md)** — Configuration guide
- **[Framework Guide](FRAMEWORK_GUIDE.md)** — Architecture & components
- **[Fixtures](FIXTURES.md)** — Pytest fixtures reference
- **[Cart Function](CART_FUNCTION.md)** — Cart operations details

## 🏗️ Project Architecture

### Page Objects
- **HomePage** — Product search, filtering
- **LoginPage** — User authentication
- **CartPage** — Cart operations, validation

### Fixtures
- `logged_in_page` — Authenticated user session
- `clear_cart` — Empty cart before test

### Tests
- `test_search_and_add_to_cart` — Parametrized E2E test
  - Searches products by category and price
  - Adds items to cart
  - Validates cart total

## About The Tests
1. The framework was chosen to test `https://www.demoblaze.com/`.
   - I also tried large commerce sites like eBay/Amazon, but anti-bot/user-captcha protections do not allow stable automation runs for this project scope.

2. Each test starts with login from fixtures.
   - Login credentials are currently loaded from `data/credentials.json`.
   - Best practice for future hardening: store credentials in environment variables (or CI secrets) instead of JSON files.

3. Each test starts with cart cleanup from fixtures.
   - The `clear_cart` fixture ensures a clean cart state in case a previous test failed before cleanup.

4. The test iterates over `data/search_test_data.json`.
   - Each JSON entry is executed as a separate parametrized test row.
   - You can see a separate row per iteration in the HTML report.

## 🔄 CI/CD Pipeline

Tests run automatically on GitHub Actions:
- **Triggers:** Every push, every PR to `main`
- **Browser:** Chromium (headless)
- **Python:** 3.13
- **Artifacts:** Reports, screenshots, validation data

See [.github/workflows/tests.yml](.github/workflows/tests.yml) for workflow details.

## 🐛 Troubleshooting

### Tests timeout
- Reduce `limit` in `data/search_test_data.json`
- Increase `timeout` in `pytest.ini`

### Playwright installation fails
```bash
playwright install chromium
# Or reinstall all browsers:
playwright install
```

### Custom URL not loading
- Verify `HOME_URL` is accessible
- Check network/firewall
- Test with `curl`/browser first

### Artifacts missing from CI
- Check workflow logs for errors
- Verify reports directory exists
- Check artifact retention days (set to 30)

## 🚀 Next Steps

1. ✅ Clone & install dependencies
2. ✅ Configure credentials in `data/credentials.json`
3. ✅ Run tests locally: `python -m pytest tests -v --headed`
4. ✅ Push to GitHub to trigger CI/CD
5. ✅ Review reports in Actions artifacts

## 📝 Contributing

1. Create feature branch from `main`
2. Make changes to page objects or tests
3. Run tests locally to verify
4. Push branch & create PR
5. CI/CD runs automatically
6. Merge after review

## 📞 Support

- Check test reports for failure details
- Review logs in GitHub Actions
- See documentation files in root directory

---

**Last Updated:** May 4, 2026  
**Framework Version:** 1.0.0  
**Python:** 3.13+  
**Playwright:** 1.59.0+

