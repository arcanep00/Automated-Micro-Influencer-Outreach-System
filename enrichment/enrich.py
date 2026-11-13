import requests
import re
import time
import random
from bs4 import BeautifulSoup
from database import get_all_influencers, update_influencer
from filtering.filter import get_passed_influencers


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

NICHE_DEMOGRAPHICS = {
    "fitness": {"audience_age": "18-34", "audience_gender": "55% Female, 45% Male", "audience_geography": "US, UK, CA, AU"},
    "beauty": {"audience_age": "16-30", "audience_gender": "80% Female, 20% Male", "audience_geography": "US, UK, IN, AU"},
    "fashion": {"audience_age": "18-35", "audience_gender": "70% Female, 30% Male", "audience_geography": "US, UK, FR, IT"},
    "tech": {"audience_age": "20-40", "audience_gender": "35% Female, 65% Male", "audience_geography": "US, IN, DE, UK"},
    "gaming": {"audience_age": "16-28", "audience_gender": "25% Female, 75% Male", "audience_geography": "US, BR, DE, KR"},
    "fintech": {"audience_age": "24-45", "audience_gender": "40% Female, 60% Male", "audience_geography": "US, UK, SG, AU"},
    "parenting": {"audience_age": "25-40", "audience_gender": "72% Female, 28% Male", "audience_geography": "US, UK, CA, AU"},
    "lifestyle": {"audience_age": "20-38", "audience_gender": "60% Female, 40% Male", "audience_geography": "US, UK, AU, CA"},
}


SKIP_DOMAINS = ("instagram.com", "youtube.com", "tiktok.com", "facebook.com", "twitter.com", "linktr.ee")


def find_email_from_profile(profile_url: str) -> str:
    if any(domain in profile_url for domain in SKIP_DOMAINS):
        return "Not Found"
    try:
        resp = requests.get(profile_url, headers=HEADERS, timeout=6)
        if resp.status_code != 200:
            return "Not Found"
        text = resp.text
        emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
        filtered = [e for e in emails if not any(x in e.lower() for x in ["example", "test", "noreply", "support"])]
        return filtered[0] if filtered else "Not Found"
    except Exception:
        return "Not Found"


def enrich_demographics(inf: dict) -> dict:
    niche = (inf.get("niche") or "lifestyle").lower()
    return NICHE_DEMOGRAPHICS.get(niche, NICHE_DEMOGRAPHICS["lifestyle"])


def run_enrichment():
    influencers = get_passed_influencers()
    print(f"\n[Enrichment] Enriching {len(influencers)} passed influencers...")

    for inf in influencers:
        updates = {}

        email = find_email_from_profile(inf["profile_url"])
        updates["contact_email"] = email

        demographics = enrich_demographics(inf)
        updates.update(demographics)

        platform = inf.get("platform", "").lower()
        if platform == "youtube":
            updates["website"] = inf["profile_url"]
        else:
            username = inf["profile_url"].rstrip("/").split("/")[-1]
            updates["website"] = f"https://linktr.ee/{username}"

        update_influencer(inf["id"], updates)

        status = "✓ email found" if email != "Not Found" else "✗ no email"
        print(f"  [{status}] {inf['name']}")

    print(f"[Enrichment] Done — {len(influencers)} profiles enriched")


def print_enrichment_summary():
    passed = get_passed_influencers()
    with_email = [i for i in passed if i.get("contact_email") != "Not Found"]
    without_email = [i for i in passed if i.get("contact_email") == "Not Found"]

    print(f"\n[Enrichment Summary]")
    print(f"  Total passed: {len(passed)}")
    print(f"  With email:   {len(with_email)}")
    print(f"  Without email: {len(without_email)}")
