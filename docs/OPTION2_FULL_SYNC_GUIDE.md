# Option 2: Full Data Sync - Complete Guide

**Date**: 2025-12-26  
**Status**: READY TO RUN  
**Method**: Sync all Reboot Motion data to PostgreSQL

---

## 🎯 What This Does

**Full Data Sync** will:
1. ✅ Sync all 100+ players from Reboot Motion
2. ✅ Sync all sessions (with participant detection)
3. ✅ Sync all biomechanics data for each session
4. ✅ Store everything in your PostgreSQL database on Railway

**After sync**, you can:
- Search players instantly (no API calls)
- View all sessions for any player
- Generate KRS reports from biomechanics data
- Everything is cached and fast!

---

## 📋 Prerequisites

### 1. Railway PostgreSQL Database

You need a PostgreSQL database on Railway. Check if you have one:

1. Go to: https://railway.app
2. Open your `reboot-motion-backend` project
3. Look for a **PostgreSQL** service

**If you don't have PostgreSQL**:
- Click **"+ New"**
- Select **"Database"** → **"PostgreSQL"**
- Railway will provision it automatically

### 2. Environment Variables

These must be set in Railway:

| Variable | Value | Status |
|----------|-------|--------|
| `REBOOT_USERNAME` | `coachrickpd@gmail.com` | ✅ Set |
| `REBOOT_PASSWORD` | `Train@2025` | ✅ Set |
| `DATABASE_URL` | (PostgreSQL connection string) | ⚠️ Check |

**To check DATABASE_URL**:
1. Go to Railway dashboard
2. Click on your **PostgreSQL** service
3. Go to **"Variables"** tab
4. Copy the `DATABASE_URL` value
5. Add it to your **main service** variables

---

## 🚀 Method 1: Run Sync via API (Easiest)

Once deployed, trigger the sync with a single API call:

```bash
# Trigger full sync
curl -X POST https://reboot-motion-backend-production.up.railway.app/api/reboot/sync
```

**Response**:
```json
{
  "players_synced": 100,
  "sessions_synced": 45,
  "biomechanics_synced": 150,
  "status": "success"
}
```

**Note**: This can take 5-10 minutes for large datasets. Be patient!

---

## 🚀 Method 2: Run Sync Script Locally

If you want to run the sync from your local machine:

### **Step 1: Set Environment Variables**

```bash
export REBOOT_USERNAME='coachrickpd@gmail.com'
export REBOOT_PASSWORD='Train@2025'
export DATABASE_URL='postgresql://user:pass@host:5432/dbname'
```

### **Step 2: Run the Sync Script**

```bash
cd /home/user/webapp
python sync_reboot_data.py
```

### **Expected Output**:

```
======================================================================
🚀 REBOOT MOTION FULL DATA SYNC
======================================================================
Started: 2025-12-26 14:30:00

✅ Reboot Username: coachrickpd@gmail.com
✅ Database: PostgreSQL

======================================================================
PHASE 1: SYNC PLAYERS
======================================================================
🔄 Syncing players...
📋 Fetching players from Reboot Motion API...
✅ Fetched 100 players from Reboot Motion
✅ Synced 100 players

======================================================================
PHASE 2: SYNC SESSIONS
======================================================================
🔄 Syncing HITTING sessions (last 30 days)...
✅ Synced 45 sessions

======================================================================
PHASE 3: SYNC BIOMECHANICS
======================================================================
🔄 Syncing biomechanics data...
✅ Synced 150 biomechanics records

======================================================================
✅ SYNC COMPLETE!
======================================================================
Players synced:      100
Sessions synced:     45
Biomechanics synced: 150
Status:              success

Completed: 2025-12-26 14:45:00
======================================================================
```

---

## 🚀 Method 3: Run on Railway (Automated)

### **Option A: Manual Railway Shell**

1. Go to Railway dashboard
2. Click on your service
3. Go to **"Shell"** tab (or **"Deployments"** → **"Shell"**)
4. Run:
   ```bash
   python sync_reboot_data.py
   ```

### **Option B: Scheduled Sync** (Advanced)

Add a cron job to Railway to sync daily:

