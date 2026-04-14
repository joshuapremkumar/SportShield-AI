from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from datetime import datetime
from typing import List

from backend.models.schemas import UploadResponse
from backend.core.config import Config
from backend.services.clip_service import clip_service


router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    if file.content_type not in ["image/jpeg", "image/png", "image/jpg", "image/webp"]:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only images are allowed."
        )

    contents = await file.read()

    image_id = clip_service.generate_image_id(file.filename)

    upload_path = Config.UPLOAD_DIR / f"{image_id}.png"

    try:
        with open(upload_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save image: {str(e)}")

    try:
        embedding = clip_service.generate_embedding(str(upload_path))
        embedding_file = clip_service.save_embedding(embedding, image_id)
    except Exception as e:
        upload_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=500, detail=f"Failed to generate embedding: {str(e)}"
        )

    return UploadResponse(
        image_id=image_id,
        filename=file.filename,
        embedding_file=embedding_file,
        upload_time=datetime.now(),
    )


@router.get("/list", response_model=List[dict])
async def list_uploads():
    uploads = []
    for file in Config.UPLOAD_DIR.glob("*.png"):
        uploads.append(
            {
                "image_id": file.stem,
                "filename": file.name,
                "path": str(file),
                "size": file.stat().st_size,
            }
        )
    return uploads


@router.delete("/{image_id}")
async def delete_upload(image_id: str):
    upload_path = Config.UPLOAD_DIR / f"{image_id}.png"
    embedding_path = Config.EMBEDDING_DIR / f"{image_id}.npy"

    if not upload_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")

    upload_path.unlink()
    if embedding_path.exists():
        embedding_path.unlink()

    return {"message": f"Image {image_id} deleted successfully"}
