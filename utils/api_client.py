import requests
from typing import Dict, Any, Optional
from config.settings import BASE_URL, DEFAULT_HEADERS, DEFAULT_TIMEOUT


class APIClient:
    def __init__(self, base_url: str = BASE_URL, headers: Optional[Dict] = None):
        self.base_url = base_url.rstrip('/')
        self.headers = headers or DEFAULT_HEADERS.copy()
        self.timeout = DEFAULT_TIMEOUT
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with proper error handling"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Add timeout to kwargs
        kwargs.setdefault('timeout', self.timeout)

        try:
            response = self.session.request(method, url, **kwargs)
            #response.raise_for_status()  # Raise exception for bad status codes
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise

    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """GET request"""
        return self._make_request('GET', endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None) -> requests.Response:
        """POST request"""
        if json_data:
            return self._make_request('POST', endpoint, json=json_data)
        elif data:
            return self._make_request('POST', endpoint, data=data)
        else:
            return self._make_request('POST', endpoint)

    def put(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None) -> requests.Response:
        """PUT request"""
        if json_data:
            return self._make_request('PUT', endpoint, json=json_data)
        elif data:
            return self._make_request('PUT', endpoint, data=data)
        else:
            return self._make_request('PUT', endpoint)

    def delete(self, endpoint: str) -> requests.Response:
        """DELETE request"""
        return self._make_request('DELETE', endpoint)

    def get_json(self, endpoint: str, params: Optional[Dict] = None) -> Dict[Any, Any]:
        """GET request returning JSON data"""
        response = self.get(endpoint, params=params)
        return response.json()

    def post_json(self, endpoint: str, data: Dict) -> Dict[Any, Any]:
        """POST request returning JSON data"""
        response = self.post(endpoint, json_data=data)
        return response.json()

    def close(self):
        """Close the session"""
        self.session.close()


# Global client instance
api_client = APIClient()