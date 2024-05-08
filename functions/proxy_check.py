import requests
import socket
from typing import *
import time

class ProxyCheck():
    def _send_request(self, endpoint: str, proxy: Dict[str, str], timeout: Optional[int] = 20, params: Optional[Dict[str, str]] = None) -> str:
        """
        Send a request to the API endpoint.

        Args:
            endpoint: The API endpoint to send the request to.
            proxy: Http proxy.
            timeout: (Optional) Proxy timeout.
            params: (Optional) A dictionary containing the request parameters.

        Returns:
            A dictionary containing the API response.
        """
        req: str = requests.get(
            f"{endpoint}",
            params=params,
            proxies={
                "http": f"http://{proxy}"
            },
            timeout=timeout
        )
        return req
    
    def check_http(self, url: str, proxy: str, timeout: Optional[int] = 20) -> Dict[str, str]:
        """
        Check Proxies protocol http.

        Args:
            url: Site domain to check proxies.
            proxy: proxy (ip:port).
            timeout: (Optional) proxies timeout.

        Returns:
            A dictionary containing proxies.
        """
        try:
            response = self._send_request(
                f"http://{url}",
                proxy=proxy,
                timeout=timeout
            )
            return self.get_http_type(url, proxy=proxy, timeout=timeout)
        except Exception as e: print(e); return False
    
    def get_http_type(self, url: str, proxy: str, timeout: Optional[int] = 20) -> Dict[str, str]:
        """
        Get proxies type.

        Args:
            url: Site domain to check proxies.
            proxy: proxy (ip:port).
            timeout: (Optional) proxies timeout.

        Returns:
            A dictionary containing result.
        """
        try:
            proxy_host, proxy_port = proxy.split(":")
            start_time = time.time()
            with socket.create_connection((proxy_host, int(proxy_port)), timeout=timeout) as s:
                s.sendall(f'CONNECT www.{url}:443 HTTP/1.1\r\n\r\n'.encode())
                response = s.recv(1024).decode()
                connection_time = time.time() - start_time
                if '200' in response: ssl = True
                else: ssl = False

                return {
                    "proxy": proxy,
                    "status": True,
                    "protocol": "http",
                    "ssl": ssl,
                    "speed": connection_time
                    }
                
        except Exception as e: print(e); return False

    def get_proxy_info(self, proxy: str) -> Dict[str, Any]:
        try:
            response = self._send_request(
                "http://ipwho.is/",
                proxy=proxy
            ).json()
            return response
        except Exception as e:
            print(e)
            return {
                "country_code": "Unknown",
                "flag": {
                    "emoji": "Unknown"
                }
            }
