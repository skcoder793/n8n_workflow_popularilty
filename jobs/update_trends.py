import time
import random
import logging
from app.database.db import SessionLocal
from app.services.trends_service import TrendsService
from app.models.workflow import Workflow
from app.utils.config import Config

# Configure logging for long-running harvest
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("trends-harvester")

# Strict timing to avoid 429 Too Many Requests
MIN_SLEEP = 15
MAX_SLEEP = 25

def run_trends_job():
    db = SessionLocal()
    service = TrendsService()
    
    logger.info("🚀 Starting Google Trends Data Harvest (Unified Big Shape)...")
    
    keywords = Config.get_keywords()
    total_tasks = len(keywords) * len(Config.REGIONS)
    current_task = 0

    for keyword in keywords:
        for country in Config.REGIONS:
            current_task += 1
            logger.info(f"[{current_task}/{total_tasks}] Processing: {keyword} | Region: {country}")
            
            try:
                # fetch_workflow_data now returns interest_score, growth_pct, and monthly_volume
                data = service.fetch_workflow_data(keyword, country)
                
                if data:
                    existing = db.query(Workflow).filter(
                        Workflow.workflow_name == data["workflow_name"],
                        Workflow.platform == "google",
                        Workflow.country == country
                    ).first()
                    
                    if existing:
                        # Update the specific Unified Trends fields
                        existing.interest_score = data.get("interest_score")
                        existing.growth_pct = data.get("growth_pct")
                        existing.monthly_volume = data.get("monthly_volume")
                    else:
                        # Insert new entry into the Big Unified Shape
                        db.add(Workflow(**data))
                    
                    db.commit()
                    logger.info(f"✅ Saved Trend: {keyword} ({country})")
                else:
                    logger.warning(f"⚠️ No data found or skipped for: {keyword}")

            except Exception as e:
                logger.error(f"❌ Error during Trends harvest for '{keyword}': {e}")
                db.rollback()
                # If we hit an error, sleep longer to cool down the connection
                time.sleep(60)

            # Mandatory cooldown to avoid Google IP ban
            sleep_time = random.uniform(MIN_SLEEP, MAX_SLEEP)
            time.sleep(sleep_time)
            
    db.close()
    logger.info("🏁 Google Trends Job Finished.")

if __name__ == "__main__":
    run_trends_job()