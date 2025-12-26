# 🚀 RAILWAY DEPLOYMENT INSTRUCTIONS

## Quick Deploy Steps:

### Option 1: Railway Dashboard (FASTEST)
1. Go to: https://railway.app/dashboard
2. Find project: `reboot-motion-backend`
3. Click "Settings" → "Deploy"
4. Railway will pull latest commit from GitHub
5. Wait ~2-3 minutes for deployment

### Option 2: GitHub Push (AUTO-DEPLOY)
If Railway is connected to GitHub repo:

```bash
# The code is already committed on branch: add-data-export-endpoint
# You need to either:

# A) Merge to main via GitHub UI
# B) Or push directly (if you have access)
```

---

## After Deployment - Verify It Worked:

### 1. Check Endpoint is Live:
```bash
curl "https://reboot-motion-backend-production.up.railway.app/"
```

**Expected Response:**
```json
{
  "endpoints": {
    "reboot_data_export": "/reboot/data-export/{session_id}"  ← NEW
  }
}
```

### 2. Test Data Export:
```bash
curl "https://reboot-motion-backend-production.up.railway.app/reboot/data-export/6764e74b-516d-45eb-a8a9-c50a069ef50d"
```

**Expected:** Full biomechanics JSON (~50-100 KB)

---

## If Deployment Fails:

### Check Railway Logs:
1. Go to Railway dashboard
2. Click on deployment
3. Check logs for errors

### Common Issues:
- OAuth credentials missing → Check `REBOOT_USERNAME` and `REBOOT_PASSWORD` env vars
- Import error → Check `requests` is in requirements.txt
- Timeout → Increase request timeout in Railway settings

---

## What's Changed:

### New Files in Repo:
```
main.py  ← Modified (added Data Export endpoint)
DATA_EXPORT_ENDPOINT_ADDED.md
REBOOT_DATA_EXPORT_PLAN.md
test_reboot_data.py
CRITICAL_BUGS_FOUND.md
```

### Git Status:
```
Branch: add-data-export-endpoint
Commits:
  - 2246e1d: feat: Add Reboot Motion Data Export endpoint
  - 70e0aae: docs: Add deployment guide
```

---

## Manual Deployment Alternative:

If Railway isn't auto-deploying, you can manually trigger:

### Via Railway CLI:
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Via Git Push:
```bash
cd /home/user/webapp
git checkout main
git merge add-data-export-endpoint
git push origin main
```

---

## Once Deployed - IMMEDIATE TEST:

Run this command to verify:
```bash
curl -s "https://reboot-motion-backend-production.up.railway.app/reboot/data-export/6764e74b-516d-45eb-a8a9-c50a069ef50d" | head -50
```

**If you see JSON data** → ✅ SUCCESS!

**If you see error** → Check Railway logs and let me know the error message.

---

## What We'll Do Next:

Once endpoint is working:
1. Pull Ronald Acuna's biomechanics
2. Examine data structure
3. Compare to our MediaPipe calculations
4. Calibrate physics engine
5. Fix event detection
6. Re-test with Shohei video

---

**Deploy now and let me know when it's live so we can test it!** 🎯
