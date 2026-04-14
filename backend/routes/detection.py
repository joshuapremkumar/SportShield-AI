from fastapi import APIRouter, HTTPException, Query
from typing import List

from backend.models.schemas import DetectionResponse, SearchResult
from backend.services.detection_service import detection_service


router = APIRouter(prefix="/detect", tags=["detection"])


@router.post("/", response_model=DetectionResponse)
async def detect_images(
    image_id: str = Query(..., description="The image ID to search for matches"),
    search_keyword: str = Query(
        ..., description="Keyword to search for similar images"
    ),
    top_k: int = Query(5, description="Number of top results to return"),
):
    if top_k < 1 or top_k > 20:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 20")

    try:
        results = detection_service.detect_matches(image_id, search_keyword, top_k)

        search_results = [
            SearchResult(
                image_id=r["image_id"],
                search_url=r["search_url"],
                domain=r.get("domain"),
                ip_address=r.get("ip_address"),
                country=r.get("country"),
                city=r.get("city"),
                latitude=r.get("latitude"),
                longitude=r.get("longitude"),
                similarity_score=r["similarity_score"],
                matched_keypoints=r["matched_keypoints"],
                confidence=r["confidence"],
                annotated_image=r.get("annotated_image"),
                original_image=r["original_image"],
                matched_image=r["matched_image"],
            )
            for r in results
        ]

        results_file = detection_service.save_results(image_id, results)

        return DetectionResponse(
            query_image=image_id,
            search_keyword=search_keyword,
            results=search_results,
            total_matches=len(search_results),
            detection_time=search_results[0].similarity_score
            if search_results
            else None,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")


@router.get("/results/{image_id}")
async def get_detection_results(image_id: str):
    import json
    from pathlib import Path

    results_files = sorted(
        Config.RESULTS_DIR.glob(f"results_{image_id}_*.json"),
        key=lambda x: x.stat().st_mtime,
        reverse=True,
    )

    if not results_files:
        raise HTTPException(status_code=404, detail="No results found for this image")

    with open(results_files[0]) as f:
        return json.load(f)


@router.get("/health")
async def health_check():
    from backend.services.clip_service import clip_service
    from backend.core.config import Config

    embeddings_count = len(list(Config.EMBEDDING_DIR.glob("*.npy")))
    uploads_count = len(list(Config.UPLOAD_DIR.glob("*.png")))

    return {
        "status": "healthy",
        "clip_model": clip_service.device,
        "total_embeddings": embeddings_count,
        "total_uploads": uploads_count,
        "data_directories": {
            "uploads": str(Config.UPLOAD_DIR),
            "embeddings": str(Config.EMBEDDING_DIR),
            "results": str(Config.RESULTS_DIR),
        },
    }


from backend.core.config import Config
