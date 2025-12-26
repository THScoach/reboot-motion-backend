# Reboot Motion API Integration
## Builder 2: Expose Reboot API Feature

**Date**: 2025-12-26  
**Status**: Ready for UI Implementation  
**Timeline**: ~3 hours

---

## 📋 Available Endpoints

### Session API (`session_api.py`)

✅ **GET** `/api/sessions/{session_id}/report`
- Get complete PlayerReport for a session
- Returns: Full KRS + 4B Framework data
- Example: `/api/sessions/coach_rick_abc123/report`

✅ **GET** `/api/sessions/{session_id}`
- Get session summary (without full report)
- Returns: Key metrics only (KRS, motor profile, bat speed, etc.)

✅ **GET** `/api/players/{player_id}/sessions`
- Get all sessions for a player (paginated)
- Query params: `limit` (default 10), `offset` (default 0)
- Returns: List of session summaries

✅ **GET** `/api/players/{player_id}/progress`
- Get aggregated progress for a player
- Returns: Total sessions, KRS history, recent sessions, milestones

✅ **GET** `/api/storage/health`
- Health check for session storage
- Returns: Database stats

---

### Player Report API (`player_report_routes.py`)

✅ **POST** `/reports/from-coach-rick`
- Create PlayerReport from Coach Rick analysis
- Input: Coach Rick analysis JSON
- Output: Complete PlayerReport with KRS + 4B Framework

✅ **POST** `/reports/create`
- Create custom PlayerReport
- Input: Manual report data
- Output: PlayerReport ID

✅ **GET** `/sessions/{session_id}/report`
- Get report for a session (alias)

✅ **GET** `/sessions/latest`
- Get the most recent session report

✅ **GET** `/players/{player_id}/recommended-drills`
- Get personalized drill recommendations

---

### Reboot Motion Sync Service (`sync_service.py`)

✅ **Class**: `RebootMotionSync`
- OAuth 2.0 authentication with Reboot Motion API
- Methods:
  - `get_players()` - Fetch all players
  - `get_player(player_id)` - Fetch single player
  - `get_sessions(player_id, start_date, end_date)` - Fetch sessions
  - `get_session_data(session_id)` - Fetch biomechanics data
  - `sync_all_data()` - Full sync pipeline

**Environment Variables Required**:
- `REBOOT_USERNAME` - Reboot Motion username
- `REBOOT_PASSWORD` - Reboot Motion password

**Base URL**: `https://api.rebootmotion.com`

---

## 🎯 What Coach Rick Needs

### User Story
> As a coach using Coach Rick AI, I want to:
> 1. **Search for a player** by name (from Reboot Motion database)
> 2. **View their recent sessions** from Reboot Motion
> 3. **Click "Generate KRS Report"** on any session
> 4. **See the KRS Hero + 4B Framework cards** appear instantly
> 5. **No video upload required** - data comes from Reboot API

### Current State
- ❌ Coaches must upload videos manually
- ❌ No way to access existing Reboot Motion data
- ❌ Can't view past sessions or player history

### Target State
- ✅ Player search box (autocomplete)
- ✅ Recent sessions list per player
- ✅ One-click "Generate KRS Report" button
- ✅ Reuse existing KRS Hero + 4B cards display
- ✅ Integration with `/api/reports/from-reboot` endpoint

---

## 🔧 Implementation Plan

### Step 1: Add Backend Endpoint (if needed)
**Status**: ✅ Already exists! `/reports/from-coach-rick` can handle Reboot data

### Step 2: Add Player Search Endpoint
**New endpoint needed**: `GET /api/reboot/players/search?query={name}`

```python
# Add to session_api.py or create reboot_api.py
@router.get("/reboot/players/search")
async def search_reboot_players(query: str):
    """Search for players in Reboot Motion database"""
    from sync_service import RebootMotionSync
    
    sync = RebootMotionSync()
    players = sync.get_players()
    
    # Filter by name
    filtered = [
        p for p in players
        if query.lower() in f"{p['first_name']} {p['last_name']}".lower()
    ]
    
    return {'players': filtered[:10]}  # Top 10 matches
```

### Step 3: UI Components
**Location**: `templates/coach_rick_analysis.html`

**Add above the existing Upload section**:

```html
<!-- ========================================
     REBOOT MOTION INTEGRATION (NEW!)
     ======================================== -->
<div class="reboot-integration-section">
    <h2>🔄 Import from Reboot Motion</h2>
    <p>Search for a player and generate KRS reports from existing sessions</p>
    
    <!-- Player Search -->
    <div class="player-search-box">
        <input type="text" id="playerSearch" placeholder="Search player name..." />
        <div id="playerResults" class="player-results"></div>
    </div>
    
    <!-- Sessions List (shows after player selected) -->
    <div id="sessionsList" class="sessions-list" style="display:none;">
        <h3>Recent Sessions</h3>
        <div id="sessionsContainer"></div>
    </div>
</div>

<div class="upload-divider">
    <span>OR</span>
</div>

<!-- Existing Upload Section -->
<div class="upload-section">
    <!-- existing upload form -->
</div>
```

### Step 4: JavaScript Functions

