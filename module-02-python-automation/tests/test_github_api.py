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