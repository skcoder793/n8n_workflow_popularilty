#!/bin/bash

# 1. Setup Environment
# echo "🚀 Setting up the n8n Workflow Popularity System..."
# python3 -m venv venv
# source venv/bin/activate

# 2. Install Dependencies
echo "📦 Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Initialize Database
echo "🗄️ Initializing database..."
python -m app.database.init_db

# 4. Run an initial data harvest

echo "🚜 Running initial data harvest..."
python -m jobs.update_forum
python -m jobs.update_youtube

# 5. Launch API
echo "🌐 Starting REST API at http://0.0.0.0:8000"
echo "📖 Access API Documentation at http://0.0.0.0:8000/docs"
uvicorn app.main:app --host 0.0.0.0 --port 8000