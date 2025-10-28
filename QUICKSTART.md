# ⚡ Quick Start Guide

Get PolyWhale bot running in 5 minutes!

---

## 🚀 Super Quick Setup

### 1. Install Dependencies
```bash
python setup.py
```

### 2. Get Telegram Bot Token
1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Follow prompts to create your bot
4. Copy the bot token

### 3. Set Up Database (Supabase)
1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Copy the connection string from Settings → Database
4. Go to SQL Editor and paste contents of `database/schema.sql`
5. Run the SQL

### 4. Configure Environment
Edit `.env` file:
```env
TELEGRAM_BOT_TOKEN=your_token_here
DATABASE_URL=your_supabase_url_here
```

### 5. Initialize Database
```bash
python scripts/init_db.py
```

### 6. Test Everything
```bash
python scripts/test_bot.py
python scripts/test_db.py
python scripts/test_api.py
```

### 7. Run the Bot
```bash
python main.py
```

---

## 🎯 First Commands to Try

Open your bot in Telegram and try:

- `/start` - Welcome message
- `/help` - See all commands
- `/whales` - Recent whale trades
- `/markets` - Top markets

---

## 🐛 Common Issues

### "No module named 'telegram'"
```bash
pip install -r requirements.txt
```

### "Database connection failed"
- Check DATABASE_URL in .env
- Make sure Supabase project is active
- Run `python scripts/init_db.py`

### "Bot doesn't respond"
- Check TELEGRAM_BOT_TOKEN in .env
- Make sure bot is running (`python main.py`)
- Check logs in `logs/` directory

---

## 📚 Next Steps

- Read [GETTING_STARTED.md](GETTING_STARTED.md) for detailed setup
- Read [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for features
- Read [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for roadmap

---

**Need help? Open an issue or contact [@Zun2025](https://x.com/Zun2025)**

