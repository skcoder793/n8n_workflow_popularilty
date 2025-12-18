from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import datetime
import logging
from contextlib import asynccontextmanager

# Internal imports
from app.api.workflows import router as workflow_router
from app.database.db import engine
from app.models.workflow import Base

# Set up logging to track ingestion and API performance
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("n8n-popularity")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events.
    Ensures the database is ready before the API starts accepting requests.
    """
    logger.info("🚀 System booting up. Initializing n8n_popularity.db...")
    # This creates the 'Big Unified Shape' tables if they don't exist
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("🛑 System shutting down.")

# 1. Initialize the FastAPI instance
app = FastAPI(
    title="n8n Workflow Popularity System",
    description="Unified API providing multi-platform popularity evidence (YouTube, Forum, Google Trends) for n8n automations.",
    version="1.0.0",
    lifespan=lifespan
)

# 2. CORS Configuration
# Crucial if you want to display this data in an n8n dashboard or a web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"❌ Unhandled Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An internal error occurred while processing the workflow data."},
    )

# 4. Register Routes
app.include_router(workflow_router, prefix="/api", tags=["Workflows"])

# 5. Root Landing Page
@app.get("/")
async def root():
    return {
        "project": "n8n Workflow Popularity System",
        "status": "online",
        "server_time": datetime.datetime.utcnow().isoformat(),
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        },
        "query_examples": {
            "all": "/api/workflows",
            "trending_google": "/api/workflows?platform=google",
            "india_segment": "/api/workflows?country=IN"
        }
    }

if __name__ == "__main__":
    # Standard production settings
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)