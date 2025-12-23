# 🔧 Quick Reference - API Changes

## Environment Variables (BREAKING CHANGE)

### ❌ OLD (Remove)
```bash
REBOOT_API_KEY=abc123xyz
```

### ✅ NEW (Required)
```bash
REBOOT_USERNAME=your_username
REBOOT_PASSWORD=your_password
```

---

## Key Code Changes

### 1. Authentication Method

**Before**:
```python
headers = {'X-Api-Key': api_key}
response = requests.get(url, headers=headers)
```

**After**:
```python
# Get OAuth token
token = get_access_token(username, password)
headers = {'Authorization': f'Bearer {token}'}
response = requests.get(url, headers=headers)
```

### 2. Session Participant Detection

**Before**:
```python
# Created sessions for ALL players (WRONG!)
for player in all_players:
    create_session(session_id, player_id)
```

**After**:
```python
# Check each player via /processed_data (CORRECT!)
for player in all_players:
    data = api.get('/processed_data', params={
        'session_id': session_id,
        'org_player_id': player.org_player_id
    })
    if data:  # Only if player has data
        create_session(session_id, player_id)
```

### 3. Biomechanics Data Sync

**Before**:
```python
# Faked the count (NO REAL DATA!)
biomechanics_synced = sessions_synced * 100
```

**After**:
```python
# Fetch real data from API
data = api.get('/processed_data', params={
    'session_id': session_id,
    'org_player_id': player.org_player_id
})
# Store actual movement data in database
save_biomechanics_data(data)
```

---

## API Endpoints

### ❌ Doesn't Exist
- `/sessions/{id}/movements` - 404 error

### ✅ Correct Endpoints
- `POST /oauth/token` - Get access token
- `GET /players` - List all players
- `GET /sessions` - List sessions
- `GET /processed_data` - Get player session data (KEY ENDPOINT!)

---

## Sync Process Flow

```
1. Authentication
   ↓
   POST /oauth/token → access_token
   
2. Player Sync
   ↓
   GET /players → sync to DB
   
3. Session Sync
   ↓
   GET /sessions → list sessions
   ↓
   For each session + player:
     GET /processed_data → check if has data
     ↓
     If yes: create session record
     
4. Biomechanics Sync
   ↓
   For unsynchronized sessions:
     GET /processed_data → fetch movement data
     ↓
     Store in BiomechanicsData table
     ↓
     Mark session as data_synced=True
```

---

## Database Schema Updates

### SyncLog Table (New Fields)
```python
players_synced = Column(Integer, default=0)      # NEW
sessions_synced = Column(Integer, default=0)     # NEW
biomechanics_synced = Column(Integer, default=0) # NEW
```

---

## Testing Commands

```bash
# 1. Health check
curl https://your-api.railway.app/health

# 2. Trigger sync
curl -X POST https://your-api.railway.app/sync/trigger

# 3. Get players
curl https://your-api.railway.app/players

# 4. Get sessions
curl https://your-api.railway.app/sessions

# 5. Get stats
curl https://your-api.railway.app/stats

# 6. Get session data
curl https://your-api.railway.app/sessions/1/data
```

---

## Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| "REBOOT_USERNAME not set" | Add env vars in Railway |
| "OAuth failed" | Check username/password |
| "No players synced" | Verify Reboot account has players |
| "No sessions created" | Check if you have recent hitting sessions |
| "No biomechanics data" | Run sync again, check logs |

---

## Pull Request

**Link**: https://github.com/THScoach/reboot-motion-backend/pull/1

**Files Changed**:
- ✅ `sync_service.py` - Complete rewrite
- ✅ `main.py` - Updated env vars
- ✅ `models.py` - Enhanced SyncLog
- ✅ `README.md` - New docs
- ✅ `.gitignore` - Added

---

## Deployment Checklist

- [ ] Update Railway env vars (REBOOT_USERNAME, REBOOT_PASSWORD)
- [ ] Merge PR #1
- [ ] Wait for Railway deployment
- [ ] Test `/health` endpoint
- [ ] Run `/sync/trigger`
- [ ] Verify `/players` has data
- [ ] Check `/stats` for counts
- [ ] Test frontend

---

**Ready to deploy!** Follow DEPLOYMENT_GUIDE.md for detailed instructions.
