import os

# Base URL for the API
BASE_URL = os.getenv('API_BASE_URL', 'https://jsonplaceholder.typicode.com')

# Authentication tokens (if needed)
API_TOKEN = os.getenv('API_TOKEN', None)

# Timeout settings
DEFAULT_TIMEOUT = 30

# Headers
DEFAULT_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Test data
TEST_USER_DATA = {
    'name': 'John Doe',
    'username': 'johndoe',
    'email': 'john.doe@example.com'
}

TEST_POST_DATA = {
    'title': 'Test Post',
    'body': 'This is a test post body',
    'userId': 1
}