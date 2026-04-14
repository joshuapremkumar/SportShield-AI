import numpy as np
import requests
from io import BytesIO
from PIL import Image
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

from backend.core.config import Config
from backend.services.clip_service import clip_service
from backend.services.search_service import search_service
from backend.services.geo_service import geo_service
from backend.services.explainability_service import explainability_service


class DetectionService:
    def __init__(self):
        self.results_dir = Config.RESULTS_DIR
        self.results_dir.mkdir(exist_ok=True)

    def detect_matches(
        self, image_id: str, search_keyword: str, top_k: int = 5
    ) -> List[Dict]:
        results = []

        query_embedding = clip_service.load_embedding(image_id)

        search_results = search_service.search_images(
            search_keyword, max_results=top_k + 5
        )

        for idx, search_result in enumerate(search_results):
            try:
                matched_image_path = self._download_image(
                    search_result.get("image_url", ""), idx
                )

                if matched_image_path is None:
                    continue

                matched_embedding = clip_service.generate_embedding(matched_image_path)

                similarity = clip_service.compute_similarity(
                    query_embedding, matched_embedding
                )

                if similarity < Config.SIMILARITY_THRESHOLD:
                    matched_image_path.unlink(missing_ok=True)
                    continue

                match_result = explainability_service.match_features(
                    str(Config.UPLOAD_DIR / f"{image_id}.png"), str(matched_image_path)
                )

                geo_info = geo_service.get_geo_from_url(search_result.get("url", ""))

                confidence = self._get_confidence(
                    similarity, match_result.get("matched_keypoints", 0)
                )

                result = {
                    "image_id": image_id,
                    "search_url": search_result.get("url", ""),
                    "domain": geo_info.get("domain"),
                    "ip_address": geo_info.get("ip_address"),
                    "country": geo_info.get("country"),
                    "city": geo_info.get("city"),
                    "latitude": geo_info.get("latitude"),
                    "longitude": geo_info.get("longitude"),
                    "similarity_score": round(similarity, 4),
                    "matched_keypoints": match_result.get("matched_keypoints", 0),
                    "confidence": confidence,
                    "annotated_image": match_result.get("annotated_image_base64"),
                    "original_image": image_id,
                    "matched_image": str(matched_image_path),
                }

                results.append(result)

                matched_image_path.unlink(missing_ok=True)

            except Exception as e:
                print(f"Error processing result {idx}: {e}")
                continue

        results = sorted(results, key=lambda x: x["similarity_score"], reverse=True)

        return results[:top_k]

    def _download_image(self, url: str, idx: int) -> Optional[Path]:
        if not url:
            return None

        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                if img.mode != "RGB":
                    img = img.convert("RGB")

                output_path = (
                    self.results_dir
                    / f"download_{idx}_{datetime.now().timestamp()}.png"
                )
                img.save(output_path)
                return output_path
        except Exception as e:
            print(f"Error downloading image from {url}: {e}")

        return None

    def _get_confidence(self, similarity: float, matched_keypoints: int) -> str:
        if similarity > 0.85 and matched_keypoints > 10:
            return "High"
        elif similarity > 0.60 and matched_keypoints > 5:
            return "Medium"
        else:
            return "Low"

    def save_results(self, image_id: str, results: List[Dict]) -> str:
        import json

        output_file = (
            self.results_dir / f"results_{image_id}_{datetime.now().timestamp()}.json"
        )

        serializable_results = []
        for r in results:
            res = r.copy()
            res.pop("annotated_image", None)
            res.pop("matched_image", None)
            serializable_results.append(res)

        with open(output_file, "w") as f:
            json.dump(
                {
                    "image_id": image_id,
                    "detection_time": datetime.now().isoformat(),
                    "results": serializable_results,
                },
                f,
                indent=2,
            )

        return str(output_file)


detection_service = DetectionService()
