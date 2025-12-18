from pytrends.request import TrendReq
import pandas as pd
import random
import time

class TrendsService:
    def __init__(self):
        # tz=360 is US Central Time. hl='en-US' for English results.
        self.pytrends = TrendReq(hl='en-US', tz=360)

    def fetch_workflow_data(self, keyword: str, country: str = "US"):
        """
        Fetches Google Trends data and calculates:
        1. Interest Score: Average relative popularity.
        2. Growth %: Comparison of recent vs. older baseline interest.
        """
        try:
            # Google Trends allows up to 100 characters per keyword
            kw_list = [f"n8n {keyword}"[:100]]
            
            # timeframe='today 3-m' matches your requirement for 60-90 day tracking
            self.pytrends.build_payload(kw_list, timeframe='today 3-m', geo=country)
            df = self.pytrends.interest_over_time()

            if df.empty or kw_list[0] not in df:
                print(f"⚠️ No Trends data for: {keyword}")
                return None

            # Handle Partial Data: Google often provides 'isPartial' for the current day.
            # We drop the last row if it's partial to avoid skewed growth averages.
            if 'isPartial' in df.columns and df['isPartial'].iloc[-1]:
                df = df.iloc[:-1]

            series = df[kw_list[0]]
            
            # 1. Interest Score (Relative search interest 0-100)
            avg_interest = int(series.mean())

            # 2. Change over 60 days Logic
            # We compare the average of the last 30 days to the 30-day window before it.
            recent_avg = series.iloc[-30:].mean()
            previous_avg = series.iloc[-60:-30].mean() if len(series) >= 60 else series.iloc[0:30].mean()
            
            growth_pct = 0.0
            if previous_avg > 0:
                growth_pct = round(((recent_avg - previous_avg) / previous_avg) * 100, 2)
            elif recent_avg > 0:
                # If it went from 0 to something, it's a 'Breakout' or 100% growth
                growth_pct = 100.0

            # 3. Map to the Big Unified Shape
            return {
                "workflow_name": keyword,
                "platform": "google",
                "country": country,
                # Google Specific Fields
                "interest_score": avg_interest,
                "growth_pct": growth_pct,
                "monthly_volume": random.randint(100, 5000), # Placeholder for Keyword Planner volume
                # Set other platform fields to None
                "views": None,
                "likes": None,
                "comments": None,
                "replies": None,
                "contributors": None,
                "like_to_view_ratio": None,
                "comment_to_view_ratio": None
            }

        except Exception as e:
            print(f"❌ Google Trends Error for '{keyword}': {e}")
            # If rate limited (429), sleep longer
            if "429" in str(e):
                time.sleep(60)
            return None