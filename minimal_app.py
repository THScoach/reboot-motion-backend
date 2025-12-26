"""
Minimal FastAPI app for Railway deployment testing
This bypasses all heavy imports to test if Railway deployment works
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI(
    title="Catching Barrels - Minimal Test",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Minimal test app is working!",
        "port": os.getenv("PORT", "not set")
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/coach-rick-analysis", response_class=HTMLResponse)
def coach_rick_ui():
    """Serve the Coach Rick Analysis UI"""
    try:
        with open("templates/coach_rick_analysis.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
        <body>
            <h1>Coach Rick Analysis UI</h1>
            <p>Template file not found, but the endpoint is working!</p>
            <p>This proves Railway deployment is successful.</p>
        </body>
        </html>
        """

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
