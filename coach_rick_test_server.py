"""
Coach Rick AI - Standalone Test Server
Run this to test Coach Rick AI without database dependencies
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import Coach Rick API router
from coach_rick_api import router as coach_rick_router

# Initialize FastAPI app
app = FastAPI(
    title="Coach Rick AI - Test Server",
    description="Standalone test server for Coach Rick AI Engine",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Coach Rick AI router
app.include_router(coach_rick_router, tags=["Coach Rick AI"])

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Coach Rick AI - Test Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "analyze_with_coach": "POST /api/v1/reboot-lite/analyze-with-coach",
            "health": "GET /api/v1/reboot-lite/coach-rick/health",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Coach Rick AI Test Server"
    }


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧠 COACH RICK AI - TEST SERVER")
    print("="*70)
    print("\nStarting server on http://0.0.0.0:8005")
    print("\nEndpoints:")
    print("  POST /api/v1/reboot-lite/analyze-with-coach")
    print("  GET  /api/v1/reboot-lite/coach-rick/health")
    print("  GET  /docs (Swagger UI)")
    print("  GET  /redoc (ReDoc)")
    print("\n" + "="*70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8005)
