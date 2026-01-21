import pytest


class TestAlbumsAPI:

    @pytest.mark.smoke
    def test_get_all_albums(self, api_client_instance):
        """Test getting all albums - Smoke test"""
        # Send GET request to retrieve all albums from the /albums endpoint
        response = api_client_instance.get('/albums')

        # Verify the HTTP status code is 200 (OK) - successful response
        assert response.status_code == 200
        
        # Parse the JSON response into a Python object (list of albums)
        albums = response.json()
        
        # Confirm the response is a list data structure
        assert isinstance(albums, list)
        
        # Ensure there is at least one album in the response
        assert len(albums) > 0

    @pytest.mark.sanity
    def test_get_single_album(self, api_client_instance):
        """Test getting a single album - Sanity test"""
        # Define the album ID we want to retrieve
        album_id = 1
        
        # Send GET request to retrieve specific album from the /albums/{id} endpoint
        response = api_client_instance.get(f'/albums/{album_id}')

        # Verify the HTTP status code is 200 (OK) - successful response
        assert response.status_code == 200
        
        # Parse the JSON response into a Python object (single album)
        album = response.json()
        
        # Verify the returned album has the correct ID
        assert album['id'] == album_id
        
        # Check that the album contains the required 'userId' field
        assert 'userId' in album
        
        # Check that the album contains the required 'title' field
        assert 'title' in album

    @pytest.mark.sanity
    def test_get_albums_by_user(self, api_client_instance):
        """Test getting albums for a specific user - Sanity test"""
        # Define the user ID for which we want to retrieve albums
        user_id = 1
        
        # Send GET request to retrieve albums for the specified user
        response = api_client_instance.get(f'/users/{user_id}/albums')

        # Verify the HTTP status code is 200 (OK) - successful response
        assert response.status_code == 200
        
        # Parse the JSON response into a Python object (list of albums)
        albums = response.json()
        
        # Confirm the response is a list data structure
        assert isinstance(albums, list)
        
        # Verify that all albums belong to the specified user
        for album in albums:
            assert album['userId'] == user_id, f"Album {album['id']} does not belong to user {user_id}"

    @pytest.mark.sanity
    def test_create_album(self, api_client_instance, test_album_data):
        """Test creating a new album - Sanity test"""
        # Send POST request to create a new album with the provided test data
        response = api_client_instance.post('/albums', json_data=test_album_data)

        # Verify the HTTP status code is 201 (Created) - successful creation
        assert response.status_code == 201
        
        # Parse the JSON response into a Python object (created album)
        created_album = response.json()
        
        # Verify the created album has the correct title as provided in test data
        assert created_album['title'] == test_album_data['title']
        
        # Verify the created album has the correct userId as provided in test data
        assert created_album['userId'] == test_album_data['userId']
        
        # Verify the created album has an ID assigned by the server
        assert 'id' in created_album

    @pytest.mark.regression
    def test_album_not_found(self, api_client_instance):
        """Test getting non-existent album - Regression test"""
        # Send GET request to retrieve a non-existent album with ID 99999
        response = api_client_instance.get('/albums/99999')
        
        # Verify the HTTP status code is 404 (Not Found) - resource doesn't exist
        assert response.status_code == 404

    @pytest.mark.parametrize("album_id", [1, 2, 3])
    def test_get_multiple_albums(self, api_client_instance, album_id):
        """Test getting multiple albums with parameterized tests"""
        # Send GET request to retrieve specific album by ID
        response = api_client_instance.get(f'/albums/{album_id}')
        
        # Verify the HTTP status code is 200 (OK) - successful response
        assert response.status_code == 200
        
        # Verify the returned album has the correct ID
        assert response.json()['id'] == album_id

    def test_album_response_validation(self, api_client_instance):
        """Test comprehensive album response validation"""
        # Send GET request to retrieve the first album
        response = api_client_instance.get('/albums/1')
        
        # Parse the JSON response into a Python object (single album)
        album = response.json()

        # Validate all required fields exist
        required_fields = ['id', 'userId', 'title']
        for field in required_fields:
            assert field in album, f"Required field '{field}' missing from album response"

        # Validate data types
        assert isinstance(album['id'], int)
        assert isinstance(album['userId'], int)
        assert isinstance(album['title'], str)

    @pytest.mark.sanity
    def test_album_creation_with_invalid_data(self, api_client_instance):
        """Test creating album with invalid data - Sanity test"""
        # Create invalid album data with missing required fields
        invalid_album_data = {
            'userId': 1,
            # Missing required 'title' field
        }
        
        # Send POST request to create album with invalid data
        response = api_client_instance.post('/albums', json_data=invalid_album_data)

        # Depending on API implementation, this might return 400 or 201
        # We're just ensuring it doesn't crash
        assert response.status_code in [400, 201], f"Unexpected status code: {response.status_code}"