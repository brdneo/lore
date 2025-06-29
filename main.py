#!/usr/bin/env python3
"""
Main entry point for Lore N.A. Railway deployment
Enhanced with database status logging
"""

import sys
import os

# Add the agent_runner directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'services', 'agent_runner'))

# Import and run the main application
if __name__ == "__main__":
    from api_server import app
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = "0.0.0.0"
    database_url = os.getenv("DATABASE_URL")
    
    print("🚀 Starting Lore N.A. API Server for Railway")
    print(f"🌐 Server: http://{host}:{port}")
    
    if database_url:
        print(f"💾 Database: PostgreSQL (Neon) - Connected")
    else:
        print("⚠️ DATABASE_URL not set, using SQLite fallback")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )
