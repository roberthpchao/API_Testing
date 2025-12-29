import pytest
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--run-slow",
        action="store_true",
        default=False,
        help="Run slow tests"
    )

def pytest_collection_modifyitems(config, items):
    """Skip slow tests unless --run-slow is specified"""
    if not config.getoption("--run-slow"):
        skip_slow = pytest.mark.skip(reason="Need --run-slow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)

@pytest.fixture
def github_token():
    """Provide GitHub token or skip tests if missing"""
    token = os.getenv("GITHUB_TOKEN")
    if not token or token.startswith("your_token"):
        pytest.skip("GitHub token not configured")
    return token