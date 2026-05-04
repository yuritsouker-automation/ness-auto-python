import pytest


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the application under test."""
    return "https://www.demoblaze.com/"

