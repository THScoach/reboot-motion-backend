# Railway Reboot Motion Credentials Setup

**Date**: 2025-12-26  
**Status**: Ready to Deploy

---

## ✅ Credentials Verified

The Reboot Motion API credentials have been **tested and verified**:

```
Username: coachrickpd@gmail.com
Password: Train@2025
```

**Test Results**:
- ✅ OAuth authentication successful
- ✅ API connection established
- ✅ **100 players** fetched from Reboot Motion
- ✅ Sample players: Connor Gray, Yahil Melendez, Reese Parmeley, bruce portell, Austin Almany

---

## 🚀 How to Add Credentials to Railway

### **Method 1: Railway Dashboard (Recommended)**

1. **Go to Railway Dashboard**:
   ```
   https://railway.app
   ```

2. **Select Your Project**:
   - Click on `reboot-motion-backend` project

3. **Navigate to Variables**:
   - Click on your service
   - Click on the **"Variables"** tab

4. **Add Environment Variables**:
   
   Click **"+ New Variable"** and add:
   
   ```
   Variable Name: REBOOT_USERNAME
   Value: coachrickpd@gmail.com
   ```
   
   Click **"+ New Variable"** again and add:
   
   ```
   Variable Name: REBOOT_PASSWORD
   Value: Train@2025
   ```

5. **Deploy**:
   - Railway will automatically redeploy with the new credentials
   - Wait 2-3 minutes for deployment to complete

---

### **Method 2: Railway CLI** (Alternative)

If you have Railway CLI installed:

```bash
# Login to Railway
railway login

# Link to your project
railway link

# Add variables
railway variables set REBOOT_USERNAME=coachrickpd@gmail.com
railway variables set REBOOT_PASSWORD='Train@2025'

# Deploy
railway up
```

---

## ✅ Verification After Deployment

Once deployed, test the endpoint:

### **Test Player Search**:

```bash
# Search for "Connor"
curl "https://reboot-motion-backend-production.up.railway.app/api/reboot/players/search?query=Connor"

# Search for "Yahil"
curl "https://reboot-motion-backend-production.up.railway.app/api/reboot/players/search?query=Yahil"

# Get all players (top 10)
curl "https://reboot-motion-backend-production.up.railway.app/api/reboot/players/search?query="
```

### **Expected Response**:

```json
{
  "query": "Connor",
  "count": 1,
  "players": [
    {
      "first_name": "Connor",
      "last_name": "Gray",
      "org_player_id": "...",
      "reboot_player_id": "...",
      "date_of_birth": "...",
      "height_ft": 6.0,
      "weight_lbs": 185
    }
  ],
  "source": "reboot_motion_api"
}
```

---

## 🎯 What This Enables

With Reboot credentials configured, the Coach Rick UI can now:

1. **Search Players**: Type any player name in the search box
2. **View Real Data**: See all 100 players from your Reboot Motion account
3. **Load Sessions**: Click on a player to view their sessions
4. **Generate Reports**: One-click KRS reports from Reboot data

---

## 📊 Your Reboot Motion Data

- **Total Players**: 100
- **Sample Players**:
  - Connor Gray
  - Yahil Melendez
  - Reese Parmeley
  - bruce portell
  - Austin Almany
  - ...and 95 more!

---

## 🔒 Security Notes

- Credentials are stored securely in Railway environment variables
- Never committed to Git repository
- Only accessible to Railway deployment
- OAuth tokens cached for 24 hours

---

## 🐛 Troubleshooting

### If search returns empty:

1. **Check Variables**: Verify both `REBOOT_USERNAME` and `REBOOT_PASSWORD` are set
2. **Check Spelling**: Ensure no typos in variable names
3. **Restart Service**: Sometimes Railway needs a manual restart after adding variables
4. **Check Logs**: View Railway logs for authentication errors

### If authentication fails:

- Verify credentials are correct: `coachrickpd@gmail.com` / `Train@2025`
- Check Reboot Motion API status: https://api.rebootmotion.com/health
- Contact Reboot Motion support if needed

---

## 📝 Next Steps

1. ✅ Add credentials to Railway (see Method 1 above)
2. ✅ Wait for automatic redeployment (2-3 minutes)
3. ✅ Test the endpoint with curl or browser
4. ✅ Open Coach Rick UI and search for players!

---

**Ready to add the credentials? Follow Method 1 above!** 🚀
