import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

class YouTubeService:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def fetch_workflow_data(self, query: str, region: str = "US"):
        try:
            # 1. Search for videos matching the n8n workflow query
            search_response = self.youtube.search().list(
                q=f"n8n workflow {query}",
                part="snippet",
                maxResults=5,
                type="video",
                regionCode=region
            ).execute()

            results = []
            for item in search_response.get("items", []):
                video_id = item["id"]["videoId"]
                
                # 2. Get detailed engagement statistics for the specific video
                video_response = self.youtube.videos().list(
                    id=video_id,
                    part="statistics"
                ).execute()

                if not video_response["items"]:
                    continue

                stats = video_response["items"][0]["statistics"]
                
                # Extract and cast raw metrics
                v = int(stats.get("viewCount", 0))
                l = int(stats.get("likeCount", 0))
                c = int(stats.get("commentCount", 0))

                # 3. Build the Unified Shape for the DB
                # Note: Fields like 'replies' and 'interest_score' are set to None
                results.append({
                    "workflow_name": item["snippet"]["title"],
                    "platform": "youtube",
                    "country": region,
                    # YouTube Specific metrics
                    "views": v,
                    "likes": l,
                    "comments": c,
                    "like_to_view_ratio": l / v if v > 0 else 0.0,
                    "comment_to_view_ratio": c / v if v > 0 else 0.0,
                    # Fields reserved for Forum/Trends (stored as NULL)
                    "replies": None,
                    "contributors": None,
                    "interest_score": None,
                    "monthly_volume": None,
                    "growth_pct": None
                })
            return results
        except Exception as e:
            print(f"❌ YouTube API Error: {e}")
            return []