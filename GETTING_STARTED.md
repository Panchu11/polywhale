# 🚀 Getting Started with PolyWhale Bot

This guide will help you set up and run the PolyWhale bot from scratch.

---

## 📋 Prerequisites

Before you begin, make sure you have:

1. **Python 3.11 or higher** installed
2. **Git** installed
3. **A Telegram account**
4. **A Supabase account** (free tier) - [Sign up here](https://supabase.com/)
5. **An Upstash Redis account** (free tier) - [Sign up here](https://upstash.com/)

---

## 🔧 Step 1: Create Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` command
3. Follow the prompts:
   - Choose a name: `PolyWhale`
   - Choose a username: `polywhale_bot` (must end with `_bot`)
4. **Save the bot token** - you'll need it later
5. Optional: Set bot description and profile picture using BotFather commands

---

## 🗄️ Step 2: Set Up Database (Supabase)

1. Go to [supabase.com](https://supabase.com/) and sign up
2. Create a new project:
   - Project name: `polywhale`
   - Database password: (choose a strong password)
   - Region: (choose closest to you)
3. Wait for project to be created (~2 minutes)
4. Go to **Settings** → **Database**
5. Copy the **Connection String** (URI format)
   - It looks like: `postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres`
6. Go to **SQL Editor**
7. Copy the contents of `database/schema.sql` and run it
8. Verify tables were created in **Table Editor**

---

## 🔴 Step 3: Set Up Redis (Upstash)

1. Go to [upstash.com](https://upstash.com/) and sign up
2. Create a new Redis database:
   - Name: `polywhale`
   - Type: Regional
   - Region: (choose closest to you)
3. Copy the **Redis URL** from the database details
   - It looks like: `redis://default:[PASSWORD]@[HOST]:6379`

---

## 💻 Step 4: Clone and Set Up Project

```bash
# Clone the repository (or download the code)
cd c:\Users\panchu\Desktop\polywhales

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## ⚙️ Step 5: Configure Environment Variables

1. Copy the example environment file:
```bash
copy .env.example .env
```

2. Edit `.env` file with your credentials:
```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather

# Database Configuration (from Supabase)
DATABASE_URL=postgresql://postgres:password@db.xxx.supabase.co:5432/postgres

# Redis Configuration (from Upstash)
REDIS_URL=redis://default:password@host:6379

# Bot Configuration (you can keep these defaults)
WHALE_THRESHOLD=10000
POLL_INTERVAL=60
MAX_ALERTS_PER_USER=50

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
```

---

## 🧪 Step 6: Test the Setup

```bash
# Test database connection
python scripts/test_db.py

# Test Polymarket API
python scripts/test_api.py

# Test bot connection
python scripts/test_bot.py
```

---

## 🚀 Step 7: Run the Bot

```bash
# Run the bot
python main.py
```

You should see:
```
2025-10-28 10:00:00 | INFO | PolyWhale bot started successfully
2025-10-28 10:00:00 | INFO | Polling for whale trades every 60 seconds
2025-10-28 10:00:00 | INFO | Bot is ready to receive commands
```

---

## 📱 Step 8: Test the Bot

1. Open Telegram
2. Search for your bot username (e.g., `@polywhale_bot`)
3. Send `/start` command
4. You should receive a welcome message
5. Try other commands:
   - `/help` - See all commands
   - `/whales` - See recent whale trades
   - `/markets` - See top markets

---

## 🐛 Troubleshooting

### Bot doesn't respond
- Check if `main.py` is running without errors
- Verify `TELEGRAM_BOT_TOKEN` is correct
- Make sure bot is not already running elsewhere

### Database connection error
- Verify `DATABASE_URL` is correct
- Check if Supabase project is active
- Ensure database schema was created successfully

### No whale alerts
- Check if Polymarket API is accessible
- Verify `POLL_INTERVAL` is set correctly
- Check logs for any API errors

### Redis connection error
- Verify `REDIS_URL` is correct
- Check if Upstash database is active
- Redis is optional - bot will work without it (slower)

---

## 📊 Monitoring

### View Logs
```bash
# Logs are saved in logs/ directory
tail -f logs/bot_2025-10-28.log
```

### Check Database
- Go to Supabase dashboard
- Open **Table Editor**
- View `trades`, `whales`, `users` tables

### Monitor Performance
- Check Railway dashboard (after deployment)
- View Sentry errors (if configured)

---

## 🚀 Deployment (Optional)

### Deploy to Railway.app

1. Go to [railway.app](https://railway.app/) and sign up
2. Create new project from GitHub repo
3. Add environment variables in Railway dashboard
4. Deploy automatically on push

### Deploy to Render.com

1. Go to [render.com](https://render.com/) and sign up
2. Create new Web Service
3. Connect GitHub repository
4. Add environment variables
5. Deploy

---

## 📚 Next Steps

1. ✅ Read [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for feature details
2. ✅ Read [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for development roadmap
3. ✅ Join the community and share feedback
4. ✅ Contribute to the project

---

## 🆘 Need Help?

- Check the [FAQ](FAQ.md)
- Open an issue on GitHub
- Contact on Twitter: [@Zun2025](https://x.com/Zun2025)

---

**Happy whale tracking! 🐋**

