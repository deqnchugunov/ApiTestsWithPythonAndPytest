import pytest
from utils.api_client import api_client
from config.settings import TEST_USER_DATA, TEST_POST_DATA

@pytest.fixture(scope="session")
def base_url():
    """Return base URL for API testing"""
    return "https://jsonplaceholder.typicode.com"

@pytest.fixture(scope="session")
def api_client_instance():
    """Return API client instance"""
    return api_client

@pytest.fixture(scope="function")
def test_user_data():
    """Return test user data"""
    return TEST_USER_DATA

@pytest.fixture(scope="function")
def test_post_data():
    """Return test post data"""
    return TEST_POST_DATA

@pytest.fixture(scope="function")
def cleanup_resources():
    """Fixture to clean up resources after tests"""
    # This fixture can be used to clean up created resources
    yield
    # Cleanup code would go here if needed