# 🚀 Deployment Guide

This guide covers deploying PolyWhale bot to production.

---

## 🎯 Deployment Options

### Option 1: Railway.app (Recommended)
- ✅ Free tier: 500 hours/month
- ✅ Easy deployment from GitHub
- ✅ Automatic HTTPS
- ✅ Built-in monitoring

### Option 2: Render.com
- ✅ Free tier available
- ✅ Auto-deploy from GitHub
- ✅ Good documentation

### Option 3: Fly.io
- ✅ Free tier available
- ✅ Global deployment
- ✅ Docker-based

---

## 🚂 Deploy to Railway.app

### Step 1: Prepare Repository

1. **Initialize Git** (if not already done):
```bash
git init
git add .
git commit -m "Initial commit"
```

2. **Push to GitHub**:
```bash
git remote add origin https://github.com/yourusername/polywhale.git
git push -u origin main
```

### Step 2: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `polywhale` repository

### Step 3: Configure Environment Variables

In Railway dashboard, add these variables:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
DATABASE_URL=your_supabase_url
REDIS_URL=your_upstash_url
ENVIRONMENT=production
LOG_LEVEL=INFO
WHALE_THRESHOLD=10000
POLL_INTERVAL=60
```

### Step 4: Configure Start Command

In Railway settings:
- **Start Command**: `python main.py`
- **Build Command**: `pip install -r requirements.txt`

### Step 5: Deploy

1. Click "Deploy"
2. Wait for build to complete
3. Check logs for any errors
4. Test bot in Telegram

---

## 🎨 Deploy to Render.com

### Step 1: Create Web Service

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your repository

### Step 2: Configure Service

- **Name**: polywhale-bot
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py`
- **Plan**: Free

### Step 3: Add Environment Variables

Same as Railway (see above)

### Step 4: Deploy

Click "Create Web Service" and wait for deployment

---

## ✈️ Deploy to Fly.io

### Step 1: Install Fly CLI

```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

### Step 2: Login

```bash
fly auth login
```

### Step 3: Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### Step 4: Initialize Fly App

```bash
fly launch
```

Follow prompts:
- App name: polywhale-bot
- Region: Choose closest to you
- PostgreSQL: No (using Supabase)
- Redis: No (using Upstash)

### Step 5: Set Environment Variables

```bash
fly secrets set TELEGRAM_BOT_TOKEN=your_token
fly secrets set DATABASE_URL=your_db_url
fly secrets set REDIS_URL=your_redis_url
```

### Step 6: Deploy

```bash
fly deploy
```

---

## 🔧 Post-Deployment

### 1. Verify Deployment

```bash
# Check logs
railway logs  # Railway
render logs   # Render
fly logs      # Fly.io
```

### 2. Test Bot

1. Open Telegram
2. Find your bot
3. Send `/start`
4. Verify response

### 3. Monitor Performance

- Check Railway/Render/Fly dashboard
- Monitor error rates
- Check response times
- Monitor database usage

### 4. Set Up Alerts

Configure alerts for:
- Bot downtime
- High error rates
- Database issues
- Memory/CPU usage

---

## 📊 Monitoring

### Railway Monitoring

- Built-in metrics dashboard
- View logs in real-time
- Set up webhooks for alerts

### External Monitoring

**Sentry** (Error Tracking):
1. Sign up at [sentry.io](https://sentry.io)
2. Create new project
3. Add `SENTRY_DSN` to environment variables
4. Errors will be tracked automatically

**UptimeRobot** (Uptime Monitoring):
1. Sign up at [uptimerobot.com](https://uptimerobot.com)
2. Add HTTP monitor
3. Set check interval to 5 minutes
4. Configure email alerts

---

## 🔄 Continuous Deployment

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install Railway CLI
        run: npm install -g @railway/cli
      
      - name: Deploy to Railway
        run: railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

---

## 🐛 Troubleshooting

### Bot Not Responding

1. Check logs for errors
2. Verify `TELEGRAM_BOT_TOKEN` is correct
3. Ensure bot is running (check process status)
4. Test database connection

### Database Connection Issues

1. Verify `DATABASE_URL` is correct
2. Check Supabase project is active
3. Verify database tables exist
4. Check connection pool settings

### High Memory Usage

1. Reduce `POLL_INTERVAL` to decrease frequency
2. Limit cache size
3. Optimize database queries
4. Consider upgrading to paid tier

### API Rate Limits

1. Increase `POLL_INTERVAL`
2. Implement exponential backoff
3. Add request caching
4. Monitor API usage

---

## 📈 Scaling

### When to Scale

- More than 1,000 active users
- Response time > 2 seconds
- Memory usage > 80%
- Database queries slow

### How to Scale

1. **Upgrade hosting plan**
   - Railway: $5/month for more resources
   - Render: $7/month for starter plan

2. **Optimize database**
   - Add indexes
   - Use connection pooling
   - Cache frequent queries

3. **Add Redis caching**
   - Cache market data
   - Cache whale stats
   - Reduce database load

4. **Horizontal scaling**
   - Multiple bot instances
   - Load balancing
   - Distributed caching

---

## 🔒 Security

### Best Practices

1. **Never commit secrets**
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Rotate tokens regularly**
   - Change bot token every 6 months
   - Update database passwords

3. **Monitor for abuse**
   - Rate limit user commands
   - Block spam users
   - Log suspicious activity

4. **Keep dependencies updated**
   ```bash
   pip list --outdated
   pip install --upgrade -r requirements.txt
   ```

---

## 📝 Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Environment variables configured
- [ ] Database initialized
- [ ] Bot tested locally
- [ ] Deployment successful
- [ ] Bot responding in Telegram
- [ ] Logs showing no errors
- [ ] Monitoring set up
- [ ] Alerts configured
- [ ] Documentation updated

---

**Happy deploying! 🚀**

