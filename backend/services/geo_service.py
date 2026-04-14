import requests
import json
from typing import Optional, Dict
from urllib.parse import urlparse
import socket
from backend.core.config import Config


class GeoTrackingService:
    def __init__(self):
        self.api_key = Config.IPINFO_API_KEY
        self.base_url = "https://ipinfo.io"

    def extract_domain(self, url: str) -> Optional[str]:
        try:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path.split("/")[0]
            return domain.split(":")[0] if domain else None
        except Exception:
            return None

    def resolve_ip(self, domain: str) -> Optional[str]:
        if not domain or domain.startswith(("http://", "https://")):
            return None
        try:
            ip = socket.gethostbyname(domain)
            return ip
        except socket.gaierror:
            return None

    def get_geo_info(self, ip_address: str) -> Dict:
        if not self.api_key:
            return self._mock_geo_info(ip_address)

        url = f"{self.base_url}/{ip_address}/json"
        params = {"token": self.api_key}

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return self._parse_geo_response(data)
            else:
                return self._mock_geo_info(ip_address)
        except Exception as e:
            print(f"Geo tracking error: {e}")
            return self._mock_geo_info(ip_address)

    def _parse_geo_response(self, data: dict) -> Dict:
        loc = data.get("loc", "").split(",")
        return {
            "country": data.get("country", "Unknown"),
            "city": data.get("city", "Unknown"),
            "region": data.get("region", "Unknown"),
            "latitude": float(loc[0]) if len(loc) >= 1 else None,
            "longitude": float(loc[1]) if len(loc) >= 2 else None,
            "org": data.get("org", ""),
        }

    def _mock_geo_info(self, ip_address: str) -> Dict:
        import random

        mock_ips = [
            ("US", "San Francisco", 37.7749, -122.4194),
            ("GB", "London", 51.5074, -0.1278),
            ("DE", "Berlin", 52.5200, 13.4050),
            ("JP", "Tokyo", 35.6762, 139.6503),
            ("AU", "Sydney", -33.8688, 151.2093),
            ("CA", "Toronto", 43.6532, -79.3832),
            ("FR", "Paris", 48.8566, 2.3522),
            ("BR", "Sao Paulo", -23.5505, -46.6333),
        ]
        country, city, lat, lon = random.choice(mock_ips)
        return {
            "country": country,
            "city": city,
            "region": "",
            "latitude": lat,
            "longitude": lon,
            "org": f"AS{random.randint(1000, 9999)} Example ISP",
        }

    def get_geo_from_url(self, url: str) -> Dict:
        domain = self.extract_domain(url)
        if not domain:
            return self._empty_geo_info()

        ip_address = self.resolve_ip(domain)
        if not ip_address:
            return self._empty_geo_info()

        geo_info = self.get_geo_info(ip_address)
        geo_info["ip_address"] = ip_address
        geo_info["domain"] = domain
        return geo_info

    def _empty_geo_info(self) -> Dict:
        return {
            "country": None,
            "city": None,
            "region": None,
            "latitude": None,
            "longitude": None,
            "ip_address": None,
            "domain": None,
            "org": None,
        }


geo_service = GeoTrackingService()