```javascript
// Search players
async function searchPlayers(query) {
    if (query.length < 2) return;
    
    const response = await fetch(`/api/reboot/players/search?query=${encodeURIComponent(query)}`);
    const data = await response.json();
    
    displayPlayerResults(data.players);
}

// Display player search results
function displayPlayerResults(players) {
    const container = document.getElementById('playerResults');
    container.innerHTML = players.map(p => `
        <div class="player-card" onclick="loadPlayerSessions('${p.reboot_player_id}', '${p.first_name} ${p.last_name}')">
            <strong>${p.first_name} ${p.last_name}</strong>
            <span>${p.date_of_birth || 'N/A'}</span>
        </div>
    `).join('');
}

// Load sessions for selected player
async function loadPlayerSessions(playerId, playerName) {
    const response = await fetch(`/api/players/${playerId}/sessions?limit=10`);
    const data = await response.json();
    
    document.getElementById('sessionsList').style.display = 'block';
    displaySessions(data.sessions, playerName);
}

// Display sessions with "Generate KRS Report" button
function displaySessions(sessions, playerName) {
    const container = document.getElementById('sessionsContainer');
    container.innerHTML = `
        <h4>${playerName}'s Sessions</h4>
        ${sessions.map(s => `
            <div class="session-card">
                <div class="session-info">
                    <strong>Session ${s.session_number}</strong>
                    <span>${formatDate(s.session_date)}</span>
                    <span>KRS: ${s.krs_total?.toFixed(1) || 'N/A'}</span>
                </div>
                <button onclick="generateKRSFromReboot('${s.session_id}')">
                    Generate KRS Report
                </button>
            </div>
        `).join('')}
    `;
}

// Generate KRS Report from Reboot session
async function generateKRSFromReboot(sessionId) {
    try {
        // Fetch session report
        const response = await fetch(`/api/sessions/${sessionId}/report`);
        const report = await response.json();
        
        // Display using existing functions
        displayKRS(report, sessionId);
        display4BCards(report);
        
        // Scroll to results
        document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        console.error('Error generating report:', error);
        alert('Failed to generate KRS Report. Please try again.');
    }
}

// Format date helper
function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    });
}
```

### Step 5: CSS Styling

```css
.reboot-integration-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    padding: 30px;
    color: white;
    margin-bottom: 30px;
}

.player-search-box {
    position: relative;
    margin-top: 20px;
}

.player-search-box input {
    width: 100%;
    padding: 15px;
    border-radius: 8px;
    border: none;
    font-size: 16px;
}

.player-results {
    background: white;
    color: #333;
    border-radius: 8px;
    margin-top: 10px;
    max-height: 300px;
    overflow-y: auto;
}

.player-card {
    padding: 15px;
    border-bottom: 1px solid #eee;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
}

.player-card:hover {
    background: #f5f5f5;
}

.sessions-list {
    background: white;
    color: #333;
    border-radius: 12px;
    padding: 20px;
    margin-top: 20px;
}

.session-card {
    background: #f9f9f9;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.session-card button {
    background: #667eea;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
}

.session-card button:hover {
    background: #5568d3;
}

.upload-divider {
    text-align: center;
    position: relative;
    margin: 30px 0;
}

.upload-divider span {
    background: white;
    padding: 0 20px;
    color: #999;
    font-weight: 600;
}

.upload-divider::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    height: 1px;
    background: #ddd;
    z-index: -1;
}
```

---

## ✅ Testing Checklist

### Local Testing
1. ✅ Run server: `python coach_rick_wap_integration.py`
2. ✅ Open: `http://localhost:8000/coach-rick-analysis`
3. ✅ Search for "Eric Williams"
4. ✅ Select player from results
5. ✅ View sessions list
6. ✅ Click "Generate KRS Report"
7. ✅ Verify KRS Hero + 4B cards appear

### Railway Testing
1. ✅ Commit and push changes
2. ✅ Wait for Railway deployment
3. ✅ Test at: `https://reboot-motion-backend-production.up.railway.app/coach-rick-analysis`

---

## 📦 Deliverables

- ✅ **Documentation**: `docs/REBOOT_API_INTEGRATION.md` (this file)
- 🔲 **Backend Endpoint**: `GET /api/reboot/players/search` (add to `session_api.py`)
- 🔲 **UI Update**: `templates/coach_rick_analysis.html` (Player Search + Sessions)
- 🔲 **JavaScript**: Search, load sessions, generate KRS functions
- 🔲 **CSS**: Styling for new UI components
- 🔲 **Git Commit**: With detailed commit message

---

## ⏰ Timeline Estimate

| Task | Time | Status |
|------|------|--------|
| Verify endpoints | 15 min | ✅ Complete |
| Document API | 15 min | ✅ Complete |
| Add search endpoint | 30 min | 🔲 Next |
| Build UI HTML | 30 min | 🔲 Pending |
| Wire JavaScript | 45 min | 🔲 Pending |
| Add CSS styling | 30 min | 🔲 Pending |
| Local testing | 30 min | 🔲 Pending |
| Commit & push | 5 min | 🔲 Pending |
| **TOTAL** | **~3 hours** | |

---

## 🎉 Success Criteria

✅ Coaches can search for players by name  
✅ Recent sessions display for selected player  
✅ One-click "Generate KRS Report" button works  
✅ KRS Hero + 4B cards appear (reuse existing display)  
✅ No video upload required  
✅ Integration with Reboot Motion API complete  

---

**Next Step**: Implement the player search endpoint and UI components!
