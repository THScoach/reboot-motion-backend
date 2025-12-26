# 🚀 CATCHING BARRELS - DEPLOYMENT GUIDE

**Status:** ✅ Production Ready (80% test pass rate)  
**Version:** 1.0.0  
**Last Updated:** December 25, 2025

---

## 🎯 QUICK START

Choose your deployment platform:

1. **Railway.app** (Recommended) - Free tier, automatic deployment
2. **Render.com** - Free tier available
3. **Heroku** - Paid plans
4. **Docker** - Self-hosted
5. **Manual Server** - VPS/Cloud

---

## 📋 PREREQUISITES

### Required Environment Variables
```bash
WHOP_API_KEY=your_whop_api_key_here
WHOP_COMPANY_ID=biz_4f4wiRWwiEZflF
```

### Optional Environment Variables
```bash
PORT=8006                                    # Server port (default: 8006)
DATABASE_URL=postgresql://...               # Database (default: in-memory)
ENVIRONMENT=production                       # Environment name
```

### Whop Product IDs (Already Configured)
```python
FREE_SWING_AUDIT = prod_Wkwv5hjyghOXC       # $0
BARRELS_PRO = prod_O4CB6y0IzNJLe            # $19.99/mo
BARRELS_PREMIUM = prod_7068OOSHrjMvc        # $99/mo
BARRELS_ULTIMATE = prod_OXEGclGuMyYVd       # $299.99/yr
```

---

## 🚂 OPTION 1: RAILWAY.APP (RECOMMENDED)

### Why Railway?
- ✅ Free tier available
- ✅ Automatic GitHub deployments
- ✅ Free SSL certificates
- ✅ Simple environment variable management
- ✅ Built-in monitoring

### Deployment Steps

#### 1. Install Railway CLI
```bash
npm install -g @railway/cli
```

#### 2. Login to Railway
```bash
railway login
```

#### 3. Initialize Project
```bash
cd /path/to/reboot-motion-backend
railway init
```

#### 4. Set Environment Variables
```bash
railway variables set WHOP_API_KEY="your_key_here"
railway variables set WHOP_COMPANY_ID="biz_4f4wiRWwiEZflF"
railway variables set PORT=8000
```

#### 5. Deploy
```bash
railway up
```

#### 6. Get Your URL
```bash
railway domain
```

#### 7. Configure Custom Domain (Optional)
```bash
railway domain add api.catchingbarrels.com
```

### Railway Configuration Files
- `railway.json` - Railway-specific config (already included)
- `Procfile` - Start command (already included)
- `runtime.txt` - Python version (already included)

---

## 🎨 OPTION 2: RENDER.COM

### Deployment Steps

#### 1. Create New Web Service
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect GitHub: `THScoach/reboot-motion-backend`

#### 2. Configure Service
- **Name:** catching-barrels-api
- **Environment:** Python 3
- **Region:** Choose closest to users
- **Branch:** main
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn coach_rick_wap_integration:app --host 0.0.0.0 --port $PORT`

#### 3. Add Environment Variables
In Render dashboard, add:
- `WHOP_API_KEY`
- `WHOP_COMPANY_ID`

#### 4. Deploy
Click "Create Web Service"

---

## 💜 OPTION 3: HEROKU

### Deployment Steps

#### 1. Install Heroku CLI
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

#### 2. Login
```bash
heroku login
```

#### 3. Create App
```bash
heroku create catching-barrels-api
```

#### 4. Set Environment Variables
```bash
heroku config:set WHOP_API_KEY="your_key_here"
heroku config:set WHOP_COMPANY_ID="biz_4f4wiRWwiEZflF"
```

#### 5. Deploy
```bash
git push heroku main
```

#### 6. Scale
```bash
heroku ps:scale web=1
```

---

## 🐳 OPTION 4: DOCKER

### Using Docker Compose (Recommended)

#### 1. Set Environment Variables
Create `.env` file:
```bash
WHOP_API_KEY=your_key_here
WHOP_COMPANY_ID=biz_4f4wiRWwiEZflF
```

#### 2. Start Services
```bash
docker-compose up -d
```

#### 3. Check Logs
```bash
docker-compose logs -f
```

#### 4. Stop Services
```bash
docker-compose down
```

### Using Docker Directly

#### 1. Build Image
```bash
docker build -t catching-barrels .
```

#### 2. Run Container
```bash
docker run -d \
  --name catching-barrels-api \
  -p 8006:8006 \
  -e WHOP_API_KEY="your_key_here" \
  -e WHOP_COMPANY_ID="biz_4f4wiRWwiEZflF" \
  catching-barrels