1. Create `railway.json`:
   ```json
   {
     "build": {
       "builder": "DOCKERFILE"
     },
     "deploy": {
       "healthcheckPath": "/health",
       "restartPolicyType": "ON_FAILURE"
     },
     "cron": [
       {
         "schedule": "0 2 * * *",
         "command": "python sync_reboot_data.py"
       }
     ]
   }
   ```

2. This runs sync every day at 2 AM UTC

---

## ✅ Verify Sync Worked

After running the sync, verify data is in the database:

### **Check Players**:
```bash
curl "https://reboot-motion-backend-production.up.railway.app/api/reboot/players/search?query=Connor"
```

### **Check Sessions for a Player**:
```bash
# Get Connor Gray's ID from search results
curl "https://reboot-motion-backend-production.up.railway.app/api/players/{player_id}/sessions"
```

### **Check Database Directly** (if you have access):
```sql
-- Count players
SELECT COUNT(*) FROM players;

-- Count sessions
SELECT COUNT(*) FROM sessions;

-- Count biomechanics records
SELECT COUNT(*) FROM biomechanics_data;

-- List recent sessions
SELECT * FROM sessions ORDER BY session_date DESC LIMIT 10;
```

---

## 📊 What Gets Synced

### **Players Table**
- `org_player_id` (your organization's player ID)
- `reboot_player_id` (Reboot Motion's player ID)
- `first_name`, `last_name`
- `date_of_birth`
- `height_ft`, `weight_lbs`
- `dominant_hand_hitting`, `dominant_hand_throwing`

### **Sessions Table**
- `session_id` (Reboot Motion session ID)
- `player_id` (linked to player)
- `session_date`
- `session_number`
- `movement_type` (e.g., "baseball-hitting")

### **Biomechanics Data Table**
- `session_id` (linked to session)
- `player_id` (linked to player)
- `data_type` (e.g., "momentum-energy", "inverse-kinematics")
- `data_json` (full biomechanics data)

---

## 🔧 Troubleshooting

### **Error: "DATABASE_URL environment variable is not set"**

**Solution**: Add DATABASE_URL to Railway:
1. Go to Railway PostgreSQL service
2. Copy the `DATABASE_URL` from Variables tab
3. Add it to your main service Variables

### **Error: "REBOOT_USERNAME and REBOOT_PASSWORD must be set"**

**Solution**: Add credentials to Railway:
```
REBOOT_USERNAME = coachrickpd@gmail.com
REBOOT_PASSWORD = Train@2025
```

### **Sync Takes Too Long**

- Normal! Large datasets can take 10-15 minutes
- Watch the logs to see progress
- Sessions and biomechanics take longest

### **Sync Fails Halfway**

- Check Railway logs for specific error
- Verify database connection is stable
- Try syncing in smaller batches (modify `limit` parameters)

---

## 📈 Performance

**Estimated Sync Times**:
- 100 players: ~30 seconds
- 50 sessions: ~2-3 minutes  
- 200 biomechanics records: ~5-8 minutes

**Total**: ~10-15 minutes for full sync

**After sync**:
- Player search: <100ms
- Session lookup: <50ms
- Report generation: <1 second

---

## 🔄 How Often to Sync

**Recommended Schedule**:
- **Daily**: If you capture sessions daily
- **Weekly**: If sessions are less frequent
- **On-demand**: Trigger manually when needed

**Best Practice**:
- Sync overnight (2 AM UTC)
- Use Railway cron job for automation
- Manual trigger after big training sessions

---

## 📝 Next Steps After Sync

Once data is synced, you can:

1. **Search Players**: Already works with API
2. **View Sessions**: Query from PostgreSQL
3. **Generate KRS Reports**: Use biomechanics data
4. **Build UI**: Show player progress over time
5. **Analytics**: Run queries on historical data

---

## 🎯 Summary

**Option 2 Benefits**:
- ✅ All data cached locally
- ✅ Fast queries (no API delays)
- ✅ Works offline (after initial sync)
- ✅ Full biomechanics data available
- ✅ Can generate KRS reports

**Ready to run?** Pick a method above and start syncing! 🚀

---

**Questions? Issues?** Check the logs or review the code in:
- `sync_service.py` - Sync logic
- `sync_reboot_data.py` - Standalone script
- `session_api.py` - API endpoint
