# 🛡️ SportShield AI

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=FFD43B" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.109-009974?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Streamlit-1.30-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/CLIP-OpenAI-000000?style=for-the-badge&logo=openai&logoColor=white" alt="CLIP">
</p>

> **Detect unauthorized sports media usage across the internet using AI-powered image similarity, geo-tracking, and explainability.**

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 🖼️ **AI Image Matching** | CLIP-powered semantic similarity for accurate image detection |
| 🌍 **Geo Tracking** | IP-based location tracking to identify content sources globally |
| 🧠 **Explainability Engine** | OpenCV ORB feature matching with visual highlighting |
| ⚡ **Real-time Detection** | Live threat feed with instant alerts |
| 🎯 **Tampering Detection** | Identifies cropped/resized/unauthorized modifications |
| 📊 **Spread Narrative** | Track content distribution across countries |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SportShield AI                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   Upload   │───▶│    CLIP     │───▶│    FAISS    │ │
│  │   Image   │    │  Embedding  │    │    Index   │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         │                   │                               │
│         ▼                   ▼                               │
│  ┌──────────────┐    ┌──────────────┐                    │
│  │   Tavily API  │───▶│ Geo Tracking │───▶│  IPInfo API  │ │
│  │   Web Search │    │  (IP/URL)     │    │   Location  │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────┐                                           │
│  │  Explainable│───▶│  ORB Feature │───▶│   Visual    │ │
│  │   Match     │    │   Matching   │    │  Highlights │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│                                                               │
│  ┌────────────────────────────────────────────────��──┐       │
│  │              Streamlit Dashboard                 │       │
│  │   🔴 Live Threat Feed  │  🗺️ Geo Map  │  📈 Stats  │       │
│  └───────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
SportShield AI/
├── backend/
│   ├── core/
│   │   └── config.py           ⚙️  Configuration & paths
│   ├── models/
│   │   └── schemas.py         📝  Pydantic models
│   ├── routes/
│   │   ├── upload.py          📤  Image upload endpoints
│   │   └── detection.py      🔍  Detection endpoints
│   ├── services/
│   │   ├── clip_service.py        🧠  CLIP embedding generation
│   │   ├── search_service.py      🌐  Tavily web search
│   │   ├── geo_service.py       🌍  IPinfo geo-tracking
│   │   ├── explainability_service.py  🔥  ORB feature matching
│   │   └── detection_service.py    ⚡  Detection orchestration
│   └── main.py                 🚀  FastAPI application
├── frontend/
│   └── app.py                 💻  Streamlit dashboard
├── data/
│   ├── uploads/               📁  Uploaded images
│   ├── embeddings/            💾  CLIP embeddings
│   └── results/               📊  Detection results
├── requirements.txt           📦  Python dependencies
├── .env.example              🔐  API keys template
└── README.md                 📖  This file
```

---

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API keys
cp .env.example .env
# Edit .env with your TAVILY_API_KEY and IPINFO_API_KEY

# 3. Run Backend (Terminal 1)
uvicorn backend.main:app --reload --port 8000

# 4. Run Frontend (Terminal 2)
streamlit run frontend/app.py
```

**Access Points:**
- 🌐 API: `http://localhost:8000`
- 📚 Swagger UI: `http://localhost:8000/docs`
- 🎨 Dashboard: `http://localhost:8500`

---

## 🔧 API Endpoints

### 📤 Upload
```bash
POST /upload/                  # Upload image & generate embedding
GET  /upload/list              # List all uploaded images
DELETE /upload/{image_id}      # Delete image
```

### 🔍 Detection
```bash
POST /detect/                  # Find similar images
GET  /detect/results/{id}     # Get detection results
GET  /detect/health           # Health check
```

---

## 🧠 Confidence Intelligence

| Similarity | Keypoints | Label |
|-----------|-----------|-------|
| >85% | >10 | 🔴 **High** 🚨 |
| 60-85% | >5 | 🟡 **Medium** ⚠️ |
| <60% | any | 🟢 **Low** ℹ️ |

---

## 🖥️ Usage Examples

### Upload an Image
```bash
curl -X POST -F "file=@game_highlight.jpg" http://localhost:8000/upload/
```

### Detect Unauthorized Usage
```bash
curl -X POST "http://localhost:8000/detect/?image_id=img_abc123&search_keyword=NBA&top_k=5"
```

### Dashboard Workflow
1. Navigate to **Live Threat Feed**
2. Enter your Image ID
3. Set search keyword (e.g., "NBA game")
4. Click **🔍 Scan for Threats**
5. View real-time alerts with geo-map

---

## 🔐 API Keys

Get free API keys from:

| Service | URL | Purpose |
|---------|-----|---------|
| **Tavily** | https://tavily.com | Web image search |
| **IPinfo** | https://ipinfo.io | Geo-location tracking |

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI, Uvicorn |
| **Frontend** | Streamlit |
| **AI/ML** | CLIP (OpenAI), OpenCV |
| **Search** | Tavily API |
| **Storage** | FAISS, NumPy |
| **Visualization** | Plotly, PyDeck |

</div>

---

## 📄 License

<p align="center">
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License">
  </a>
</p>

---

<p align="center">
  <strong>🛡️ SportShield AI</strong> — Protecting sports media worldwide
</p>