# GitHub Actions CI/CD Setup

## Workflow: Run Tests

This repository is configured to automatically run tests on GitHub Actions on every push and pull request.

### Workflow File
- **Location:** `.github/workflows/tests.yml`
- **Triggers:** 
  - Push to `main` or `develop` branches
  - Pull requests to `main` or `develop` branches

### What the workflow does

1. **Checkout code** — Clones the repository
2. **Setup Python** — Installs Python 3.13 with pip caching
3. **Install dependencies** — Runs `pip install -r requirements.txt`
4. **Install Playwright browsers** — Installs Chromium
5. **Run tests (headless)** — Executes pytest with:
   - `--browser chromium` (headless automatically)
   - `--html=reports/report.html` (generates HTML report)
   - `--self-contained-html` (single-file HTML, no external dependencies)
6. **Upload artifacts** — Saves reports, screenshots, and validation data

### Artifacts Generated

After each workflow run, the following artifacts are available for download:

| Artifact | Contents | Location |
|---|---|---|
| `pytest-report` | Main HTML test report | `reports/report.html` |
| `cart-validation` | Cart total validation data (JSON, HTML, PNG) | `reports/cart_validation/` |
| `test-screenshots` | Screenshots from failures | `reports/screenshots/` |

### How to access artifacts

1. **Go to GitHub Actions tab** in your repository
2. **Click the workflow run** (most recent first)
3. **Scroll to "Artifacts" section**
4. **Download** the desired artifact (e.g., `pytest-report`)
5. **Extract** the ZIP file
6. **Open** `reports/report.html` in a browser

### Local requirements.txt

The workflow uses `requirements.txt` to install dependencies. Ensure it's kept up-to-date:

```bash
pip freeze > requirements.txt
```

Or manually maintain it with your project's core dependencies:

```
pytest==9.0.3
pytest-playwright==0.7.2
pytest-html==4.2.0
pytest-metadata==3.1.1
playwright==1.59.0
```

### Customizing the workflow

Edit `.github/workflows/tests.yml` to:

- Add more branches
- Change Python version
- Add additional test frameworks
- Configure different artifact retention times
- Add Slack/email notifications
- Run tests on different OS (Windows, macOS)

### Example: Run on multiple OS

```yaml
runs-on: ${{ matrix.os }}
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ["3.11", "3.12", "3.13"]
```

### Troubleshooting

**Tests fail on GitHub but pass locally:**
- Check Python version compatibility
- Verify all dependencies are in `requirements.txt`
- Ensure headless mode is compatible (most issues with UI interactions)

**Artifacts not appearing:**
- Check workflow run logs for errors
- Verify reports directory exists after test run
- Check artifact retention days (set to 30 by default)

**Slow test runs on GitHub:**
- Consider using GitHub-hosted runner cache
- Split tests into multiple parallel jobs
- Adjust timeouts in workflow (default: 30 minutes)

### Next steps

1. Push changes to trigger the workflow
2. Monitor the Actions tab for execution
3. Download and review test reports
4. Integrate with branch protection rules (require passing tests for merge)
5. Add status badges to README.md

---

**Generated:** May 4, 2026
**Workflow Version:** 1.0.0

