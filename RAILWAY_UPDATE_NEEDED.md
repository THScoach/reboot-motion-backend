# 🚨 RAILWAY DEPLOYMENT UPDATE NEEDED

## Current Situation:

**Railway is running OLD code:**
- Commit: `eda59399` (Dec 22, 7:00 PM)
- This is BEFORE our Data Export endpoint was added

**Latest code in this session:**
- Commit: `2246e1d` - Data Export endpoint added
- Commit: `70e0aae` - Deployment guide
- Branch: `add-data-export-endpoint`

**Result:** The new endpoint doesn't exist on Railway yet.

---

## TO UPDATE RAILWAY WITH NEW CODE:

### Step 1: Push Latest Code to GitHub

Railway is connected to your GitHub repo and auto-deploys from `main` branch.

**Option A - Merge via GitHub UI:**
1. Go to: https://github.com/THScoach/reboot-motion-backend
2. Look for branch: `add-data-export-endpoint`
3. Click "Compare & pull request"
4. Review changes (should show `main.py` with new endpoint)
5. Click "Merge pull request"
6. Railway will auto-deploy in 2-3 minutes

**Option B - Push via Git (if authenticated):**
```bash
cd /home/user/webapp
git checkout main
git merge add-data-export-endpoint
git push origin main
```

### Step 2: Wait for Railway to Deploy

Railway Activity will show:
```
reboot-motion-backend
Deployment successful
Just now
```

### Step 3: Verify New Endpoint

```bash
curl "https://reboot-motion-backend-production.up.railway.app/"
```

**Should now show:**
```json
{
  "endpoints": {
    "reboot_data_export": "/reboot/data-export/{session_id}"  ← NEW!
  }
}
```

---

## Alternative: Manual Redeploy in Railway

If you can't push to GitHub:

1. **Go to Railway Dashboard** → `reboot-motion-backend`
2. **Settings** → **GitHub** → Check which branch is connected
3. **Make sure it's pointing to the right repo/branch**
4. **Click "Redeploy"** (but this won't help if code isn't in GitHub)

---

## What's Happening:

Railway watches your GitHub repo for changes. When you push to `main`, it automatically:
1. Pulls latest code
2. Rebuilds Docker image
3. Deploys new version
4. Takes ~2-3 minutes

**But:** Our new code is only in this sandbox session, not in GitHub yet.

---

## Quick Check - Is Code in GitHub?

Go to: https://github.com/THScoach/reboot-motion-backend/blob/main/main.py

**Search for:** `reboot/data-export`

**If you see it:** Railway should pick it up if you trigger redeploy
**If you don't see it:** Need to push the branch first

---

## After Deployment Works:

Once Railway shows the new endpoint, immediately test:

```bash
# Test endpoint exists
curl "https://reboot-motion-backend-production.up.railway.app/" | grep reboot_data_export

# Pull real biomechanics
curl "https://reboot-motion-backend-production.up.railway.app/reboot/data-export/6764e74b-516d-45eb-a8a9-c50a069ef50d"
```

Then we can:
1. ✅ Analyze pro player biomechanics structure
2. ✅ Compare to our MediaPipe calculations
3. ✅ Calibrate physics engine with real data
4. ✅ Fix event detection
5. ✅ Re-test and validate

---

**Bottom line:** Need to get the latest code from this sandbox session into GitHub main branch, then Railway will auto-deploy it. 

Can you access GitHub to create a PR or push the branch?
