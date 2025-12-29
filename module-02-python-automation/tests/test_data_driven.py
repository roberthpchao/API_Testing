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