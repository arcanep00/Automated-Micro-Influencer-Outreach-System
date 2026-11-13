<div align="center">

# 🤝 influencer-outreach

**Find micro-influencers. Filter the best. Send personalized outreach. Automatically.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-412991?style=flat&logo=openai&logoColor=white)](https://openai.com)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=flat&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat)](./LICENSE)

</div>

---

## ✨ What it does

| Step | Description |
|------|-------------|
| 🔍 **Discovery** | Finds micro-influencers from Instagram & YouTube (5k–100k followers) |
| 🎯 **Filtering** | Filters by engagement rate, follower count, and niche |
| 📋 **Enrichment** | Adds audience demographics and contact email to each profile |
| 🤖 **Personalization** | Generates a unique email pitch + Instagram DM per influencer using OpenAI |
| 📤 **Sending** | Sends outreach emails via Gmail and prevents duplicates |
| 📊 **Tracking** | Logs every send with status, timestamp, and full outreach history |

---

## 🚀 Getting started

```bash
git clone https://github.com/arcanep00/influencer-outreach.git
cd influencer-outreach
pip install -r requirements.txt
cp .env.example .env
```

Fill in your `.env`:

```env
OPENAI_API_KEY=
RAPIDAPI_KEY=
GMAIL_SENDER_EMAIL=
GMAIL_APP_PASSWORD=
NICHE=fitness
```

Then just run:

```bash
python main.py
```

---

## 🔑 API keys

Everything is optional — the system handles missing keys gracefully.

| Key | Without it |
|-----|-----------|
| `RAPIDAPI_KEY` | Falls back to 53 built-in mock influencers |
| `OPENAI_API_KEY` | Uses niche-specific message templates instead |
| Gmail credentials | Runs in simulation mode — logs outreach without sending |

---

## 📁 Project structure

```
influencer-outreach/
├── main.py               ← entry point, runs all phases
├── config.py             ← settings & env vars
├── database.py           ← SQLite setup & queries
│
├── discovery/            ← Instagram, YouTube, Collabstr scraping
├── filtering/            ← follower, engagement, niche checks
├── enrichment/           ← email scraping, demographics, CSV export
├── personalization/      ← OpenAI message generation
├── sending/              ← Gmail SMTP + simulation mode
├── tracker/              ← outreach log & reporting
└── data/                 ← all output files (db, csv, json)
```

---

## 📬 Gmail App Password

Regular Gmail password won't work. You need an App Password:

1. Google Account → **Security** → **2-Step Verification** → enable it
2. Search **"App passwords"** → create one for **Mail**
3. Paste the 16-char password into `GMAIL_APP_PASSWORD` in `.env`

---

## 🛠 Stack

`Python` · `SQLite` · `OpenAI API` · `RapidAPI` · `BeautifulSoup` · `Gmail SMTP`
