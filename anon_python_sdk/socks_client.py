import requests
from requests.exceptions import RequestException


class SocksClient:
    """
    A SOCKS client for making HTTP requests through the Anon network.
    """

    def __init__(self, proxy_host: str = "127.0.0.1", proxy_port: int = 9050):
        """
        Initializes the SOCKS client.
        Args:
            proxy_host (str): The host address of the SOCKS proxy (default: 127.0.0.1).
            proxy_port (int): The port number of the SOCKS proxy (default: 9050).
        """
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxies = {
            "http": f"socks5h://{proxy_host}:{proxy_port}",
            "https": f"socks5h://{proxy_host}:{proxy_port}",
        }

    def get(self, url: str, **kwargs):
        """
        Sends a GET request through the Anon network.
        Args:
            url (str): The URL to request.
            **kwargs: Additional parameters for the `requests.get` method.
        Returns:
            Response: The HTTP response object.
        """
        return self._request("get", url, **kwargs)

    def post(self, url: str, data=None, json=None, **kwargs):
        """
        Sends a POST request through the Anon network.
        Args:
            url (str): The URL to request.
            data: Form data to send in the POST request.
            json: JSON data to send in the POST request.
            **kwargs: Additional parameters for the `requests.post` method.
        Returns:
            Response: The HTTP response object.
        """
        return self._request("post", url, data=data, json=json, **kwargs)

    def put(self, url: str, data=None, **kwargs):
        """
        Sends a PUT request through the Anon network.
        Args:
            url (str): The URL to request.
            data: Data to send in the PUT request.
            **kwargs: Additional parameters for the `requests.put` method.
        Returns:
            Response: The HTTP response object.
        """
        return self._request("put", url, data=data, **kwargs)

    def delete(self, url: str, **kwargs):
        """
        Sends a DELETE request through the Anon network.
        Args:
            url (str): The URL to request.
            **kwargs: Additional parameters for the `requests.delete` method.
        Returns:
            Response: The HTTP response object.
        """
        return self._request("delete", url, **kwargs)

    def head(self, url: str, **kwargs):
        """
        Sends a HEAD request through the Anon network.
        Args:
            url (str): The URL to request.
            **kwargs: Additional parameters for the `requests.head` method.
        Returns:
            Response: The HTTP response object.
        """
        return self._request("head", url, **kwargs)

    def patch(self, url: str, data=None, **kwargs):
        """
        Sends a PATCH request through the Anon network.
        Args:
            url (str): The URL to request.
            data: Data to send in the PATCH request.
            **kwargs: Additional parameters for the `requests.patch` method.
        Returns:
            Response: The HTTP response object.
        """
        return self._request("patch", url, data=data, **kwargs)

    def options(self, url: str, **kwargs):
        """
        Sends an OPTIONS request through the Anon network.
        Args:
            url (str): The URL to request.
            **kwargs: Additional parameters for the `requests.options` method.
        Returns:
            Response: The HTTP response object.
        """
        return self._request("options", url, **kwargs)

    def _request(self, method: str, url: str, **kwargs):
        """
        Internal method to send HTTP requests through the Anon network.
        Args:
            method (str): HTTP method (e.g., 'get', 'post').
            url (str): The URL to request.
            **kwargs: Additional parameters for the `requests` method.
        Returns:
            Response: The HTTP response object.
        """
        try:
            request_method = getattr(requests, method)
            response = request_method(url, proxies=self.proxies, **kwargs)
            response.raise_for_status()
            return response
        except RequestException as e:
            raise RuntimeError(f"Error making {method.upper()} request through Anon: {e}")