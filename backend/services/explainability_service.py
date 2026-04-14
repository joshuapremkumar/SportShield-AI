import cv2
import numpy as np
import base64
from PIL import Image
import io
from typing import Tuple, Optional
from pathlib import Path

from backend.core.config import Config


class ExplainabilityService:
    def __init__(self):
        self.orb = cv2.ORB_create(nfeatures=1000)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    def extract_keypoints(self, image_path: str) -> Tuple:
        img = cv2.imread(image_path)
        if img is None:
            return None, None

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        keypoints, descriptors = self.orb.detectAndCompute(gray, None)
        return keypoints, descriptors

    def match_features(self, source_path: str, target_path: str) -> dict:
        kp1, desc1 = self.extract_keypoints(source_path)
        kp2, desc2 = self.extract_keypoints(target_path)

        if desc1 is None or desc2 is None:
            return {
                "matched_keypoints": 0,
                "total_keypoints_source": 0,
                "total_keypoints_target": 0,
                "match_ratio": 0.0,
                "annotated_image_base64": None,
            }

        if len(kp1) < 2 or len(kp2) < 2:
            return {
                "matched_keypoints": 0,
                "total_keypoints_source": len(kp1),
                "total_keypoints_target": len(kp2),
                "match_ratio": 0.0,
                "annotated_image_base64": None,
            }

        matches = self.bf.match(desc1, desc2)
        matches = sorted(matches, key=lambda x: x.distance)

        good_matches = [m for m in matches if m.distance < 50]

        match_ratio = len(good_matches) / max(len(kp1), len(kp2), 1)

        annotated = self._create_annotated_image(
            source_path, target_path, kp1, kp2, good_matches
        )

        return {
            "matched_keypoints": len(good_matches),
            "total_keypoints_source": len(kp1),
            "total_keypoints_target": len(kp2),
            "match_ratio": match_ratio,
            "annotated_image_base64": annotated,
        }

    def _create_annotated_image(
        self, source_path: str, target_path: str, kp1: list, kp2: list, matches: list
    ) -> Optional[str]:
        try:
            img1 = cv2.imread(source_path)
            img2 = cv2.imread(target_path)

            if img1 is None or img2 is None:
                return None

            h1, w1 = img1.shape[:2]
            h2, w2 = img2.shape[:2]

            max_height = max(h1, h2)
            scale1 = max_height / h1 if h1 > 0 else 1
            scale2 = max_height / h2 if h2 > 0 else 1

            img1 = cv2.resize(img1, (int(w1 * scale1), max_height))
            img2 = cv2.resize(img2, (int(w2 * scale2), max_height))

            h, w = max_height, img1.shape[1] + img2.shape[1]
            combined = np.zeros((h, w, 3), dtype=np.uint8)
            combined[: img1.shape[0], : img1.shape[1]] = img1
            combined[: img2.shape[0], img1.shape[1] :] = img2

            for match in matches[:20]:
                pt1 = kp1[match.queryIdx].pt
                pt2 = kp2[match.trainIdx].pt
                pt2 = (pt2[0] + img1.shape[1], pt2[1])

                pt1_int = (int(pt1[0]), int(pt1[1]))
                pt2_int = (int(pt2[0]), int(pt2[1]))

                cv2.circle(combined, pt1_int, 8, (0, 255, 0), -1)
                cv2.circle(combined, pt2_int, 8, (0, 255, 0), -1)
                cv2.line(combined, pt1_int, pt2_int, (0, 255, 255), 2)

            _, buffer = cv2.imencode(".jpg", combined)
            b64 = base64.b64encode(buffer).decode("utf-8")
            return b64

        except Exception as e:
            print(f"Error creating annotated image: {e}")
            return None

    def save_annotated_image(self, base64_str: str, output_path: str) -> bool:
        try:
            img_bytes = base64.b64decode(base64_str)
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imwrite(output_path, img)
            return True
        except Exception as e:
            print(f"Error saving annotated image: {e}")
            return False


explainability_service = ExplainabilityService()
