import csv
import json
import os
from personalization.generate import get_all_messages
from config import DATA_DIR


def export_messages_csv():
    messages = get_all_messages()
    if not messages:
        print("[Export] No messages to export")
        return

    filepath = os.path.join(DATA_DIR, "personalized_messages.csv")
    fields = ["name", "platform", "niche", "contact_email", "email_pitch", "instagram_dm", "generated_at"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(messages)

    print(f"[Export] Messages CSV saved: {filepath} ({len(messages)} records)")
    return filepath


def export_messages_json():
    messages = get_all_messages()
    if not messages:
        print("[Export] No messages to export")
        return

    filepath = os.path.join(DATA_DIR, "personalized_messages.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, default=str)

    print(f"[Export] Messages JSON saved: {filepath} ({len(messages)} records)")
    return filepath


def print_sample_messages(count: int = 3):
    messages = get_all_messages()
    print(f"\n{'='*60}")
    print("SAMPLE PERSONALIZED MESSAGES")
    print('='*60)

    for msg in messages[:count]:
        print(f"\nInfluencer : {msg['name']} ({msg['platform']} | {msg['niche']})")
        print(f"Email      : {msg['contact_email']}")
        print(f"\n--- Email Pitch ---")
        print(msg['email_pitch'])
        print(f"\n--- Instagram DM ---")
        print(msg['instagram_dm'])
        print("-" * 60)
