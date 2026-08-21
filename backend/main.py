from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.api import crop_router

# Resolve paths relative to the project root
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
FRONTEND_DIR = ROOT_DIR / "frontend"

app = FastAPI(
    title="AI Crop Advisor",
    description="Refactored modular FastAPI backend for crop recommendations.",
    version="1.0.0",
)

# Register API Router
app.include_router(crop_router, prefix="/api")

# Define Health Check endpoint
@app.get("/health")
async def health_check() -> dict:
    return {
        "status": "ok",
        "message": "AI Crop Advisor backend is running."
    }

# Serve root index.html
@app.get("/")
async def serve_index():
    return FileResponse(FRONTEND_DIR / "index.html")

# Serve styles.css directly at /styles.css for fallback or support
@app.get("/styles.css")
async def serve_css():
    return FileResponse(FRONTEND_DIR / "styles.css")

# Serve script.js directly at /script.js for fallback or support
@app.get("/script.js")
async def serve_js():
    return FileResponse(FRONTEND_DIR / "script.js")

# Mount the frontend directory under /static to support clean relative references
# (e.g. /static/styles.css, /static/script.js, /static/assets/...)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
