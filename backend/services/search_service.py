import requests
import json
from typing import List, Dict
from backend.core.config import Config


class SearchService:
    def __init__(self):
        self.api_key = Config.TAVILY_API_KEY
        self.base_url = "https://api.tavily.com/search"

    def search_images(self, query: str, max_results: int = None) -> List[Dict]:
        if not self.api_key:
            return self._mock_search_results(query, max_results)

        max_results = max_results or Config.MAX_SEARCH_RESULTS

        headers = {"Content-Type": "application/json"}

        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "basic",
            "max_results": max_results,
            "include_answer": False,
            "include_images": True,
            "include_raw_content": False,
        }

        try:
            response = requests.post(
                self.base_url, json=payload, headers=headers, timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                return self._extract_image_results(data, query)
            else:
                return self._mock_search_results(query, max_results)
        except Exception as e:
            print(f"Search error: {e}")
            return self._mock_search_results(query, max_results)

    def _extract_image_results(self, data: dict, query: str) -> List[Dict]:
        results = []
        images = data.get("images", [])

        for img in images:
            if isinstance(img, dict):
                results.append(
                    {
                        "url": img.get("url", ""),
                        "image_url": img.get("image_url", ""),
                        "title": img.get("title", query),
                        "score": img.get("score", 0.8),
                    }
                )

        for result in data.get("results", [])[:5]:
            if result.get("images"):
                for img in result.get("images", [])[:2]:
                    results.append(
                        {
                            "url": result.get("url", ""),
                            "image_url": img,
                            "title": result.get("title", query),
                            "score": result.get("score", 0.7),
                        }
                    )

        return results[: Config.MAX_SEARCH_RESULTS]

    def _mock_search_results(self, query: str, max_results: int) -> List[Dict]:
        return [
            {
                "url": f"https://example{i}.com/article/{query.replace(' ', '-')}",
                "image_url": f"https://picsum.photos/seed/{i + 1}/800/600",
                "title": f"Sample Image {i + 1} - {query}",
                "score": 0.9 - (i * 0.05),
            }
            for i in range(min(max_results, 5))
        ]


search_service = SearchService()