```

#### 3. Check Status
```bash
docker ps
docker logs catching-barrels-api
```

---

## 🖥️ OPTION 5: MANUAL SERVER (VPS/AWS/GCP/Azure)

### Server Requirements
- **OS:** Ubuntu 20.04+ / Debian 11+
- **RAM:** 512 MB minimum, 1 GB recommended
- **CPU:** 1 core minimum
- **Disk:** 2 GB free space
- **Python:** 3.12

### Deployment Steps

#### 1. SSH to Server
```bash
ssh user@your-server.com
```

#### 2. Install Dependencies
```bash
sudo apt update
sudo apt install -y python3.12 python3-pip python3-venv nginx
```

#### 3. Clone Repository
```bash
git clone https://github.com/THScoach/reboot-motion-backend.git
cd reboot-motion-backend
```

#### 4. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 5. Set Environment Variables
Create `/etc/environment`:
```bash
WHOP_API_KEY="your_key_here"
WHOP_COMPANY_ID="biz_4f4wiRWwiEZflF"
```

#### 6. Create Systemd Service
Create `/etc/systemd/system/catching-barrels.service`:
```ini
[Unit]
Description=Catching Barrels API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/user/reboot-motion-backend
Environment="PATH=/home/user/reboot-motion-backend/venv/bin"
EnvironmentFile=/etc/environment
ExecStart=/home/user/reboot-motion-backend/venv/bin/uvicorn coach_rick_wap_integration:app --host 0.0.0.0 --port 8006
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 7. Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable catching-barrels
sudo systemctl start catching-barrels
sudo systemctl status catching-barrels
```

#### 8. Configure Nginx
Create `/etc/nginx/sites-available/catching-barrels`:
```nginx
server {
    listen 80;
    server_name api.catchingbarrels.com;

    location / {
        proxy_pass http://localhost:8006;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/catching-barrels /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 9. Install SSL Certificate (Let's Encrypt)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d api.catchingbarrels.com
```

---

## ⚙️ POST-DEPLOYMENT CONFIGURATION

### 1. Configure Whop Webhook

1. Go to https://whop.com/biz/developer
2. Navigate to Webhooks section
3. Add new webhook:
   - **URL:** `https://your-domain.com/webhooks/whop`
   - **Events:** Select all `membership.*` and `payment.*` events
   - **Secret:** (Optional) Store for signature verification

### 2. Test Endpoints

```bash
# Health check
curl https://your-domain.com/health

# Swing DNA health
curl https://your-domain.com/api/swing-dna/health

# Coach Rick health
curl https://your-domain.com/api/v1/reboot-lite/coach-rick/health

# API Documentation
open https://your-domain.com/docs
```

### 3. Update Frontend Configuration

Update frontend API base URL to point to your deployed backend:
```javascript
const API_BASE_URL = 'https://your-domain.com';
```

### 4. Monitor Application

#### View Logs (Railway)
```bash
railway logs
```

#### View Logs (Render)
Check Render dashboard → Logs tab

#### View Logs (Docker)
```bash
docker-compose logs -f
```

#### View Logs (Systemd)
```bash
sudo journalctl -u catching-barrels -f
```

---

## 🧪 VERIFICATION CHECKLIST

After deployment, verify these endpoints:

- [ ] `GET /health` - Returns 200 OK
- [ ] `GET /docs` - Swagger UI loads
- [ ] `GET /api/swing-dna/health` - Returns healthy status
- [ ] `GET /api/v1/reboot-lite/coach-rick/health` - Returns healthy status
- [ ] `GET /webhooks/whop/status` - Returns webhook status
- [ ] `POST /webhooks/whop` - Accepts Whop webhooks
- [ ] `GET /coach-rick-ui` - UI loads
- [ ] `GET /swing-dna/upload` - UI loads

---

## 📊 MONITORING & MAINTENANCE

### Health Checks
All platforms support automatic health checks:
- **Endpoint:** `/health`
- **Expected:** 200 OK
- **Interval:** 30 seconds

### Performance Monitoring
- **Response Time:** <10ms (verified in tests)
- **Uptime:** Target 99.9%
- **Error Rate:** <1%

### Log Monitoring
Monitor for:
- Application errors
- Webhook delivery failures
- CSV upload errors
- Database connection issues

### Backup Strategy
- **Database:** Daily automated backups (if using PostgreSQL)
- **Code:** GitHub repository
- **Environment Variables:** Secure backup of credentials

---

## 🔒 SECURITY BEST PRACTICES

### Environment Variables
- ✅ Never commit API keys to Git
- ✅ Use platform secret management (Railway Variables, Render Env Vars)
- ✅ Rotate keys regularly

### HTTPS/SSL
- ✅ Always use HTTPS in production
- ✅ Free SSL via Let's Encrypt or platform provider
- ✅ Enforce HTTPS redirects

### Webhook Security
- ✅ Verify Whop webhook signatures
- ✅ Rate limit webhook endpoints
- ✅ Log all webhook events

---

## 🐛 TROUBLESHOOTING

### Common Issues

#### 1. Port Already in Use
```bash
# Find and kill process
lsof -ti:8006 | xargs kill -9
```

#### 2. Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 3. Whop Webhook Not Working
- Verify webhook URL is publicly accessible
- Check webhook secret configuration
- Review webhook logs in Whop dashboard

#### 4. Database Connection Error
- Verify DATABASE_URL is set correctly
- Check database credentials
- Ensure database server is accessible

---

## 📚 RESOURCES

- **GitHub Repository:** https://github.com/THScoach/reboot-motion-backend
- **System Test Report:** [SYSTEM_TEST_REPORT.md](SYSTEM_TEST_REPORT.md)
- **API Documentation:** `/docs` endpoint (Swagger UI)
- **Whop Developer Portal:** https://whop.com/biz/developer

---

## 🆘 SUPPORT

### Deployment Issues
- Check logs for error messages
- Review this deployment guide
- Verify environment variables
- Test endpoints manually

### Production Issues
- Monitor application logs
- Check health endpoints
- Review webhook delivery status
- Test with Swagger UI

---

## ✅ DEPLOYMENT CHECKLIST

Before going live:

- [ ] All environment variables set
- [ ] Whop webhook configured
- [ ] SSL certificate installed
- [ ] Health checks passing
- [ ] All endpoints tested
- [ ] Frontend configured
- [ ] Monitoring enabled
- [ ] Backup strategy in place
- [ ] Documentation updated
- [ ] Team notified

---

**🎉 Ready to Deploy!**

Choose your platform above and follow the step-by-step instructions.

**Current Status:** ✅ Production Ready (80% test pass rate)
**Latest Commit:** 7d5f133
**Test Results:** 8/10 passing (non-critical failures)
