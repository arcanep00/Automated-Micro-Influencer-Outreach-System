# influencer-outreach

Automated system that finds micro-influencers, filters them, generates personalized outreach messages, and sends emails.

## What it does

- Discovers influencers from Instagram and YouTube (5k–100k followers)
- Filters by engagement rate, niche, and follower count
- Enriches profiles with audience demographics and contact email
- Generates a personalized email pitch and Instagram DM for each influencer using OpenAI
- Sends emails via Gmail and tracks who's been contacted

## Setup

```bash
git clone https://github.com/your-username/influencer-outreach.git
cd influencer-outreach
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env`:

```
OPENAI_API_KEY=
RAPIDAPI_KEY=
GMAIL_SENDER_EMAIL=
GMAIL_APP_PASSWORD=
NICHE=fitness
```

Then run:

```bash
python main.py
```

## API keys

All keys are optional. The system falls back gracefully:

- No `RAPIDAPI_KEY` → uses built-in mock data (53 influencers)
- No `OPENAI_API_KEY` → uses niche-specific message templates
- No Gmail credentials → runs in simulation mode, logs outreach without sending

## Gmail App Password

Regular Gmail password won't work here. Go to Google Account → Security → App Passwords and generate one for Mail. Paste it into `GMAIL_APP_PASSWORD`.

## Stack

Python, SQLite, OpenAI API, RapidAPI, BeautifulSoup, Gmail SMTP
