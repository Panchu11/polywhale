# ✅ PolyWhale Setup Checklist

Use this checklist to set up your PolyWhale bot step by step.

---

## 📋 Pre-Setup

- [ ] Python 3.11+ installed
- [ ] Git installed
- [ ] Telegram account created
- [ ] Code editor installed (VS Code recommended)

---

## 🔧 Step 1: Project Setup

- [ ] Navigate to project directory
  ```bash
  cd c:\Users\panchu\Desktop\polywhales
  ```

- [ ] Create virtual environment
  ```bash
  python -m venv venv
  ```

- [ ] Activate virtual environment
  ```bash
  # Windows
  venv\Scripts\activate
  
  # Mac/Linux
  source venv/bin/activate
  ```

- [ ] Install dependencies
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Verify installation
  ```bash
  pip list
  ```

---

## 🤖 Step 2: Create Telegram Bot

- [ ] Open Telegram
- [ ] Search for `@BotFather`
- [ ] Send `/newbot` command
- [ ] Choose bot name: `PolyWhale` (or your choice)
- [ ] Choose username: `polywhale_bot` (must end with `_bot`)
- [ ] Copy bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
- [ ] Save token somewhere safe
- [ ] (Optional) Set bot description with `/setdescription`
- [ ] (Optional) Set bot about text with `/setabouttext`
- [ ] (Optional) Upload bot profile picture with `/setuserpic`

---

## 🗄️ Step 3: Set Up Database (Supabase)

- [ ] Go to [supabase.com](https://supabase.com)
- [ ] Sign up / Log in
- [ ] Click "New Project"
- [ ] Fill in details:
  - [ ] Organization: (create or select)
  - [ ] Project name: `polywhale`
  - [ ] Database password: (choose strong password - save it!)
  - [ ] Region: (choose closest to you)
- [ ] Click "Create new project"
- [ ] Wait for project to be created (~2 minutes)
- [ ] Go to Settings → Database
- [ ] Copy "Connection string" (URI format)
- [ ] Save connection string
- [ ] Go to SQL Editor
- [ ] Click "New query"
- [ ] Open `database/schema.sql` in your code editor
- [ ] Copy all SQL code
- [ ] Paste into Supabase SQL Editor
- [ ] Click "Run"
- [ ] Verify tables created in Table Editor
- [ ] Check these tables exist:
  - [ ] users
  - [ ] whales
  - [ ] trades
  - [ ] markets
  - [ ] alerts
  - [ ] tracked_whales
  - [ ] notifications

---

## 🔴 Step 4: Set Up Redis (Optional)

- [ ] Go to [upstash.com](https://upstash.com)
- [ ] Sign up / Log in
- [ ] Click "Create Database"
- [ ] Fill in details:
  - [ ] Name: `polywhale`
  - [ ] Type: Regional
  - [ ] Region: (choose closest to you)
- [ ] Click "Create"
- [ ] Copy "Redis URL" from database details
- [ ] Save Redis URL

**Note**: Redis is optional. Bot will work without it (just slower).

---

## ⚙️ Step 5: Configure Environment

- [ ] Copy `.env.example` to `.env`
  ```bash
  copy .env.example .env
  ```

- [ ] Open `.env` in code editor

- [ ] Add Telegram bot token
  ```env
  TELEGRAM_BOT_TOKEN=your_token_from_botfather
  ```

- [ ] Add database URL
  ```env
  DATABASE_URL=your_supabase_connection_string
  ```

- [ ] (Optional) Add Redis URL
  ```env
  REDIS_URL=your_upstash_redis_url
  ```

- [ ] Review other settings (defaults are fine)

- [ ] Save `.env` file

- [ ] Verify `.env` is in `.gitignore` (should be by default)

---

## 🧪 Step 6: Initialize & Test

- [ ] Initialize database
  ```bash
  python scripts/init_db.py
  ```
  - [ ] Should see "✓ Schema executed successfully"
  - [ ] Should see list of created tables

- [ ] Test bot connection
  ```bash
  python scripts/test_bot.py
  ```
  - [ ] Should see "✓ Bot connected: @your_bot_username"

- [ ] Test database connection
  ```bash
  python scripts/test_db.py
  ```
  - [ ] Should see "✓ Database connected"
  - [ ] Should see list of tables

- [ ] Test Polymarket API
  ```bash
  python scripts/test_api.py
  ```
  - [ ] Should see "✓ Fetched X trades"
  - [ ] Should see "✓ Fetched X markets"

---

## 🚀 Step 7: Run the Bot

- [ ] Start the bot
  ```bash
  python main.py
  ```

- [ ] Verify startup messages:
  - [ ] "✓ Settings validated"
  - [ ] "✓ Database connected"
  - [ ] "✓ Whale tracker initialized"
  - [ ] "🐋 PolyWhale bot started successfully!"

- [ ] Open Telegram

- [ ] Search for your bot username

- [ ] Send `/start` command

- [ ] Verify you receive welcome message

- [ ] Try other commands:
  - [ ] `/help` - See help message
  - [ ] `/whales` - See recent whale trades
  - [ ] `/markets` - See top markets
  - [ ] `/whale <address>` - View whale profile (if you have an address)

---

## 🎉 Step 8: Verify Everything Works

- [ ] Bot responds to commands
- [ ] No errors in console
- [ ] Database is storing data
- [ ] Whale trades are being detected
- [ ] Commands return expected results

---

## 🐛 Troubleshooting

### If bot doesn't respond:
- [ ] Check `TELEGRAM_BOT_TOKEN` is correct in `.env`
- [ ] Verify bot is running (`python main.py`)
- [ ] Check console for errors
- [ ] Try restarting bot

### If database errors:
- [ ] Check `DATABASE_URL` is correct in `.env`
- [ ] Verify Supabase project is active
- [ ] Run `python scripts/init_db.py` again
- [ ] Check Supabase dashboard for errors

### If API errors:
- [ ] Check internet connection
- [ ] Verify Polymarket API is accessible
- [ ] Try running `python scripts/test_api.py`
- [ ] Check console for specific error messages

### If "Module not found" errors:
- [ ] Verify virtual environment is activated
- [ ] Run `pip install -r requirements.txt` again
- [ ] Check Python version is 3.11+

---

## 📚 Next Steps

- [ ] Read [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for features
- [ ] Read [TODO.md](TODO.md) for upcoming features
- [ ] Join Polymarket community
- [ ] Share bot with friends
- [ ] (Optional) Deploy to production - see [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 🎯 Optional: Deploy to Production

- [ ] Read [DEPLOYMENT.md](DEPLOYMENT.md)
- [ ] Choose hosting platform (Railway recommended)
- [ ] Push code to GitHub
- [ ] Connect GitHub to hosting platform
- [ ] Set environment variables
- [ ] Deploy
- [ ] Test in production
- [ ] Set up monitoring

---

## ✅ Completion Checklist

- [ ] Bot is running locally
- [ ] All commands work
- [ ] Database is connected
- [ ] API is working
- [ ] No errors in console
- [ ] Ready to use!

---

## 🎊 Congratulations!

You've successfully set up PolyWhale! 🐋

**What's next?**
- Start tracking whales
- Customize your alerts
- Share with the community
- Contribute to the project

**Need help?**
- Check documentation
- Open GitHub issue
- Contact [@Zun2025](https://x.com/Zun2025)

---

**Happy whale tracking! 🐋🚀**

