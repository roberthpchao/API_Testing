# Module 2: Python API Automation (module-02-python-automation/README.md)
```
    markdown
# Module 2: Python API Automation

## 🎯 Module Objectives
- Transition from Postman to Python automation
- Build maintainable test frameworks
- Implement data-driven testing patterns
- Generate professional test reports

## 📋 Prerequisites
- Complete [Module 1: Postman Mastery](../module-01-postman-mastery/)
- Python 3.8+ installed
- VS Code with Python extension
- GitHub Personal Access Token (from Module 1)

---

## 🚀 Exercise 1: Setting Up Your Python Test Environment

### Step 1: Project Structure Setup
Your `module-02-python-automation/` folder should look like this:
```
```
module-02-python-automation/
├── README.md # This file
├── tests/
│ ├── init.py
│ ├── test_github_api.py # Main test file
│ ├── test_data_driven.py # Data-driven tests
│ └── conftest.py # Shared fixtures
├── utilities/
│ ├── init.py
│ ├── api_client.py # Reusable API client
│ ├── helpers.py helper functions
│ └── validators.py # Validation utilities
├── data/
│ ├── test_users.json # Test data
│ └── schemas/ # JSON schemas
├── reports/ # Generated reports
└── requirements.txt # Module dependencies
```
text

### Step 2: Create the Utilities

**Create `utilities/api_client.py`:**
```python
import os
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class GitHubAPIClient:
    """Reusable client for GitHub API interactions"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or "https://api.github.com"
        self.token = os.getenv("GITHUB_TOKEN")
        
        if not self.token:
            logger.warning("GITHUB_TOKEN not found in .env file")
            
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Python-API-Testing-Course"
        }
        
        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Generic request handler with logging and error handling"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"{method.upper()} {url}")
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
    
    def get_user(self, username: str) -> Dict[str, Any]:
        """Get user profile information"""
        response = self._make_request("GET", f"/users/{username}")
        return response.json()
    
    def get_user_repos(self, username: str, per_page: int = 10) -> Dict[str, Any]:
        """Get user repositories with pagination"""
        params = {"per_page": per_page, "sort": "updated"}
        response = self._make_request("GET", f"/users/{username}/repos", params=params)
        return response.json()
    
    def create_gist(self, description: str, content: str, public: bool = False) -> Dict[str, Any]:
        """Create a new gist"""
        payload = {
            "description": description,
            "public": public,
            "files": {
                "test_file.txt": {
                    "content": content
                }
            }
        }
        response = self._make_request("POST", "/gists", json=payload)
        return response.json()
    
    def delete_gist(self, gist_id: str) -> int:
        """Delete a gist by ID"""
        response = self._make_request("DELETE", f"/gists/{gist_id}")
        return response.status_code
    
    def search_repositories(self, query: str, per_page: int = 5) -> Dict[str, Any]:
        """Search GitHub repositories"""
        params = {"q": query, "per_page": per_page}
        response = self._make_request("GET", "/search/repositories", params=params)
        return response.json()
    
    def get_rate_limit(self) -> Dict[str, Any]:
        """Check API rate limits"""
        response = self._make_request("GET", "/rate_limit")
        return response.json()      
```
#### Create utilities/helpers.py:
```python
import json
import time
from typing import Any, Dict
from datetime import datetime

def load_test_data(file_path: str) -> Any:
    """Load test data from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_response(response_data: Dict, filename: str) -> None:
    """Save API response to file for debugging"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename}_{timestamp}.json"
    
    with open(f"debug/{filename}", 'w', encoding='utf-8') as file:
        json.dump(response_data, file, indent=2)

def validate_response_time(response, max_time_ms: int = 1000) -> bool:
    """Validate response time meets requirements"""
    return response.elapsed.total_seconds() * 1000 <= max_time_ms

def generate_test_description(test_name: str, **kwargs) -> str:
    """Generate dynamic test descriptions"""
    if kwargs:
        params = ', '.join(f"{k}={v}" for k, v in kwargs.items())
        return f"{test_name} [{params}]"
    return test_name
```
### Step 3: Create Your First Python Tests
Create tests/test_github_api.py:
```python
import pytest
import time
from utilities.api_client import GitHubAPIClient
from utilities.helpers import validate_response_time

class TestGitHubAPI:
    """Test suite for GitHub API using Python"""
    
    @pytest.fixture(scope="class")
    def api_client(self):
        """Create API client instance for all tests"""
        return GitHubAPIClient()
    
    @pytest.fixture
    def test_gist(self, api_client):
        """Create a test gist and clean up after test"""
        # Setup: Create gist
        gist = api_client.create_gist(
            description="Test gist for automated tests",
            content=f"This gist was created at {time.time()}",
            public=False
        )
        
        gist_id = gist["id"]
        yield gist  # Provide gist to test
        
        # Teardown: Delete gist
        try:
            api_client.delete_gist(gist_id)
            print(f"✓ Cleaned up gist: {gist_id}")
        except Exception as e:
            print(f"⚠️ Failed to delete gist {gist_id}: {e}")
    
    # ===== BASIC TESTS =====
    
    def test_get_user_profile(self, api_client):
        """Test fetching a user profile"""
        # Act
        user_data = api_client.get_user("octocat")
        
        # Assert
        assert user_data["login"] == "octocat"
        assert isinstance(user_data["id"], int)
        assert "avatar_url" in user_data
        assert user_data["type"] in ["User", "Organization"]
        assert user_data["public_repos"] >= 0
    
    def test_get_user_profile_response_time(self, api_client):
        """Test response time performance"""
        response = api_client._make_request("GET", "/users/octocat")
        assert validate_response_time(response, 500), \
            f"Response time {response.elapsed.total_seconds()*1000:.0f}ms exceeds 500ms limit"
    
    def test_get_nonexistent_user(self, api_client):
        """Test error handling for non-existent user"""
        try:
            api_client.get_user("nonexistentuser123456789")
            pytest.fail("Expected an exception for non-existent user")
        except Exception as e:
            # Should get 404
            assert "404" in str(e)
    
    # ===== GIST TESTS =====
    
    def test_gist_creation(self, api_client, test_gist):
        """Test creating a gist"""
        # Assertions
        assert "id" in test_gist
        assert test_gist["description"] == "Test gist for automated tests"
        assert test_gist["public"] is False
        assert "test_file.txt" in test_gist["files"]
        
        # Verify file content
        file_content = test_gist["files"]["test_file.txt"]["content"]
        assert "This gist was created at" in file_content
    
    def test_gist_deletion(self, api_client):
        """Test full create-delete lifecycle"""
        # Create
        gist = api_client.create_gist(
            description="Temporary test gist",
            content="Content to be deleted",
            public=False
        )
        
        gist_id = gist["id"]
        assert gist_id is not None
        
        # Delete
        status_code = api_client.delete_gist(gist_id)
        assert status_code == 204, f"Expected 204, got {status_code}"
    
    # ===== SEARCH TESTS =====
    
    def test_search_repositories(self, api_client):
        """Test repository search functionality"""
        results = api_client.search_repositories("python testing", per_page=3)
        
        assert "items" in results
        assert "total_count" in results
        assert len(results["items"]) <= 3
        
        if results["items"]:
            repo = results["items"][0]
            assert "name" in repo
            assert "html_url" in repo
            assert "stargazers_count" in repo
    
    def test_rate_limit(self, api_client):
        """Test rate limit endpoint"""
        rate_data = api_client.get_rate_limit()
        
        assert "resources" in rate_data
        assert "core" in rate_data["resources"]
        assert "remaining" in rate_data["resources"]["core"]
        assert "limit" in rate_data["resources"]["core"]
        
        # Should have some requests remaining
        assert rate_data["resources"]["core"]["remaining"] > 0
    
    # ===== DATA VALIDATION TESTS =====
    
    @pytest.mark.parametrize("username,expected_type", [
        ("octocat", "User"),
        ("github", "Organization"),
        ("microsoft", "Organization"),
    ])
    def test_user_types(self, api_client, username, expected_type):
        """Parameterized test for different user types"""
        user_data = api_client.get_user(username)
        assert user_data["type"] == expected_type, \
            f"{username} should be {expected_type}, got {user_data['type']}"
```
### Step 4: Create Configuration File
Create tests/conftest.py:

