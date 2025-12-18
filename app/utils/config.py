import os
import json
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Config:
    PROJECT_NAME = "n8n Workflow Popularity System"
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    
    # Targeted Regions for YouTube and Trends
    REGIONS = ["US", "IN"]
    
    # Discourse Forum URL
    FORUM_URL = "https://community.n8n.io"

    # Define a reliable root path (Pathlib is more modern than os.path)
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    @staticmethod
    def get_keywords():
        """
        Dynamically loads and cleans workflow keywords.
        """
        json_path = Config.BASE_DIR / "data" / "seed_workflows.json"
        
        try:
            with open(json_path, "r") as f:
                keywords = json.load(f)
                # deduplicate and clean whitespace
                return list(set([k.strip() for k in keywords if k]))
        except (FileNotFoundError, json.JSONDecodeError):
            # Fallback in case the JSON file is missing or corrupted
            print(f"⚠️ Warning: Seed file not found at {json_path}. Using fallbacks.")
            return ["n8n workflow", "n8n automation", "n8n tutorial"]