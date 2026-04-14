from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from backend.core.config import Config
from backend.models.schemas import HealthResponse
from backend.routes.upload import router as upload_router
from backend.routes.detection import router as detection_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"SportShield AI Backend Starting...")
    print(f"Upload directory: {Config.UPLOAD_DIR}")
    print(f"Embedding directory: {Config.EMBEDDING_DIR}")
    print(f"Results directory: {Config.RESULTS_DIR}")
    yield
    print("SportShield AI Backend Shutting down...")


app = FastAPI(
    title="SportShield AI API",
    description="AI-powered sports media detection and tracking system",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(detection_router)


@app.get("/", response_model=HealthResponse)
async def root():
    return HealthResponse(
        status="running",
        message="SportShield AI API is running. Use /docs for API documentation.",
    )


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="healthy", message="All services are operational")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