```python
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
```
### Step 5: Create Test Data
Create data/test_users.json:

```json
{
  "valid_users": [
    {
      "username": "octocat",
      "expected_type": "User",
      "description": "GitHub mascot"
    },
    {
      "username": "github",
      "expected_type": "Organization",
      "description": "GitHub organization"
    },
    {
      "username": "defunkt",
      "expected_type": "User",
      "description": "GitHub founder"
    }
  ],
  "invalid_users": [
    {
      "username": "nonexistentuser123456789",
      "expected_error": "404"
    },
    {
      "username": "",
      "expected_error": "404"
    }
  ]
}
```
### Step 6: Run Your Tests
```bash
# Navigate to your project
cd C:\Users\Admin\Documents\Projects\API_Testing\module-02-python-automation

# Install module-specific dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_github_api.py -v

# Run with HTML report
pytest tests/ --html=reports/report.html --self-contained-html

# Run tests in parallel (faster)
pytest tests/ -n 2

# Run with custom marker
pytest tests/ -m "not slow"
```
### Step 7: Create Module Requirements
Create requirements.txt in module folder:

```txt
# Test Framework
pytest==7.4.3
pytest-html==4.1.1
pytest-xdist==3.5.0
pytest-rerunfailures==14.0

# API & HTTP
requests==2.31.0
httpx==0.25.2

# Data Validation
jsonschema==4.20.0
pydantic==2.5.0

# Utilities
python-dotenv==1.0.0
Faker==20.1.0
allure-pytest==2.13.2

# Reporting
pytest-html==4.1.1
pytest-json-report==1.5.0
```

