from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import sys
from pathlib import Path

# Add the project root to the Python path to allow imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import routers
from ui.services.monitoring.router import router as monitoring_router
from ui.services.websites.router import router as websites_router

# Create FastAPI app
app = FastAPI(
    title="Scraper Monitoring Dashboard",
    description="Real-time monitoring and management interface for web scraping operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this appropriately for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(monitoring_router)
app.include_router(websites_router)

# Root endpoint - redirect to monitoring dashboard
@app.get("/")
async def root():
    """Redirect to the monitoring dashboard."""
    return RedirectResponse(url="/monitoring")



def run():
    uvicorn.run(app, host="0.0.0.0", port=8002, log_level="info", access_log=True)
