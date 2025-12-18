import time
import logging
from app.database.db import SessionLocal
from app.services.youtube_service import YouTubeService
from app.models.workflow import Workflow
from app.utils.config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("youtube-harvester")

def run_youtube_job():
    db = SessionLocal()
    service = YouTubeService()
    
    logger.info("🚀 Starting YouTube Data Harvest (Big Unified Shape)...")
    
    keywords = Config.get_keywords()
    total_keywords = len(keywords)
    
    for i, keyword in enumerate(keywords):
        for region in Config.REGIONS:
            logger.info(f"[{i+1}/{total_keywords}] Fetching: {keyword} in {region}")
            
            try:
                # fetch_workflow_data returns the complete dictionary for the Unified DB
                results = service.fetch_workflow_data(keyword, region)
                
                for data in results:
                    # Upsert Logic: Check if workflow exists for this platform/country
                    # We use the title and platform to find existing records
                    existing = db.query(Workflow).filter(
                        Workflow.workflow_name == data["workflow_name"],
                        Workflow.platform == "youtube",
                        Workflow.country == region
                    ).first()
                    
                    if existing:
                        # Update all YouTube-related metrics in the Big Shape
                        existing.views = data["views"]
                        existing.likes = data["likes"]
                        existing.comments = data["comments"]
                        existing.like_to_view_ratio = data["like_to_view_ratio"]
                        existing.comment_to_view_ratio = data["comment_to_view_ratio"]
                        logger.debug(f"Updated: {data['workflow_name']}")
                    else:
                        # Add new entry with the full set of keys (including NULLs for other platforms)
                        new_wf = Workflow(**data)
                        db.add(new_wf)
                        logger.debug(f"Added New: {data['workflow_name']}")
                
                # Commit after every keyword/region pair to ensure progress is saved
                db.commit()
                
                # Small sleep to manage YouTube API quota usage
                time.sleep(0.5) 
                
            except Exception as e:
                logger.error(f"❌ Error harvesting YouTube data for '{keyword}': {e}")
                db.rollback()
                time.sleep(2) # Wait a bit before retrying next keyword
                
    db.close()
    logger.info("✅ YouTube Job Finished.")

if __name__ == "__main__":
    run_youtube_job()