## 🚀 Exercise 2: Data-Driven Testing
Create tests/test_data_driven.py:

```python
import pytest
import json
from utilities.api_client import GitHubAPIClient

class TestDataDriven:
    """Data-driven testing examples"""
    
    @pytest.fixture(scope="class")
    def api_client(self):
        return GitHubAPIClient()
    
    @pytest.fixture
    def user_data(self):
        """Load test data from JSON file"""
        with open('data/test_users.json', 'r') as file:
            return json.load(file)
    
    def test_multiple_users(self, api_client, user_data):
        """Test multiple users from data file"""
        for user in user_data["valid_users"]:
            username = user["username"]
            expected_type = user["expected_type"]
            
            user_info = api_client.get_user(username)
            
            # Assertions
            assert user_info["login"].lower() == username.lower()
            assert user_info["type"] == expected_type
            assert user_info["id"] > 0
    
    @pytest.mark.parametrize("query, min_results", [
        ("python", 1),
        ("javascript", 1),
        ("docker", 1),
        ("nonexistenttech123", 0)
    ])
    def test_search_queries(self, api_client, query, min_results):
        """Parameterized search tests"""
        results = api_client.search_repositories(query, per_page=5)
        
        if min_results > 0:
            assert results["total_count"] >= min_results
            assert len(results["items"]) > 0
        else:
            # For invalid queries, we might get 0 results
            assert results["total_count"] == 0 or len(results["items"]) == 0
```            
## 🚀 Exercise 3: Advanced Patterns
Create JSON Schema Validation
Create data/schemas/user_schema.json:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GitHub User Schema",
  "type": "object",
  "properties": {
    "login": {"type": "string"},
    "id": {"type": "integer"},
    "node_id": {"type": "string"},
    "avatar_url": {"type": "string", "format": "uri"},
    "type": {"type": "string", "enum": ["User", "Organization"]},
    "name": {"type": ["string", "null"]},
    "company": {"type": ["string", "null"]},
    "blog": {"type": ["string", "null"], "format": "uri"},
    "location": {"type": ["string", "null"]},
    "email": {"type": ["string", "null"], "format": "email"},
    "hireable": {"type": ["boolean", "null"]},
    "bio": {"type": ["string", "null"]},
    "public_repos": {"type": "integer", "minimum": 0},
    "public_gists": {"type": "integer", "minimum": 0},
    "followers": {"type": "integer", "minimum": 0},
    "following": {"type": "integer", "minimum": 0},
    "created_at": {"type": "string", "format": "date-time"},
    "updated_at": {"type": "string", "format": "date-time"}
  },
  "required": ["login", "id", "node_id", "avatar_url", "type", "created_at", "updated_at"],
  "additionalProperties": true
}
```
### Update utilities/validators.py:

```python
import jsonschema
from jsonschema import validate

def validate_json_schema(data, schema):
    """Validate data against JSON schema"""
    try:
        validate(instance=data, schema=schema)
        return True, "Valid"
    except jsonschema.exceptions.ValidationError as e:
        return False, str(e)
```
✅ Module 2 Checklist
Created folder structure

Implemented GitHubAPIClient class

Created basic API tests

Added fixtures for setup/teardown

Implemented data-driven testing

Created JSON schemas for validation

Set up pytest configuration

Generated test reports

📚 Next Steps
Run the tests and ensure they pass

Experiment with different test patterns

Add more test scenarios (error cases, edge cases)

Proceed to Module 3 for advanced strategies

🔧 Troubleshooting
Issue: Token not found

Check .env file exists in project root

Ensure GITHUB_TOKEN=your_token is set

Restart VS Code terminal

Issue: Import errors

Make sure __init__.py files exist in folders

Check Python path: import sys; print(sys.path)

Issue: Rate limiting

GitHub has 60 requests/hour for unauthenticated calls

Use your token for 5000 requests/hour

Add delays between tests if needed

###Proceed to Module 3: Advanced Testing Strategies when ready.

```text

## **📁 Create These Files Now**

In your VS Code terminal:

```bash
# Navigate to Module 2 folder
cd C:\Users\Admin\Documents\Projects\API_Testing\module-02-python-automation

# Create folder structure
mkdir -p tests utilities data/schemas reports debug

# Create __init__.py files
New-Item tests/__init__.py, utilities/__init__.py, data/__init__.py

# Create the main files
# 1. Copy the README.md content above
# 2. Create utilities/api_client.py
# 3. Create tests/test_github_api.py
# 4. Create data/test_users.json
# 5. Create requirements.txt
```
🎯 Immediate Next Action
Start with Exercise 1, Step 2: Create the utilities/api_client.py file. This is your foundation for all Python API testing.