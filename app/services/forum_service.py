import requests
import time

class ForumService:
    def __init__(self):
        self.base_url = "https://community.n8n.io"
        self.headers = {
            "User-Agent": "n8n-popularity-harvester/1.0",
            "Accept": "application/json"
        }

    def fetch_workflow_data(self, query: str):
        """
        Two-step fetch: 
        1. Search for relevant topics.
        2. Get detailed metrics (replies, contributors, views) for each topic.
        """
        try:
            # Step 1: Search for topics
            search_url = f"{self.base_url}/search.json"
            search_params = {"q": query}
            
            search_resp = requests.get(search_url, params=search_params, headers=self.headers, timeout=10)
            search_resp.raise_for_status()
            search_data = search_resp.json()
            
            # Extract top 5 topics to remain polite to the API
            topics = search_data.get("topics", [])[:5]
            results = []

            for t in topics:
                topic_id = t.get("id")
                if not topic_id:
                    continue

                # Step 2: Fetch detailed topic data for precise metrics
                # Endpoint: /t/{id}.json
                detail_url = f"{self.base_url}/t/{topic_id}.json"
                
                try:
                    detail_resp = requests.get(detail_url, headers=self.headers, timeout=10)
                    detail_resp.raise_for_status()
                    d = detail_resp.json()

                    # Mapping to the Big Unified Shape
                    results.append({
                        "workflow_name": d.get("title"),
                        "platform": "forum",
                        "country": "GLOBAL",
                        # Forum Specific Metrics
                        "views": d.get("views"),
                        "likes": d.get("like_count"),
                        "replies": d.get("reply_count"),
                        "contributors": d.get("participant_count"),
                        # Set YouTube/Google specific fields to None
                        "comments": None,
                        "like_to_view_ratio": None,
                        "comment_to_view_ratio": None,
                        "interest_score": None,
                        "monthly_volume": None,
                        "growth_pct": None
                    })
                    
                    # Rate limiting protection: 1 second delay between detail calls
                    time.sleep(1)

                except Exception as detail_err:
                    print(f"⚠️ Error fetching details for topic {topic_id}: {detail_err}")
                    continue

            return results

        except Exception as e:
            print(f"❌ Forum Service Error for '{query}': {e}")
            return []