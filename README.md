# 🚀 Reboot Motion Backend API

## ✅ **What This Is**

This is the backend REST API for the Reboot Motion Athlete App. It serves data to the frontend.

---

## 📦 **What's Included**

- ✅ **main.py** - FastAPI REST API with 13 endpoints
- ✅ **requirements.txt** - Python dependencies
- ✅ **Procfile** - Railway deployment configuration
- ✅ **railway.json** - Railway build settings

---

## 🎯 **API Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/players` | GET | List all players |
| `/players/{id}` | GET | Get player details |
| `/players/{id}/sessions` | GET | Get player's sessions |
| `/sessions/{id}` | GET | Get session details |
| `/sessions/{id}/data` | GET | Get biomechanics data |
| `/sessions/{id}/metrics` | GET | Get session metrics |
| `/sync/status` | GET | Check sync status |
| `/sync/trigger` | POST | Trigger manual sync |
| `/docs` | GET | Interactive API docs (Swagger UI) |

---

## 🚀 **DEPLOYMENT TO RAILWAY.APP**

### **Step 1: Sign Up for Railway**

1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign up with GitHub (free)

### **Step 2: Create New Project**

1. Click "New Project"
2. Select "Empty Project"
3. Name it: "reboot-motion-api"

### **Step 3: Deploy from Local**

**Option A: Upload Files**
1. Click "Deploy from GitHub repo"
2. OR click "Deploy from local"
3. Select this backend folder
4. Railway will auto-detect Python and deploy

**Option B: Use Railway CLI**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# Deploy
railway up
```

### **Step 4: Add Environment Variables (Optional)**

In Railway dashboard, go to Variables and add:
- `REBOOT_API_KEY` - Your Reboot Motion API key (if you want real data)
- `DATABASE_URL` - Railway will provide this automatically

### **Step 5: Get Your API URL**

Railway will give you a URL like:
```
https://reboot-motion-api.railway.app
```

Save this URL - you'll need it for the frontend!

---

## 🔧 **UPDATE FRONTEND WITH API URL**

Once deployed, update your frontend:

1. **Edit `js/api.js` in your frontend code**
2. **Change this line:**
   ```javascript
   const API_BASE_URL = 'http://localhost:8000';
   ```
   **To:**
   ```javascript
   const API_BASE_URL = 'https://your-api.railway.app';
   ```
3. **Re-deploy frontend to Netlify**

---

## 📊 **CURRENT STATUS**

**Right now, the API uses MOCK DATA:**
- ✅ 3 sample players
- ✅ 3 sample sessions
- ✅ Generated biomechanics data

**This is perfect for:**
- Testing the frontend
- Seeing how everything works
- Demo purposes

**To use REAL DATA:**
- Add your Reboot Motion API key
- Connect to PostgreSQL database
- Uncomment database code in main.py

---

## 🧪 **TESTING THE API**

### **After Deployment:**

1. Visit: `https://your-api.railway.app`
   - Should show API information

2. Visit: `https://your-api.railway.app/docs`
   - Interactive API documentation (Swagger UI)
   - Test all endpoints in your browser!

3. Test endpoints:
   ```bash
   # Get players
   curl https://your-api.railway.app/players
   
   # Get health status
   curl https://your-api.railway.app/health
   ```

---

## ⚡ **QUICK START COMMANDS**

```bash
# Local testing (optional)
pip install -r requirements.txt
uvicorn main:app --reload

# Visit: http://localhost:8000/docs
```

---

## 🎯 **NEXT STEPS AFTER DEPLOYMENT**

1. ✅ Deploy backend to Railway → Get API URL
2. ✅ Update frontend `js/api.js` with API URL
3. ✅ Re-deploy frontend to Netlify
4. ✅ Test your live app!
5. ✅ Everything should work! 🎉

---

## 💡 **FEATURES**

**Current (Mock Data):**
- ✅ All API endpoints working
- ✅ CORS enabled for frontend
- ✅ Sample player data
- ✅ Sample session data
- ✅ Generated biomechanics charts

**Future (Real Data):**
- Add PostgreSQL database
- Connect to Reboot Motion API
- Sync real athlete data
- Store biomechanics data

---

## 🆘 **TROUBLESHOOTING**

### **Railway deployment fails:**
- Check `requirements.txt` is included
- Check `Procfile` exists
- Check Python version (3.9+)

### **API doesn't start:**
- Check logs in Railway dashboard
- Verify PORT environment variable is set

### **Frontend can't connect:**
- Check CORS is enabled (it is by default)
- Verify API URL is correct in `js/api.js`
- Make sure Railway app is running

---

## 📞 **SUPPORT**

**Railway Documentation:** https://docs.railway.app
**FastAPI Documentation:** https://fastapi.tiangolo.com

---

## 🎉 **YOU'RE ALMOST DONE!**

Once you deploy this to Railway and update your frontend:
- ✅ Frontend (Netlify): DEPLOYED
- ✅ Backend (Railway): DEPLOYED
- ✅ Everything connected: WORKING!

**Total time: 10 minutes** ⏰

---

**Deploy to Railway now!** 🚀
