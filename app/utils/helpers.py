import re

def calculate_engagement(likes: int, views: int) -> float:
    """Safely calculate like-to-view ratio (primary for YouTube)."""
    if not views or views == 0:
        return 0.0
    return round(likes / views, 4)

def calculate_growth_pct(series) -> float:
    """
    Calculates percentage growth between the start and end of a time series.
    Used for Google Trends 'is it trending up in the last 30-60 days?'
    """
    if series is None or len(series) < 10:
        return 0.0
    
    # Compare average of first 10 days to average of last 10 days
    first_avg = series.iloc[:10].mean()
    last_avg = series.iloc[-10:].mean()
    
    if first_avg > 0:
        return round(((last_avg - first_avg) / first_avg) * 100, 2)
    elif last_avg > 0:
        return 100.0  # From zero to hero
    return 0.0

def clean_title(title: str) -> str:
    """
    Normalizes titles from YouTube and Forums.
    Removes HTML entities, marketing fluff, and common keywords.
    """
    if not title:
        return "Untitled Workflow"
        
    # Remove HTML entities like &ndash; or &rsquo;
    cleaned = re.sub(r'&\w+;', ' ', title)
    
    # Specific n8n clutter removal
    removals = ["[n8n]", "n8n tutorial", "n8n workflow", "2024", "2025", "how to", "setup"]
    cleaned = cleaned.lower()
    for word in removals:
        cleaned = cleaned.replace(word, "")
    
    # Remove extra spaces and capitalize
    return " ".join(cleaned.split()).strip().capitalize()

def format_percentage(value: float) -> str:
    """Formats growth as a string with a + sign if positive."""
    if value > 0:
        return f"+{value}%"
    return f"{value}%"