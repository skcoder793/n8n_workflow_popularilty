from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    workflow_name = Column(String, index=True)
    platform = Column(String)  # youtube, forum, google
    country = Column(String)   # US, IN, GLOBAL

    # --- Unified Storage (Big Shape) ---
    # YouTube metrics
    views = Column(Integer, nullable=True)          
    likes = Column(Integer, nullable=True)          
    comments = Column(Integer, nullable=True)       
    like_to_view_ratio = Column(Float, nullable=True)
    comment_to_view_ratio = Column(Float, nullable=True)

    # Forum specific metrics
    replies = Column(Integer, nullable=True)        
    contributors = Column(Integer, nullable=True)   

    # Google Trends specific metrics
    interest_score = Column(Integer, nullable=True) 
    monthly_volume = Column(Integer, nullable=True) 
    growth_pct = Column(Float, nullable=True)       
    
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        """Unified API shape with platform-specific metric visibility."""
        output = {
            "workflow": self.workflow_name,
            "platform": self.platform,
            "country": self.country,
            "popularity_metrics": {}
        }

        if self.platform.lower() == "youtube":
            output["popularity_metrics"] = {
                "views": self.views,
                "likes": self.likes,
                "comments": self.comments,
                "like_to_view_ratio": round(self.like_to_view_ratio, 4) if self.like_to_view_ratio else 0.0,
                "comment_to_view_ratio": round(self.comment_to_view_ratio, 4) if self.comment_to_view_ratio else 0.0
            }
        elif self.platform.lower() == "forum":
            output["popularity_metrics"] = {
                "replies": self.replies,
                "likes": self.likes,
                "unique_contributors": self.contributors,
                "thread_views": self.views
            }
        elif self.platform.lower() == "google":
            output["popularity_metrics"] = {
                "relative_search_interest": self.interest_score,
                "keyword_search_volume": self.monthly_volume,
                "change_over_60_days": f"{self.growth_pct}%" if self.growth_pct else "0%"
            }
        
        return output