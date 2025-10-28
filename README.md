# 🐋 PolyWhale - Polymarket Whale Tracker Bot

> **Track the smartest money in prediction markets**

A free, open-source Telegram bot that provides real-time alerts and analytics for whale activity on Polymarket.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://telegram.org/)

---

## 📚 Documentation

### 🚀 Getting Started
- **[START_HERE.md](START_HERE.md)** - **👈 START HERE!** Your main entry point
- **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
- **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** - Step-by-step setup checklist
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Detailed setup guide

### 📖 Project Information
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Complete feature overview
- **[FEASIBILITY_ANALYSIS.md](FEASIBILITY_ANALYSIS.md)** - Technical feasibility
- **[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)** - Development roadmap
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Current status
- **[TODO.md](TODO.md)** - Task list

### 🚀 Deployment & Contributing
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)** - What's been built

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Telegram account
- Supabase account (free tier)
- Upstash Redis account (free tier)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/polywhale.git
cd polywhale
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Initialize database**
```bash
python scripts/init_db.py
```

6. **Run the bot**
```bash
python main.py
```

---

## 🎯 Features

### ✅ Implemented (MVP Ready!)
- ✅ Real-time whale detection (>$10k trades)
- ✅ Whale profile viewer with statistics
- ✅ Market scanner by whale activity
- ✅ Database integration (PostgreSQL)
- ✅ API integration (Polymarket)
- ✅ Basic bot commands (/start, /help, /whales, /markets, /whale)

### 🚧 In Progress
- 🟡 Alert notification system
- 🟡 Track/untrack whales
- 🟡 User settings management
- 🟡 Whale leaderboard

### 📋 Planned (Next 2 Weeks)
- ⏳ Smart money flow analysis
- ⏳ Whale consensus indicators
- ⏳ Historical analytics
- ⏳ Digest mode
- ⏳ Advanced filtering

---

## 🤖 Bot Commands

### Basic
- `/start` - Welcome message & setup
- `/help` - Show all commands
- `/about` - About PolyWhale

### Whale Tracking
- `/whales` - Recent whale trades
- `/whale <address>` - View whale profile
- `/track <address>` - Track a whale
- `/mywhales` - Your tracked whales

### Markets
- `/markets` - Top markets by whale activity
- `/trending` - Hottest markets
- `/search <query>` - Search markets

### Analytics
- `/top` - Whale leaderboard
- `/flow` - Smart money flow
- `/consensus` - Whale consensus

### Settings
- `/alerts` - Manage alerts
- `/settings` - Configure preferences
- `/threshold <amount>` - Set minimum trade size

---

## 🏗️ Architecture

```
PolyWhale Bot
├── main.py                 # Entry point
├── bot/
│   ├── handlers/           # Command handlers
│   ├── services/           # Business logic
│   ├── models/             # Data models
│   └── utils/              # Utilities
├── database/
│   ├── models.py           # Database models
│   └── migrations/         # SQL migrations
├── config/
│   └── settings.py         # Configuration
└── tests/                  # Unit tests
```

---

## 🛠️ Tech Stack

- **Language**: Python 3.11+
- **Bot Framework**: python-telegram-bot
- **Database**: PostgreSQL (Supabase)
- **Cache**: Redis (Upstash)
- **Hosting**: Railway.app
- **Monitoring**: Sentry

---

## 📊 Project Status

**Current Phase**: Week 1 - MVP Complete! 🎉
**Progress**: 85% (MVP Ready for Testing)
**Next Milestone**: Deploy to production & beta testing

### What's Done
- ✅ Complete project structure (40+ files)
- ✅ Database schema with 7 tables
- ✅ 5 working bot commands
- ✅ 3 core services (API, Database, WhaleTracker)
- ✅ 5 data models
- ✅ Comprehensive documentation (11 files)
- ✅ Testing scripts
- ✅ Setup automation

### What's Next
- ⏳ Complete alert system
- ⏳ Add remaining commands
- ⏳ Deploy to Railway.app
- ⏳ Beta testing with users

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Polymarket](https://polymarket.com/) for providing public APIs
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for the excellent bot framework
- The prediction markets community

---

## 📞 Contact

- Twitter: [@Zun2025](https://x.com/Zun2025)
- Website: [polywhalestracker.xyz](https://www.polywhalestracker.xyz/)
- Telegram: [Coming soon]

---

**Built with ❤️ for the Polymarket community**

