import pytest


class TestPostsAPI:

    @pytest.mark.smoke
    def test_get_all_posts(self, api_client_instance):
        """Test getting all posts"""
        response = api_client_instance.get('/posts')

        assert response.status_code == 200
        posts = response.json()
        assert isinstance(posts, list)
        assert len(posts) > 0

    @pytest.mark.sanity
    def test_get_single_post(self, api_client_instance):
        """Test getting a single post"""
        post_id = 1
        response = api_client_instance.get(f'/posts/{post_id}')

        assert response.status_code == 200
        post = response.json()
        assert post['id'] == post_id
        assert 'title' in post
        assert 'body' in post
        assert 'userId' in post

    @pytest.mark.sanity
    def test_create_post(self, api_client_instance, test_post_data):
        """Test creating a new post"""
        response = api_client_instance.post('/posts', json_data=test_post_data)

        assert response.status_code == 201
        created_post = response.json()
        assert created_post['title'] == test_post_data['title']
        assert created_post['body'] == test_post_data['body']
        assert created_post['userId'] == test_post_data['userId']
        assert 'id' in created_post

    @pytest.mark.regression
    def test_post_not_found(self, api_client_instance):
        """Test getting non-existent post"""
        response = api_client_instance.get('/posts/99999')
        assert response.status_code == 404

    @pytest.mark.sanity
    def test_post_response_structure(self, api_client_instance):
        """Test post response structure validation"""
        response = api_client_instance.get('/posts/1')
        post = response.json()

        # Required fields
        required_fields = ['id', 'title', 'body', 'userId']
        for field in required_fields:
            assert field in post, f"Missing required field: {field}"

        # Data types
        assert isinstance(post['id'], int)
        assert isinstance(post['title'], str)
        assert isinstance(post['body'], str)
        assert isinstance(post['userId'], int)