from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.db import get_db
from app.models.workflow import Workflow
import datetime

router = APIRouter()

@router.get("/workflows", response_model=None)
def read_workflows(
    platform: Optional[str] = Query(None, description="Filter by platform (youtube, forum, google)"),
    country: Optional[str] = Query(None, description="Filter by country (US, IN, GLOBAL)"),
    db: Session = Depends(get_db)
):
    """
    Returns a list of workflows. 
    The shape of 'popularity_metrics' changes dynamically based on the platform.
    """
    query = db.query(Workflow)
    
    # Apply Filters
    if platform:
        query = query.filter(Workflow.platform == platform.lower())
    if country:
        # Use upper for US/IN, but keep 'GLOBAL' consistent
        query = query.filter(Workflow.country == country.upper())
    
    results = query.all()
    
    # to_dict() in the model handles the 'Big Shape' filtering
    return [w.to_dict() for w in results]

@router.get("/health")
def health_check():
    """Health check endpoint for deployment monitoring."""
    return {
        "status": "online", 
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }