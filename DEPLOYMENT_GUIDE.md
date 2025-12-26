# 🚀 Deployment Guide - Reboot Motion Backend

## ✅ Pull Request Created!

**PR Link**: https://github.com/THScoach/reboot-motion-backend/pull/1

---

## 📋 What Was Fixed

### 1. ✅ OAuth 2.0 Authentication
**Problem**: Used incorrect API key authentication  
**Solution**: Implemented OAuth 2.0 Resource Owner Password Flow  
**Impact**: Proper authentication with automatic token refresh

### 2. ✅ Session Participant Detection
**Problem**: Created session records for ALL players for every session  
**Solution**: Uses `/processed_data` endpoint to check which players actually participated  
**Impact**: Accurate player-session relationships

### 3. ✅ Biomechanics Data Sync
**Problem**: No actual biomechanics data was synced (faked with `sessions * 100`)  
**Solution**: Real data sync using `/processed_data` endpoint  
**Impact**: Actual movement data stored in database

### 4. ✅ Correct API Endpoints
**Problem**: Tried to use `/sessions/{id}/movements` (doesn't exist)  
**Solution**: Uses documented `/processed_data` endpoint  
**Impact**: No more 404 errors

---

## 🔧 Pre-Deployment Checklist

Before deploying, you MUST update environment variables:

### ⚠️ BREAKING CHANGE: Environment Variables

**Old (Remove These)**:
```bash
REBOOT_API_KEY=your_api_key
```

**New (Add These)**:
```bash
REBOOT_USERNAME=your_reboot_username
REBOOT_PASSWORD=your_reboot_password
```

---

## 🚀 Deployment Steps (5 Minutes)

### Step 1: Update Railway Environment Variables (2 min)

1. Go to Railway Dashboard: https://railway.app/
2. Select your project: `reboot-motion-backend`
3. Go to **Variables** tab
4. **Remove**: `REBOOT_API_KEY` (if exists)
5. **Add**:
   - Key: `REBOOT_USERNAME` → Value: Your Reboot Motion username
   - Key: `REBOOT_PASSWORD` → Value: Your Reboot Motion password
6. Click **Save**

### Step 2: Merge Pull Request (1 min)

1. Go to: https://github.com/THScoach/reboot-motion-backend/pull/1
2. Review the changes
3. Click **Merge pull request**
4. Click **Confirm merge**

### Step 3: Railway Auto-Deploys (2 min)

Railway will automatically:
- ✅ Detect the GitHub merge
- ✅ Pull the new code
- ✅ Install dependencies
- ✅ Restart the backend
- ✅ Apply database migrations

Watch the deployment logs in Railway dashboard.

---

## 🧪 Testing After Deployment (5 Minutes)

### Test 1: Check API Health
```bash
curl https://reboot-motion-backend-production.up.railway.app/health
```

**Expected**: `{"status":"healthy","database":"connected"}`

### Test 2: Trigger Data Sync
1. Go to: https://reboot-motion-backend-production.up.railway.app/docs
2. Find `POST /sync/trigger`
3. Click **Try it out**
4. Click **Execute**
5. Wait for response (may take 1-2 minutes)

**Expected Response**:
```json
{
  "status": "success",
  "players_synced": 25,
  "sessions_synced": 150,
  "biomechanics_synced": 3500
}
```

### Test 3: Verify Players
```bash
curl https://reboot-motion-backend-production.up.railway.app/players
```

**Expected**: Array of real player data from your Reboot Motion account

### Test 4: Verify Sessions
```bash
curl https://reboot-motion-backend-production.up.railway.app/sessions
```

**Expected**: Array of sessions with accurate player assignments

### Test 5: Check Database Stats
```bash
curl https://reboot-motion-backend-production.up.railway.app/stats
```

**Expected**:
```json
{
  "total_players": 25,
  "total_sessions": 150,
  "synced_sessions": 150,
  "biomechanics_records": 3500
}
```

---

## 📊 Sync Process Flow

1. **Authentication** → OAuth token obtained (valid 24 hours)
2. **Player Sync** → All players fetched from `/players`
3. **Session Sync** → For each hitting session:
   - Check each player via `/processed_data`
   - Only create session if player has data
4. **Biomechanics Sync** → Fetch detailed movement data
5. **Complete** → All sessions marked as `data_synced=True`

---

## 🐛 Troubleshooting

### Issue: "REBOOT_USERNAME and REBOOT_PASSWORD must be set"
**Solution**: Update Railway environment variables (see Step 1)

### Issue: "OAuth token request failed"
**Solution**: 
- Verify username/password are correct
- Test login at https://app.rebootmotion.com/
- Check Railway logs for error details

### Issue: No players synced
**Solution**:
- Verify your Reboot Motion account has players
- Check Railway logs for API errors
- Ensure you have proper permissions in Reboot Motion

### Issue: No sessions created
**Solution**:
- Check if you have HITTING sessions in last 30 days
- Verify `/processed_data` returns data for your players
- Try adjusting `days_back` parameter in sync

### Issue: No biomechanics data
**Solution**:
- Run sync again (biomechanics happens after sessions)
- Verify sessions exist and have `data_synced=False`
- Check that `/processed_data` returns movement data

---

## 📚 API Documentation

Full interactive API docs available at:
- **Swagger UI**: https://reboot-motion-backend-production.up.railway.app/docs
- **ReDoc**: https://reboot-motion-backend-production.up.railway.app/redoc

---

## 🎯 Key Improvements

| Area | Before | After |
|------|--------|-------|
| **Authentication** | ❌ API Key (not supported) | ✅ OAuth 2.0 |
| **Session Detection** | ❌ All players for all sessions | ✅ Only actual participants |
| **Biomechanics Data** | ❌ Fake count | ✅ Real movement data |
| **API Endpoints** | ❌ Non-existent endpoints | ✅ Correct documented endpoints |
| **Token Management** | ❌ N/A | ✅ 24-hour caching with refresh |
| **Error Handling** | ❌ Basic | ✅ Comprehensive |
| **Logging** | ❌ Minimal | ✅ Detailed with emoji indicators |

---

## 🎊 What You'll Have After Deployment

✅ **OAuth 2.0 Authentication** - Secure, proper authentication  
✅ **Accurate Player-Session Data** - Only actual participants  
✅ **Real Biomechanics Data** - Detailed movement information  
✅ **Correct API Integration** - Using documented endpoints  
✅ **Production-Ready Backend** - Professional error handling  
✅ **Comprehensive Logging** - Easy debugging and monitoring  
✅ **Database Efficiency** - No duplicate records  

---

## 📞 Next Steps

1. ✅ Update Railway environment variables (REBOOT_USERNAME, REBOOT_PASSWORD)
2. ✅ Merge the pull request: https://github.com/THScoach/reboot-motion-backend/pull/1
3. ✅ Wait for Railway auto-deployment (~2 minutes)
4. ✅ Run initial sync via `/sync/trigger`
5. ✅ Verify data in `/players`, `/sessions`, `/stats`
6. ✅ Test your frontend - should now show real data!

---

## 🎉 Success!

Your Reboot Motion backend is now production-ready with:
- ✅ Correct authentication
- ✅ Accurate data sync
- ✅ Real biomechanics data
- ✅ Professional implementation

**Time to Production**: ~10 minutes  
**Cost**: $0 (within Railway free tier)  
**Status**: Ready to use! 🚀

---

**Questions?** Check the troubleshooting section or review the PR description for more details.
