import pytest


class TestCommentsAPI:

    @pytest.mark.smoke
    def test_get_all_comments(self, api_client_instance):
        """Test getting all comments - Smoke test"""
        response = api_client_instance.get('/comments')

        # Validate status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        # Validate response structure
        comments = response.json()
        assert isinstance(comments, list), "Response should be a list"
        assert len(comments) > 0, "Should have at least one comment"

        # Validate first comment structure
        first_comment = comments[0]
        assert 'id' in first_comment, "Comment should have id"
        assert 'postId' in first_comment, "Comment should have postId"
        assert 'name' in first_comment, "Comment should have name"
        assert 'email' in first_comment, "Comment should have email"
        assert 'body' in first_comment, "Comment should have body"

    @pytest.mark.sanity
    def test_get_comments_by_post(self, api_client_instance):
        """Test getting comments for a specific post - Sanity test"""
        post_id = 1
        response = api_client_instance.get(f'/posts/{post_id}/comments')

        # Validate status code
        assert response.status_code == 200

        # Validate response data
        comments = response.json()
        assert isinstance(comments, list), "Response should be a list"
        
        # All comments should belong to the same post
        for comment in comments:
            assert comment['postId'] == post_id, f"Comment {comment['id']} does not belong to post {post_id}"

    @pytest.mark.sanity
    def test_get_single_comment(self, api_client_instance):
        """Test getting a single comment - Sanity test"""
        comment_id = 1
        response = api_client_instance.get(f'/comments/{comment_id}')

        # Validate status code
        assert response.status_code == 200

        # Validate response data
        comment = response.json()
        assert comment['id'] == comment_id
        assert 'postId' in comment
        assert 'name' in comment
        assert 'email' in comment
        assert 'body' in comment

    @pytest.mark.sanity
    def test_create_comment(self, api_client_instance, test_comment_data):
        """Test creating a new comment - Sanity test"""
        response = api_client_instance.post('/comments', json_data=test_comment_data)

        # Validate status code
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

        # Validate response data
        created_comment = response.json()
        assert created_comment['postId'] == test_comment_data['postId']
        assert created_comment['name'] == test_comment_data['name']
        assert created_comment['email'] == test_comment_data['email']
        assert created_comment['body'] == test_comment_data['body']
        assert 'id' in created_comment, "Created comment should have an ID"

    @pytest.mark.regression
    def test_comment_not_found(self, api_client_instance):
        """Test getting non-existent comment - Regression test"""
        response = api_client_instance.get('/comments/999999')

        # Should return 404 for not found
        assert response.status_code == 404

    @pytest.mark.parametrize("comment_id", [1, 2, 3])
    def test_get_multiple_comments(self, api_client_instance, comment_id):
        """Test getting multiple comments with parameterized tests"""
        response = api_client_instance.get(f'/comments/{comment_id}')
        assert response.status_code == 200
        assert response.json()['id'] == comment_id

    def test_comment_response_validation(self, api_client_instance):
        """Test comprehensive comment response validation"""
        response = api_client_instance.get('/comments/1')
        comment = response.json()

        # Validate all required fields exist
        required_fields = ['id', 'postId', 'name', 'email', 'body']
        for field in required_fields:
            assert field in comment, f"Required field '{field}' missing from comment response"

        # Validate data types
        assert isinstance(comment['id'], int)
        assert isinstance(comment['postId'], int)
        assert isinstance(comment['name'], str)
        assert isinstance(comment['email'], str)
        assert isinstance(comment['body'], str)

    @pytest.mark.sanity
    def test_comment_creation_with_invalid_data(self, api_client_instance):
        """Test creating comment with invalid data - Sanity test"""
        invalid_comment_data = {
            'postId': 1,
            # Missing required fields
        }
        response = api_client_instance.post('/comments', json_data=invalid_comment_data)

        # Depending on API implementation, this might return 400 or 201
        # We're just ensuring it doesn't crash
        assert response.status_code in [400, 201], f"Unexpected status code: {response.status_code}"