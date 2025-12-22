# Fix Session Sync - Use Movements to Match Players

## Problem
The Reboot Motion API doesn't have a `/players/{id}/sessions` endpoint. All 100 players returned 404 errors.

## Root Cause
Based on Robert's email and API testing:
- ✅ `/players` endpoint works (100 players synced)
- ✅ `/sessions` endpoint works (returns group sessions)
- ❌ `/players/{id}/sessions` doesn't exist
- ✅ `/sessions/{session_id}/movements` endpoint exists

## Solution
Updated `sync_sessions()` to use the correct API flow:

### New Approach:
1. **Fetch all sessions** from `/sessions` (returns ~100-200 sessions)
2. **For each session**, fetch movements from `/sessions/{session_id}/movements`
3. **Extract player IDs** from each movement (`movement.player_id`)
4. **Match movements to players** using `reboot_player_id`
5. **Create session records** for each player who participated

### Key Changes:
```python
# OLD (Wrong - endpoint doesn't exist)
sessions_data = self._make_request(f'/players/{player.reboot_player_id}/sessions')

# NEW (Correct - get all sessions, then check movements)
sessions_data = self._make_request('/sessions', params={'limit': 200})
movements_data = self._make_request(f'/sessions/{session_id}/movements')
```

## Deployment Steps

### Step 1: Update GitHub
1. Go to: https://github.com/THScoach/reboot-motion-backend/blob/main/sync_service.py
2. Click the pencil icon (Edit)
3. Select ALL code (Ctrl+A)
4. Delete it
5. Copy ALL code from `backend_production/sync_service.py` in GenSpark
6. Paste into GitHub editor
7. Commit with message: `Fix: Use movements endpoint to match sessions to players`

### Step 2: Wait for Railway Deployment
- Go to: https://railway.app/project/24d0cc9a-16f7-4ac7-b160-86cbce39edd0
- Wait 2-3 minutes for new deployment
- Status should show "Active"
- Logs should show: `INFO: Application startup complete`

### Step 3: Trigger Sync
1. Go to: https://reboot-motion-backend-production.up.railway.app/docs
2. Find `POST /sync/trigger`
3. Click "Try it out" → "Execute"

### Step 4: Expected Results
```json
{
  "status": "success",
  "message": "Data sync completed successfully",
  "players_synced": 100,
  "sessions_synced": 250,  // ← Should be > 0 now!
  "biomechanics_synced": 25000
}
```

**Expected logs:**
```
INFO:sync_service:🔄 Syncing sessions from global endpoint...
INFO:sync_service:📊 API returned 100 sessions
INFO:sync_service:📊 Built lookup for 100 players
INFO:sync_service:✅ Synced 250 player-session records
INFO:sync_service:📊 Checked 5000 movements across 100 sessions
```

## Why This Works

The Reboot Motion API uses a **session-centric** model:
- Sessions are group events (multiple players)
- Each session contains multiple movements
- Each movement belongs to one player
- Player participation is determined by their movements

This is the correct way to sync data:
```
/sessions → Get all sessions
  ↓
/sessions/{id}/movements → Get movements for each session
  ↓
movement.player_id → Match to players in database
  ↓
Create SessionModel record for each (player, session) pair
```

## API Endpoints Used
- ✅ `GET /players` - Get all players
- ✅ `GET /sessions?limit=200` - Get recent sessions
- ✅ `GET /sessions/{session_id}/movements?limit=100` - Get movements per session
- ❌ `GET /players/{id}/sessions` - Doesn't exist (404)

## Benefits of This Approach
1. **Accurate**: Uses actual movement data to determine participation
2. **Efficient**: Fetches sessions once, then processes movements
3. **Scalable**: Can handle any number of players per session
4. **Robust**: Handles group sessions correctly
