# Influencer Outreach

Automated micro-influencer discovery, filtering, enrichment, and personalized outreach system.

---

## What it does

1. **Discovers** micro-influencers from Instagram, YouTube, and public directories
2. **Filters** them based on follower count, engagement rate, and niche
3. **Enriches** each profile with audience demographics and contact email
4. **Generates** personalized email pitches (60–90 words) and Instagram DMs (15–30 words) using AI
5. **Sends** outreach emails via Gmail SMTP and logs every action
6. **Tracks** send status, duplicates, and results in a structured outreach log

---

## Tech stack

- Python 3.10+
- SQLite — local database
- OpenAI API (gpt-3.5-turbo) — message personalization
- BeautifulSoup + requests — email scraping from public profiles
- Gmail SMTP — email sending
- RapidAPI (Instagram Scraper, YouTube Search) — influencer discovery
- Apify — optional scraping fallback

---

## Project structure

```
influencer-outreach/
├── config.py                   # All settings and API keys
├── database.py                 # DB setup and query functions
├── main.py                     # Runs all phases end to end
├── requirements.txt
├── .env                        # API keys (not committed)
├── .env.example                # Key reference template
│
├── discovery/
│   ├── scraper.py              # Instagram, YouTube, Collabstr scraping
│   └── mock_data.py            # 53 sample influencers for testing
│
├── filtering/
│   └── filter.py               # Follower, engagement, niche filtering
│
├── enrichment/
│   ├── enrich.py               # Email scraping + demographics
│   └── export.py               # CSV and JSON export
│
├── personalization/
│   ├── generate.py             # OpenAI + fallback message generation
│   └── export_messages.py      # Messages CSV/JSON export
│
├── sending/
│   └── sender.py               # Gmail SMTP sending + simulation mode
│
├── tracker/
│   └── tracker.py              # Outreach log export and summary
│
└── data/                       # All generated output files
    ├── influencers.db
    ├── influencers_all.csv
    ├── influencers_passed.csv
    ├── influencers_passed.json
    ├── personalized_messages.csv
    ├── personalized_messages.json
    ├── outreach_tracker.csv
    └── outreach_tracker.json
```

---

## Setup

**1. Clone and install dependencies**

```bash
git clone https://github.com/your-username/influencer-outreach.git
cd influencer-outreach
pip install -r requirements.txt
```

**2. Configure environment**

```bash
cp .env.example .env
```

Edit `.env` and fill in your keys:

```
OPENAI_API_KEY=sk-...
RAPIDAPI_KEY=...
GMAIL_SENDER_EMAIL=you@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
NICHE=fitness
```

**3. Run**

```bash
python main.py
```

---

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Optional | GPT-3.5 for message generation. Falls back to templates if missing. |
| `RAPIDAPI_KEY` | Optional | Instagram + YouTube scraping. Falls back to mock data if missing. |
| `GMAIL_SENDER_EMAIL` | Optional | Gmail address to send from |
| `GMAIL_APP_PASSWORD` | Optional | Gmail App Password (not your account password) |
| `NICHE` | Optional | Target niche. Default: `fitness` |

---

## Discovery methodology

The scraper targets three sources in order:

1. **RapidAPI Instagram Scraper** — fetches profiles via hashtag search for the chosen niche
2. **RapidAPI YouTube Search** — finds channels by keyword
3. **Collabstr public directory** — fallback for additional profiles

Only accounts with 5,000–100,000 followers are kept. Duplicates are removed by profile URL before saving to the database.

---

## Filtering logic

Each influencer is checked against:

- Follower count: 5,000–100,000
- Engagement rate: minimum 2.0%
- Niche: must be one of the supported categories
- Profile URL: must be present

Each record gets a `filter_status` of `passed` or `failed` with a plain-text `filter_reason`.

---

## Enrichment process

For each passed influencer:

- **Email**: scraped from their public profile or website. Skips social media domains (Instagram, YouTube, etc.) since they don't surface emails. Marked `Not Found` if unavailable.
- **Audience demographics**: assigned based on niche (age range, gender split, geography) using research-backed averages.
- **Website**: set to their channel/profile URL for YouTube creators, or a Linktree pattern for Instagram.

---

## AI personalization

- **With OpenAI key**: sends a structured prompt to `gpt-3.5-turbo` with the influencer's name, niche, content themes, follower count, and engagement rate. Temperature 0.85 for natural variation.
- **Without OpenAI key**: uses niche-specific fallback templates that dynamically inject the influencer's name and content themes. Each niche has a distinct tone and collaboration angle.

Both modes produce:
- Email pitch: 60–90 words, references niche and proposes a specific collaboration type
- Instagram DM: 15–30 words, short and conversational

---

## Sending mechanism

The sender reads from the database — only influencers who passed filtering, have a valid email, and haven't been contacted before are included.

- **Live mode**: sends via Gmail SMTP SSL (port 465) using an App Password
- **Simulation mode**: logs the outreach as `simulated` without sending — activated automatically when Gmail credentials are not set

Duplicate prevention: before every send, the system checks the `outreach_log` table. If a `sent` or `simulated` record exists for that influencer, it's skipped.

---

## Gmail App Password setup

Standard Gmail password won't work. You need an App Password:

1. Go to your Google Account → Security
2. Enable 2-Step Verification
3. Search "App passwords" → create one for "Mail"
4. Copy the 16-character password into `GMAIL_APP_PASSWORD` in `.env`

---

## Limitations

- Email addresses are scraped from public websites only. Most Instagram/YouTube profiles don't expose emails publicly, so `Not Found` is common and expected.
- Instagram DM sending via API is restricted by Meta's platform policies. The system generates DMs and logs them but does not automate sending.
- RapidAPI free tier has request limits. For 500+ influencers, a paid plan or additional sources are needed.
- Mock data (53 influencers) is provided for testing without any API keys.

---

## Scaling to 500+ influencers

- Add more hashtags per niche in `discovery/scraper.py`
- Add pagination to the Collabstr scraper
- Integrate Apify actors for deeper Instagram/TikTok scraping
- Swap SQLite for PostgreSQL by changing the connection in `database.py`
