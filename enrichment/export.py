import csv
import json
import os
from database import get_all_influencers
from filtering.filter import get_passed_influencers
from config import DATA_DIR


def export_to_csv(filename: str = "influencers.csv", passed_only: bool = False):
    influencers = get_passed_influencers() if passed_only else get_all_influencers()
    if not influencers:
        print("[Export] No data to export")
        return

    filepath = os.path.join(DATA_DIR, filename)
    fields = ["name", "platform", "follower_count", "engagement_rate", "niche",
              "contact_email", "profile_url", "content_themes", "filter_status",
              "filter_reason", "audience_age", "audience_gender", "audience_geography", "website"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(influencers)

    print(f"[Export] CSV saved: {filepath} ({len(influencers)} records)")
    return filepath


def export_to_json(filename: str = "influencers.json", passed_only: bool = False):
    influencers = get_passed_influencers() if passed_only else get_all_influencers()
    if not influencers:
        print("[Export] No data to export")
        return

    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(influencers, f, indent=2, default=str)

    print(f"[Export] JSON saved: {filepath} ({len(influencers)} records)")
    return filepath
