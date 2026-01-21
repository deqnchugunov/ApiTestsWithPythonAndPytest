import pytest


class TestPostsAPI:

    @pytest.mark.smoke
    def test_get_all_posts(self, api_client_instance):
        """Test getting all posts"""
        # Send GET request to retrieve all posts from the /posts endpoint
        response = api_client_instance.get('/posts')

        # Verify the HTTP status code is 200 (OK) - successful response
        assert response.status_code == 200

        # Parse the JSON response into a Python object (list of posts)
        posts = response.json()

        # Confirm the response is a list data structure
        assert isinstance(posts, list)

        # Ensure there is at least one post in the response
        assert len(posts) > 0

    @pytest.mark.sanity
    def test_get_single_post(self, api_client_instance):
        """Test getting a single post"""
        # Define the post ID we want to retrieve
        post_id = 1

        # Send GET request to retrieve specific post from the /posts/{id} endpoint
        response = api_client_instance.get(f'/posts/{post_id}')

        # Verify the HTTP status code is 200 (OK) - successful response
        assert response.status_code == 200

        # Parse the JSON response into a Python object (single post)
        post = response.json()

        # Verify the returned post has the correct ID
        assert post['id'] == post_id

        # Check that the post contains the required 'title' field
        assert 'title' in post

        # Check that the post contains the required 'body' field
        assert 'body' in post

        # Check that the post contains the required 'userId' field
        assert 'userId' in post

    @pytest.mark.sanity
    def test_create_post(self, api_client_instance, test_post_data):
        """Test creating a new post"""
        # Send POST request to create a new post with the provided test data
        response = api_client_instance.post('/posts', json_data=test_post_data)

        # Verify the HTTP status code is 201 (Created) - successful creation
        assert response.status_code == 201

        # Parse the JSON response into a Python object (created post)
        created_post = response.json()

        # Verify the created post has the correct title as provided in test data
        assert created_post['title'] == test_post_data['title']

        # Verify the created post has the correct body as provided in test data
        assert created_post['body'] == test_post_data['body']

        # Verify the created post has the correct userId as provided in test data
        assert created_post['userId'] == test_post_data['userId']

        # Verify the created post has an ID assigned by the server
        assert 'id' in created_post

    @pytest.mark.regression
    def test_post_not_found(self, api_client_instance):
        """Test getting non-existent post"""
        # Send GET request to retrieve a non-existent post with ID 99999
        response = api_client_instance.get('/posts/99999')

        # Verify the HTTP status code is 404 (Not Found) - resource doesn't exist
        assert response.status_code == 404

    @pytest.mark.sanity
    def test_post_response_structure(self, api_client_instance):
        """Test post response structure validation"""
        # Send GET request to retrieve the first post from the /posts endpoint
        response = api_client_instance.get('/posts/1')

        # Parse the JSON response into a Python object (single post)
        post = response.json()

        # Define the list of required fields that must be present in the post
        required_fields = ['id', 'title', 'body', 'userId']

        # Iterate through each required field and verify it exists in the post
        for field in required_fields:
            assert field in post, f"Missing required field: {field}"

        # Verify that the 'id' field is an integer type
        assert isinstance(post['id'], int)

        # Verify that the 'title' field is a string type
        assert isinstance(post['title'], str)

        # Verify that the 'body' field is a string type
        assert isinstance(post['body'], str)

        # Verify that the 'userId' field is an integer type
        assert isinstance(post['userId'], int)