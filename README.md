# SportShield AI

AI-Powered Sports Media Detection & Tracking System

## Overview

SportShield AI detects unauthorized usage of sports media across the internet using:
- **CLIP** for AI-powered image similarity matching
- **Tavily API** for web search
- **Geo-tracking** with IPinfo to locate content sources
- **Explainability** using OpenCV ORB feature matching

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **AI Models**: CLIP (transformers)
- **Computer Vision**: OpenCV
- **Visualization**: Plotly, PyDeck

## Project Structure

```
Cepheus 2.0 2026/
├── backend/
│   ├── core/
│   │   └── config.py          # Configuration and paths
│   ├── models/
│   │   └── schemas.py        # Pydantic models
│   ├── routes/
│   │   ├── upload.py        # Image upload endpoints
│   │   └── detection.py     # Detection endpoints
│   ├── services/
│   │   ├── clip_service.py         # CLIP embedding generation
│   │   ├── search_service.py      # Web search via Tavily
│   │   ├── geo_service.py         # IP geo-tracking
│   │   ├── explainability_service.py  # Feature matching
│   │   └── detection_service.py  # Main detection logic
│   └── main.py              # FastAPI application
├── frontend/
│   └── app.py              # Streamlit dashboard
├── data/
│   ├── uploads/            # Uploaded images
│   ├── embeddings/         # Generated embeddings
│   └── results/            # Detection results
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Prerequisites

- Python 3.9+
- OpenAI API key (for CLIP)
- Tavily API key (for web search)
- IPinfo API key (for geo-tracking)

### 2. Environment Setup

Create a `.env` file in the project root:

```env
# API Keys (get from https://platform.openai.com, https://tavily.com, https://ipinfo.io)
TAVILY_API_KEY=your_tavily_api_key
IPINFO_API_KEY=your_ipinfo_api_key

# Optional: Set environment for transformers cache
HF_HOME=/path/to/huggingface/cache
TRANSFORMERS_CACHE=/path/to/transformers/cache
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: For FAISS support, you may need to install separately:
```bash
pip install faiss-cpu
```

### 4. Run the Backend

```bash
# Start FastAPI server
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### 5. Run the Frontend

```bash
# In a new terminal
streamlit run frontend/app.py
```

The dashboard will open at `http://localhost:8500`

## API Endpoints

### Upload
- `POST /upload/` - Upload an image
- `GET /upload/list` - List uploaded images
- `DELETE /upload/{image_id}` - Delete an image

### Detection
- `POST /detect/` - Detect similar images
- `GET /detect/results/{image_id}` - Get detection results
- `GET /detect/health` - Health check

### Main
- `GET /` - Root endpoint
- `GET /health` - Health check

## Usage Example

1. **Upload an image** via the dashboard or API:
   ```bash
   curl -X POST -F "file=@image.jpg" http://localhost:8000/upload/
   ```

2. **Detect matches**:
   ```bash
   curl -X POST "http://localhost:8000/detect/?image_id=img_abc123&search_keyword=NBA%20game&top_k=5"
   ```

3. **View results** in the dashboard at `http://localhost:8500`

## Confidence Labels

| Similarity | Keypoints | Label |
|------------|----------|-------|
| >85% | >10 | High |
| 60-85% | >5 | Medium |
| <60% | any | Low |

## Features

1. **Media Upload**: Upload images, generate CLIP embeddings
2. **Web Search**: Search for similar images using Tavily API
3. **Image Matching**: Cosine similarity with CLIP embeddings
4. **Geo Tracking**: Extract location from source domains
5. **Explainability**: Highlight matching regions with ORB
6. **Dashboard**: Streamlit UI with maps and visualizations

## License

MIT License