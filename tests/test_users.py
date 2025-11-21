import pytest


class TestUsersAPI:

    @pytest.mark.smoke
    def test_get_all_users(self, api_client_instance):
        """Test getting all users - Smoke test"""
        response = api_client_instance.get('/users')

        # Validate status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        # Validate response structure
        users = response.json()
        assert isinstance(users, list), "Response should be a list"
        assert len(users) > 0, "Should have at least one user"

        # Validate first user structure
        first_user = users[0]
        assert 'id' in first_user, "User should have id"
        assert 'name' in first_user, "User should have name"
        assert 'email' in first_user, "User should have email"

    @pytest.mark.sanity
    def test_get_single_user(self, api_client_instance):
        """Test getting a single user - Sanity test"""
        user_id = 1
        response = api_client_instance.get(f'/users/{user_id}')

        # Validate status code
        assert response.status_code == 200

        # Validate response data
        user = response.json()
        assert user['id'] == user_id
        assert 'name' in user
        assert 'email' in user
        assert 'phone' in user

    @pytest.mark.sanity
    def test_create_user(self, api_client_instance, test_user_data):
        """Test creating a new user - Sanity test"""
        response = api_client_instance.post('/users', json_data=test_user_data)

        # Validate status code
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

        # Validate response data
        created_user = response.json()
        assert created_user['name'] == test_user_data['name']
        assert created_user['email'] == test_user_data['email']
        assert 'id' in created_user, "Created user should have an ID"

    @pytest.mark.regression
    def test_user_not_found(self, api_client_instance):
        """Test getting non-existent user - Regression test"""
        response = api_client_instance.get('/users/999999')

        # Should return 404 for not found
        assert response.status_code == 404

    @pytest.mark.parametrize("user_id", [1, 2, 3])
    def test_get_multiple_users(self, api_client_instance, user_id):
        """Test getting multiple users with parameterized tests"""
        response = api_client_instance.get(f'/users/{user_id}')
        assert response.status_code == 200
        assert response.json()['id'] == user_id

    def test_user_response_validation(self, api_client_instance):
        """Test comprehensive user response validation"""
        response = api_client_instance.get('/users/1')
        user = response.json()

        # Validate all required fields exist
        required_fields = ['id', 'name', 'username', 'email', 'address', 'phone', 'website', 'company']
        for field in required_fields:
            assert field in user, f"Required field '{field}' missing from user response"

        # Validate data types
        assert isinstance(user['id'], int)
        assert isinstance(user['name'], str)
        assert isinstance(user['email'], str)