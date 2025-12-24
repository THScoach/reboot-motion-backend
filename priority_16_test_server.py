"""
PRIORITY 16: TEAM MANAGEMENT TEST SERVER
=========================================

Test server for Coach Dashboard and Team Management APIs

Features:
- Coach authentication
- Team management
- Athlete roster
- Training assignments
- Team analytics

Usage:
    python3 priority_16_test_server.py

Access at: http://localhost:8003
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from team_management_routes import router as team_router

# Create FastAPI app
app = FastAPI(
    title="Reboot Motion - Coach Dashboard API",
    description="Team Management & Coach Dashboard - Priority 16",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include team management routes
app.include_router(team_router)


@app.get("/", response_class=HTMLResponse)
def root():
    """Landing page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Reboot Motion - Coach Dashboard</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }
            h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                text-align: center;
            }
            .subtitle {
                text-align: center;
                font-size: 1.2em;
                opacity: 0.9;
                margin-bottom: 30px;
            }
            .feature-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .feature-card {
                background: rgba(255, 255, 255, 0.15);
                border-radius: 15px;
                padding: 25px;
                transition: transform 0.3s;
            }
            .feature-card:hover {
                transform: translateY(-5px);
                background: rgba(255, 255, 255, 0.2);
            }
            .feature-icon {
                font-size: 3em;
                margin-bottom: 15px;
            }
            .feature-title {
                font-size: 1.3em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .feature-desc {
                opacity: 0.9;
                line-height: 1.6;
            }
            .cta-button {
                display: inline-block;
                background: white;
                color: #667eea;
                padding: 15px 40px;
                border-radius: 30px;
                text-decoration: none;
                font-weight: bold;
                margin: 10px;
                transition: all 0.3s;
            }
            .cta-button:hover {
                transform: scale(1.05);
                box-shadow: 0 5px 20px rgba(255, 255, 255, 0.4);
            }
            .button-container {
                text-align: center;
                margin: 40px 0;
            }
            .api-section {
                background: rgba(0, 0, 0, 0.2);
                border-radius: 15px;
                padding: 25px;
                margin: 30px 0;
            }
            .endpoint {
                background: rgba(255, 255, 255, 0.1);
                border-left: 4px solid #4CAF50;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
            }
            .method {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 5px;
                font-weight: bold;
                margin-right: 10px;
            }
            .method-get {
                background: #4CAF50;
            }
            .method-post {
                background: #2196F3;
            }
            .method-put {
                background: #FF9800;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏆 Reboot Motion Coach Dashboard</h1>
            <div class="subtitle">Priority 16: Team Management & Multi-Athlete Coordination</div>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon">👥</div>
                    <div class="feature-title">Team Management</div>
                    <div class="feature-desc">
                        Create and manage multiple teams, organize athletes by season, 
                        and track roster changes throughout the year.
                    </div>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <div class="feature-title">Athlete Roster</div>
                    <div class="feature-desc">
                        Complete athlete profiles with biometrics, positions, status tracking,
                        and performance history. Search and filter by any criteria.
                    </div>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">📝</div>
                    <div class="feature-title">Coach Notes</div>
                    <div class="feature-desc">
                        Document observations, concerns, and progress for each athlete.
                        Tag notes by category for easy retrieval.
                    </div>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🎯</div>
                    <div class="feature-title">Drill Assignments</div>
                    <div class="feature-desc">
                        Assign personalized training drills to athletes, set deadlines,
                        and track completion progress in real-time.
                    </div>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">📈</div>
                    <div class="feature-title">Team Analytics</div>
                    <div class="feature-desc">
                        View aggregate team statistics, compare athletes side-by-side,
                        and identify trends across your roster.
                    </div>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🔍</div>
                    <div class="feature-title">Multi-Athlete Comparison</div>
                    <div class="feature-desc">
                        Compare performance metrics across multiple athletes to identify
                        strengths, weaknesses, and training priorities.
                    </div>
                </div>
            </div>
            
            <div class="button-container">
                <a href="/docs" class="cta-button">📚 API Documentation</a>
                <a href="/dashboard" class="cta-button">🎯 View Dashboard</a>
            </div>
            
            <div class="api-section">
                <h2>🔌 Available API Endpoints</h2>
                
                <div class="endpoint">
                    <span class="method method-post">POST</span>
                    <span>/api/teams/coaches</span>
                    <div style="margin-top: 8px; opacity: 0.8;">Create coach profile</div>
                </div>
                
                <div class="endpoint">
                    <span class="method method-post">POST</span>
                    <span>/api/teams/teams</span>
                    <div style="margin-top: 8px; opacity: 0.8;">Create new team</div>
                </div>
                
                <div class="endpoint">
                    <span class="method method-post">POST</span>
                    <span>/api/teams/athletes</span>
                    <div style="margin-top: 8px; opacity: 0.8;">Add athlete to roster</div>
                </div>
                
                <div class="endpoint">
                    <span class="method method-get">GET</span>
                    <span>/api/teams/teams/{team_id}/roster</span>
                    <div style="margin-top: 8px; opacity: 0.8;">Get team roster with filters</div>
                </div>
                
                <div class="endpoint">
                    <span class="method method-get">GET</span>
                    <span>/api/teams/teams/{team_id}/analytics</span>
                    <div style="margin-top: 8px; opacity: 0.8;">Get team analytics</div>
                </div>
                
                <div class="endpoint">
                    <span class="method method-post">POST</span>
                    <span>/api/teams/assignments</span>
                    <div style="margin-top: 8px; opacity: 0.8;">Assign drill to athlete</div>
                </div>
                
                <div class="endpoint">
                    <span class="method method-get">GET</span>
                    <span>/api/teams/dashboard/{coach_id}</span>
                    <div style="margin-top: 8px; opacity: 0.8;">Get coach dashboard summary</div>
                </div>
                
                <div class="endpoint">
                    <span class="method method-post">POST</span>
                    <span>/api/teams/athletes/compare</span>
                    <div style="margin-top: 8px; opacity: 0.8;">Compare multiple athletes</div>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 40px; opacity: 0.8;">
                <p>🔗 <strong>Integrates With:</strong></p>
                <p>Priority 9: Kinetic Capacity | Priority 10: Recommendations | 
                   Priority 11: Motor Preference | Priority 13: Video Library | 
                   Priority 14: Progress Tracking</p>
            </div>
        </div>
    </body>
    </html>
    """


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    """Coach dashboard UI"""
    # This would be served from templates/coach_dashboard.html
    # For now, return a simple placeholder
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Coach Dashboard</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100">
        <div class="container mx-auto px-4 py-8">
            <h1 class="text-4xl font-bold text-gray-800 mb-8">Coach Dashboard</h1>
            
            <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
                <h2 class="text-2xl font-semibold mb-4">Quick Start</h2>
                <p class="text-gray-600 mb-4">
                    To use the Coach Dashboard, make API calls to the endpoints listed below.
                    Full UI implementation will be added in the next phase.
                </p>
                <a href="/docs" class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700">
                    View API Documentation
                </a>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-white rounded-lg shadow p-6">
                    <h3 class="text-xl font-semibold mb-2">Teams</h3>
                    <p class="text-3xl font-bold text-blue-600">0</p>
                    <p class="text-gray-600 text-sm">Total teams managed</p>
                </div>
                
                <div class="bg-white rounded-lg shadow p-6">
                    <h3 class="text-xl font-semibold mb-2">Athletes</h3>
                    <p class="text-3xl font-bold text-green-600">0</p>
                    <p class="text-gray-600 text-sm">Active athletes</p>
                </div>
                
                <div class="bg-white rounded-lg shadow p-6">
                    <h3 class="text-xl font-semibold mb-2">Assignments</h3>
                    <p class="text-3xl font-bold text-purple-600">0</p>
                    <p class="text-gray-600 text-sm">Pending assignments</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    print("=" * 70)
    print("PRIORITY 16: COACH DASHBOARD & TEAM MANAGEMENT")
    print("=" * 70)
    print()
    print("🚀 Starting test server...")
    print()
    print("📍 Server running on: http://0.0.0.0:8003")
    print("📍 Local access: http://localhost:8003")
    print("📚 API Docs: http://localhost:8003/docs")
    print("🎯 Dashboard: http://localhost:8003/dashboard")
    print()
    print("=" * 70)
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8003)
