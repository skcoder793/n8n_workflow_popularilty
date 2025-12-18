from app.database.db import engine
from app.models.workflow import Base
import os

def init_db():
    """
    Initializes the SQLite database by creating all tables defined in the models.
    This script should be run once before starting the application or whenever 
    the model schema is updated.
    """
    print("\n🚀 Initializing the n8n Popularity Database...")
    
    # 1. Ensure the directory structure exists
    db_path = "./n8n_popularity.db"
    
    # 2. Import models to register them with the Base.metadata
    # We import Workflow specifically to ensure SQLAlchemy sees the table definition
    try:
        from app.models.workflow import Workflow
        
        print("📝 Registering models...")
        Base.metadata.create_all(bind=engine)
        
        print(f"✅ Database tables created successfully at: {os.path.abspath(db_path)}")
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")

if __name__ == "__main__":
    init_db()