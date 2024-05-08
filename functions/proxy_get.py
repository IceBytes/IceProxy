import requests
from bs4 import BeautifulSoup
from typing import *

class ProxyGet():
    def __init__(self, ptype: str) -> None:
        """
        Get Proxy.

        Args:
            ptype: The proxy type [http, https].

        """
        self.ptype: str = ptype

    def _send_request(self, endpoint: str, params: Optional[Dict[str, str]] = None) -> str:
        """
        Send a request to the API endpoint.

        Args:
            endpoint: The API endpoint to send the request to.
            params: (Optional) A dictionary containing the request parameters.

        Returns:
            A dictionary containing the API response.
        """
        req: str = requests.get(f"{endpoint}", params=params, timeout=10)
        return req.text
    
    def get_proxyscrape(self, timeout: Optional[int] = 10000, country: Optional[str] = "all") -> list:
        """
        Get proxies from ProxyScrape.

        Args:
            timeout: (Optional) proxies timeout.
            country: (Optional) Country code.

        Returns:
            A dictionary containing proxies.
        """
        req = self._send_request("https://api.proxyscrape.com/v2/", params={"request": "displayproxies", "protocol": self.ptype, "timeout": str(timeout), "country": country, "ssl": "all", "anonymity": "all"})
        soup = BeautifulSoup(req, 'html.parser')
        proxies = soup.get_text().split('\r\n')
        return proxies
