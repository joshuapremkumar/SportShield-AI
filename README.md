# 🛡️ SportShield AI

**AI-powered Digital Asset Protection for Sports Media**

SportShield AI detects unauthorized usage of sports images and videos across the internet using computer vision, geo-tracking, and explainable AI.

---

## 🚨 The Problem

Sports organizations generate massive volumes of high-value media that spread rapidly across global platforms. This creates a visibility gap, making it nearly impossible to track unauthorized usage and protect intellectual property.

---

## 💡 Our Solution

SportShield AI uses:

* 🧠 AI-powered visual fingerprinting (CLIP embeddings)
* 🌍 Geo-tracking to identify where content spreads globally
* 🔍 Web intelligence via Tavily API
* 🧩 Explainability engine to show *why* content was flagged

---

## ⚡ Key Features

* 📤 Media Upload & Fingerprinting
* 🌐 Web Search & Detection
* 🧠 Explainable AI (Visual Matching)
* 🌍 Geo Tracking (Global Spread Analysis)
* 🚨 Confidence-Based Violation Detection

---

## 🧠 What Makes It Unique

Unlike traditional systems, SportShield AI doesn't just detect misuse—it explains it and tracks its global spread in real-time.

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