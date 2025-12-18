# 🚀 n8n Workflow Popularity Tracker

A professional-grade data engine that harvests popularity **"evidence"** for n8n automations across **YouTube**, the **n8n Community Forum**, and **Google Trends**.  
It provides a unified REST API to discover which automations are actually trending and in demand.

---

## 🌟 Key Features

### 🔌 Multi-Source Harvester
Specialized scrapers for:
- **YouTube** (YouTube Data API v3)
- **n8n Forum** (Discourse API)
- **Google Trends** (Pytrends)

### 🧱 Unified Data Model
A single **"Big Shape"** SQLite database that normalizes heterogeneous metrics.

### 🧠 Intelligent Metrics
- **YouTube**
  - View counts
  - Likes
  - Engagement ratios
- **Forum**
  - Replies
  - Thread views
  - Unique participant counts
- **Google Trends**
  - Relative interest score
  - 60-day growth velocity

### 🔄 Dynamic API
A single endpoint that reformats JSON responses on-the-fly based on the platform source.

### 📈 Scalable
Built-in rate limiting and error recovery to handle **20,000+ workflow records**.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+ & FastAPI  
- **Database:** SQLite with SQLAlchemy ORM  
- **APIs & Libraries:**  
  - YouTube Data API v3  
  - Discourse API  
  - Pytrends  
  - Requests  
  - Pandas  
- **Server:** Uvicorn  

---

## 📂 Project Structure

```plaintext
.
├── app/
│   ├── api/            # FastAPI routes & endpoints
│   ├── database/       # DB session and initialization
│   ├── models/         # SQLAlchemy unified schema
│   ├── services/       # YouTube, Forum, and Trends logic
│   ├── utils/          # Helper functions & config
│   └── main.py         # App entry point
├── data/
│   └── seed_workflows.json   # 3,000+ keywords for harvesting
├── jobs/               # Background data collection scripts
└── .env                # API keys and environment variables

```






## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10 or higher
- A YouTube Data API Key (from Google Cloud Console)

---

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/n8n-popularity-tracker.git
cd n8n-popularity-tracker

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### 3. Configuration

Create a `.env` file in the project root:

```env
YOUTUBE_API_KEY=your_key_here
```

---

## 📡 API Endpoints

| Endpoint | Description |
|--------|------------|
| GET /api/workflows | List all workflows with unified metrics |
| GET /api/workflows?platform=youtube | Filter results for YouTube engagement |
| GET /api/workflows?country=IN | Segment data by region |
| GET /api/health | Health check |
| GET /docx | API dashboard |

---

## 📊 Data Mapping (The "Big Shape")

- **YouTube:** views, likes, engagement_ratios
- **Forum:** replies, likes, unique_contributors
- **Google Trends:** interest_score, growth_pct
