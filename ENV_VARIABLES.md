# Environment Variables

## Overview

The project uses environment variables to configure test environments. All URLs and credentials can be overridden via environment variables.

## Available Variables

### `HOME_URL`
- **Description:** Base URL for the application under test
- **Default:** `https://www.demoblaze.com/`
- **Usage:** Override to test against staging, local, or alternative environments

**Example:**
```bash
# Test against staging environment
export HOME_URL=https://staging.demoblaze.com/
python -m pytest tests

# Or inline
HOME_URL=https://local.demoblaze.com:8000/ python -m pytest tests
```

## Setting Environment Variables

### Option 1: Export in terminal (session-wide)
```bash
export HOME_URL=https://staging.demoblaze.com/
python -m pytest tests
```

### Option 2: Inline with command
```bash
HOME_URL=https://local.demoblaze.com:8000/ python -m pytest tests
```

### Option 3: Create `.env` file (recommended for local development)

1. Copy `.env.example` to `.env.local`:
   ```bash
   cp .env.example .env.local
   ```

2. Edit `.env.local` with your values:
   ```
   HOME_URL=https://local.demoblaze.com:8000/
   ```

3. Load variables before running tests:
   ```bash
   # Using python-dotenv (if installed)
   set -a
   source .env.local
   set +a
   python -m pytest tests
   ```

### Option 4: GitHub Actions secrets

For CI/CD, define secrets in your GitHub repository:

1. Go to **Settings** > **Secrets and variables** > **Actions**
2. Click **New repository secret**
3. Add secret: `HOME_URL` with your staging URL

4. Update `.github/workflows/tests.yml`:
   ```yaml
   - name: Run tests
     env:
       HOME_URL: ${{ secrets.HOME_URL }}
     run: python -m pytest tests
   ```

## Configuration by Environment

### Local Development
```bash
HOME_URL=http://localhost:8000/ python -m pytest tests
```

### Staging
```bash
HOME_URL=https://staging.demoblaze.com/ python -m pytest tests
```

### Production (read-only, not recommended for tests)
```bash
HOME_URL=https://www.demoblaze.com/ python -m pytest tests
```

## Variables Used in Code

| Variable | File | Usage |
|---|---|---|
| `HOME_URL` | `pages/home_page.py` | HomePage.URL |
| `HOME_URL` | `pages/login_page.py` | LoginPage.URL |
| `HOME_URL` | `pages/cart_page.py` | CartPage.HOME_URL |
| `HOME_URL` | `fixtures/conftest.py` | BASE_URL fixture |

## Best Practices

1. **Never commit `.env` files** — add to `.gitignore`
2. **Use `.env.example`** — as template for team
3. **Document environment-specific URLs** — in team docs
4. **Use secrets for CI/CD** — never commit sensitive URLs
5. **Test locally first** — before pushing to CI

## Troubleshooting

**"Home page not loading"**
- Verify `HOME_URL` is accessible
- Check network/firewall rules
- Ensure URL ends without trailing slash (or with it consistently)

**"Environment variable not recognized"**
- Verify you exported it: `echo $HOME_URL`
- Check shell syntax (bash vs zsh vs fish)
- For `.env` files, ensure you sourced them: `source .env.local`

**"Different behavior on CI vs local"**
- Check GitHub Actions secrets match local `HOME_URL`
- Verify `.github/workflows/tests.yml` env section
- Test with exact same `HOME_URL` locally

---

**Last Updated:** May 4, 2026

