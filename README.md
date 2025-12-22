# 🏏 Reboot Motion Athlete Analytics Backend

## 🎯 Production-Ready API with Real-Time Data Sync

Complete FastAPI backend that syncs player, session, and biomechanics data from Reboot Motion API.

---

## 🔑 **Environment Variables Required**

Create a `.env` file or set these in your Railway/hosting environment:

```bash
# Database (automatically set by Railway PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Reboot Motion API Credentials (REQUIRED)
REBOOT_USERNAME=your_reboot_username
REBOOT_PASSWORD=your_reboot_password
```

**⚠️ IMPORTANT**: The API now uses OAuth 2.0 authentication. You MUST set `REBOOT_USERNAME` and `REBOOT_PASSWORD` instead of `REBOOT_API_KEY`.

---

## 📦 **Project Files:**

**7 Production Files:**

1. ✅ **main.py**
   - FastAPI app with PostgreSQL integration
   - All endpoints connect to real database
   - Production error handling & logging

2. ✅ **models.py**
   - SQLAlchemy ORM models
   - Player, Session, BiomechanicsData, SyncLog tables
   - Relationships and indexes

3. ✅ **database.py**
   - Database connection management
   - Connection pooling
   - Auto table creation

4. ✅ **sync_service.py** (UPDATED!)
   - ✅ OAuth 2.0 authentication (username/password)
   - ✅ Correct session participant detection via /processed_data
   - ✅ Real biomechanics data sync
   - ✅ Accurate player-session relationships
   - ✅ Comprehensive error handling and logging

5. ✅ **requirements.txt**
   - All Python dependencies
   - PostgreSQL drivers
   - Updated versions

6. ✅ **Procfile** & **railway.json**
   - Railway deployment config
   - Auto-deployment settings

---

## 🚀 **Deployment to Railway (10 Minutes):**

### **Prerequisites**
Before deploying, ensure you have:
- Your Reboot Motion username and password
- GitHub repository ready
- Railway account connected to GitHub

### **Step 1: Set Environment Variables in Railway (2 min)**
**CRITICAL**: Set these environment variables in Railway BEFORE deployment:

1. Go to Railway Dashboard → Your Project → Variables
2. Add these variables:
   ```
   REBOOT_USERNAME=your_reboot_username
   REBOOT_PASSWORD=your_reboot_password
   ```
3. DATABASE_URL is automatically set by Railway PostgreSQL

### **Step 2: Upload to GitHub (3 min)**
Go to: https://github.com/YOUR_USERNAME/YOUR_REPO

1. Click "Add file" → "Upload files"
2. Upload all 7 files
3. Commit: "Fixed API sync with OAuth 2.0 and correct endpoints"

### **Step 3: Railway Auto-Deploys (3 min)**
Railway automatically:
- Detects changes
- Installs dependencies
- Connects to PostgreSQL
- Creates database tables
- Starts API

### **Step 4: Run Initial Sync (2 min)**
Visit: `https://your-app.up.railway.app/docs`

1. Find "POST /sync/trigger"
2. Click "Try it out"
3. Click "Execute"
4. Wait for sync to complete (watch the logs!)

### **Step 5: Verify (1 min)**
Visit: `https://your-app.up.railway.app/players`

**You should see all your real athletes!** ✅

---

## 🔧 **What Was Fixed:**

### **Issue #1: Authentication Method** ✅ FIXED
- **Before**: Used API key authentication (X-Api-Key header)
- **After**: OAuth 2.0 Resource Owner Password Flow
- **Impact**: Proper authentication with access token refresh

### **Issue #2: Session Participant Assignment** ✅ FIXED
- **Before**: Created session records for ALL players for every session
- **After**: Uses `/processed_data` endpoint to determine actual participants
- **Impact**: Accurate player-session relationships

### **Issue #3: Missing Biomechanics Data** ✅ FIXED
- **Before**: Faked count with `sessions_synced * 100`
- **After**: Real data sync using `/processed_data` endpoint
- **Impact**: Actual biomechanics data stored in database

