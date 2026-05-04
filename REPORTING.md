# DemoBlaze Automation Framework - Reports

## Test Reporting

This framework includes comprehensive test reporting capabilities:

### HTML Report

After running tests, an interactive HTML report is automatically generated at:

```
reports/report.html
```

**Features:**
- ✅ Test results summary (passed, failed, skipped)
- ✅ Detailed test execution timeline
- ✅ Environment metadata
- ✅ Test duration and performance metrics
- ✅ Self-contained HTML (no external dependencies)

**View the report:**
```bash
open reports/report.html  # macOS
xdg-open reports/report.html  # Linux
start reports/report.html  # Windows
```

### Screenshots on Failure

Failed tests automatically capture screenshots stored in:

```
reports/screenshots/failure_*.png
```

### Running Tests with Reports

```bash
# Default - generates HTML report
python -m pytest

# Custom report name
python -m pytest --html=reports/custom_report.html

# Skip report generation
python -m pytest -p no:html
```

### Report Location Mapping

```
ness-auto-python/
├── reports/               # Generated test reports
│   ├── report.html       # Main HTML report
│   ├── test_summary.json # Summary for CI/CD
│   └── screenshots/      # Failure screenshots
└── ...
```

### Integration

For CI/CD pipelines, the JSON summary can be parsed:

```python
from utils.report_config import generate_summary

summary_data = {
    "total": 1,
    "passed": 1,
    "failed": 0,
    "skipped": 0
}
generate_summary(summary_data)
```

This generates `reports/test_summary.json` for downstream processing.

