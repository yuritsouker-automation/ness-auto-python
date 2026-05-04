import os
import json


class ReportConfig:
    """Configuration for test reporting."""

    REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
    REPORT_FILE = os.path.join(REPORTS_DIR, "report.html")

    @staticmethod
    def ensure_reports_dir():
        """Ensure the reports directory exists."""
        os.makedirs(ReportConfig.REPORTS_DIR, exist_ok=True)


def generate_summary(summary_data: dict, filename: str = "test_summary.json"):
    """Generate a JSON summary of test results for CI/CD integration."""
    ReportConfig.ensure_reports_dir()
    summary_path = os.path.join(ReportConfig.REPORTS_DIR, filename)
    with open(summary_path, "w") as f:
        json.dump(summary_data, f, indent=2)
    print(f"Test summary saved to: {summary_path}")