### **Issue #4: Non-Existent Endpoints** ✅ FIXED
- **Before**: Tried to use `/sessions/{id}/movements` (doesn't exist)
- **After**: Uses correct `/processed_data` endpoint
- **Impact**: No more 404 errors, proper data retrieval

---

## 📊 **How It Works Now:**

### **1. Authentication**
```python
# OAuth 2.0 token request
POST /oauth/token
Body: {"username": "...", "password": "..."}
Response: {"access_token": "...", "refresh_token": "..."}
```

### **2. Player Sync**
```python
GET /players
# Syncs all players in organization
```

### **3. Session Sync (Smart Detection)**
```python
# For each session:
for session in hitting_sessions:
    for player in players:
        # Check if player has data for this session
        GET /processed_data?session_id=X&movement_type_id=1&org_player_id=Y
        # Only creates session record if data exists
```

### **4. Biomechanics Data Sync**
```python
# For each session without data:
GET /processed_data?session_id=X&movement_type_id=1&org_player_id=Y
# Stores detailed movement data in BiomechanicsData table
```

---

## 🎯 **API Endpoints:**

### **GET /players**
List all players with their information

### **GET /players/{player_id}**
Get specific player details

### **GET /sessions**
List all sessions with optional filters

### **GET /sessions/{session_id}**
Get specific session details

### **GET /sessions/{session_id}/biomechanics**
Get biomechanics data for a session

### **POST /sync/trigger**
Manually trigger data sync

### **GET /sync/status**
Check sync status and history

---

## 💾 **Database Schema:**

### **Players Table**
- org_player_id (unique)
- reboot_player_id
- first_name, last_name
- date_of_birth
- height_ft, weight_lbs
- dominant_hand_hitting, dominant_hand_throwing

### **Sessions Table**
- session_id (unique)
- player_id (foreign key)
- session_date
- movement_type_id, movement_type_name
- data_synced (boolean)

### **BiomechanicsData Table**
- session_id (foreign key)
- frame_number
- timestamp
- joint_angles (JSON)
- joint_positions (JSON)
- joint_velocities (JSON)

### **SyncLog Table**
- sync_type
- status
- records_synced
- error_message
- started_at, completed_at

---

## 💰 **COST:**

**Still FREE!**
- ✅ Railway PostgreSQL: Free tier (512 MB)
- ✅ Railway Backend: $5 free credit/month
- ✅ Netlify Frontend: FREE
- ✅ Total: $0/month (within free limits)

---

## 📊 **AFTER DEPLOYMENT:**

**Your app will show:**
- ✅ Real athlete names
- ✅ Real session dates
- ✅ Real movement types (Pitching, Hitting, etc.)
- ✅ Actual data from Reboot Motion
- ✅ Professional production app!

**Frontend automatically works** - no changes needed!

---

## 🎊 **What You've Built:**

**Complete Production App:**
1. ✅ Professional frontend (Netlify)
2. ✅ Production backend API (Railway)
3. ✅ PostgreSQL database (Railway)
4. ✅ OAuth 2.0 authentication (Reboot Motion)
5. ✅ Accurate data sync with correct endpoints
6. ✅ Real biomechanics data storage
7. ✅ Full CRUD operations
8. ✅ Error handling & logging
9. ✅ Ready to use!

---

## 🐛 **Troubleshooting:**

### **Issue: Authentication Failed**
- ✅ Verify `REBOOT_USERNAME` and `REBOOT_PASSWORD` are set correctly in Railway
- ✅ Check credentials work on https://app.rebootmotion.com/

### **Issue: No Players Synced**
- ✅ Check Railway logs for API errors
- ✅ Verify your Reboot Motion account has players
- ✅ Ensure DATABASE_URL is set correctly

### **Issue: No Sessions Created**
- ✅ Check if you have HITTING sessions in last 30 days
- ✅ Verify players have processed data available
- ✅ Check Railway logs for `/processed_data` errors

### **Issue: No Biomechanics Data**
- ✅ Run sync again (biomechanics sync happens after sessions)
- ✅ Check that sessions have `data_synced=False`
- ✅ Verify `/processed_data` endpoint returns data

---

## 📝 **Testing the API:**

### **Test 1: Check Health**
```bash
curl https://your-app.up.railway.app/
# Should return: {"status": "ok", "message": "Reboot Motion API is running"}
```

### **Test 2: Trigger Sync**
```bash
curl -X POST https://your-app.up.railway.app/sync/trigger
# Should return sync results
```

### **Test 3: Get Players**
```bash
curl https://your-app.up.railway.app/players
# Should return array of players
```

### **Test 4: Get Sessions**
```bash
curl https://your-app.up.railway.app/sessions
# Should return array of sessions
```

---

## 🔄 **Sync Process Flow:**

1. **Authentication** → Get OAuth access token (valid 24 hours)
2. **Player Sync** → Fetch all players from `/players`
3. **Session Sync** → Fetch hitting sessions, check each player via `/processed_data`
4. **Biomechanics Sync** → Fetch detailed movement data via `/processed_data`
5. **Mark Complete** → Set `data_synced=True` for synced sessions

---

## 📚 **API Documentation:**

Full API documentation is available at:
- **Swagger UI**: `https://your-app.up.railway.app/docs`
- **ReDoc**: `https://your-app.up.railway.app/redoc`

---

## 🎯 **Key Improvements:**

✅ **OAuth 2.0 Authentication** - Secure token-based auth  
✅ **Smart Session Detection** - Only creates records for actual participants  
✅ **Real Biomechanics Data** - Fetches and stores detailed movement data  
✅ **Correct API Endpoints** - Uses `/processed_data` as documented  
✅ **Token Caching** - Reuses tokens until expiration (24 hours)  
✅ **Error Handling** - Graceful handling of missing data  
✅ **Comprehensive Logging** - Detailed logs for debugging  
✅ **Database Efficiency** - Avoids duplicate records  

---

## 🚀 **Ready to Deploy!**

Your backend is now production-ready with:
- ✅ Correct authentication
- ✅ Accurate data sync
- ✅ Real biomechanics data
- ✅ Proper error handling

**Next Steps:**
1. Set environment variables in Railway
2. Push code to GitHub
3. Wait for Railway deployment
4. Run initial sync
5. Verify data in `/players` endpoint
6. 🎉 Enjoy your production app!
