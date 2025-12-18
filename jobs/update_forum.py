from app.database.db import SessionLocal
from app.services.forum_service import ForumService
from app.models.workflow import Workflow
from app.utils.config import Config
import time
import logging

# Set up logging to track long-running harvest progress
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("forum-harvester")

def run_forum_job():
    db = SessionLocal()
    service = ForumService()
    
    logger.info("🚀 Starting Deep Forum Data Harvest...")
    
    # Load keywords from data/seed_workflows.json
    keywords = Config.get_keywords()
    total_keywords = len(keywords)
    
    new_records = 0
    updated_records = 0

    for i, keyword in enumerate(keywords):
        logger.info(f"[{i+1}/{total_keywords}] Harvesting for: {keyword}")
        
        try:
            # fetch_workflow_data now returns the deep topic metrics
            results = service.fetch_workflow_data(keyword)
            
            if not results:
                logger.warning(f"⚠️ No results found for '{keyword}'")
                continue

            for data in results:
                # Deduplication: Check if this specific thread title exists for 'forum'
                existing = db.query(Workflow).filter(
                    Workflow.workflow_name == data["workflow_name"],
                    Workflow.platform == "forum"
                ).first()
                
                if existing:
                    # Update metrics for the Unified Shape
                    existing.replies = data.get("replies")
                    existing.likes = data.get("likes")
                    existing.views = data.get("views")
                    existing.contributors = data.get("contributors")
                    updated_records += 1
                else:
                    # Insert new record into the Unified Shape
                    db.add(Workflow(**data))
                    new_records += 1
            
            # Commit after every keyword to prevent massive transaction lockup
            db.commit()
            
        except Exception as e:
            logger.error(f"❌ Critical error during keyword '{keyword}': {e}")
            db.rollback() # Undo any pending changes if commit failed
            # Optional: Sleep longer if error suggests a rate limit
            time.sleep(5)
            
    db.close()
    logger.info(f"✅ Forum Job Finished. New: {new_records}, Updated: {updated_records}")

if __name__ == "__main__":
    run_forum_job()