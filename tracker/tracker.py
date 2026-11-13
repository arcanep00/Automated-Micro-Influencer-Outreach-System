import csv
import json
import os
import sqlite3
from config import DB_PATH, DATA_DIR


def get_outreach_log() -> list:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute("""
        SELECT i.name as influencer, ol.email, ol.message_type,
               ol.sent_at, ol.status
        FROM outreach_log ol
        JOIN influencers i ON i.id = ol.influencer_id
        ORDER BY ol.sent_at DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def export_tracker_csv():
    log = get_outreach_log()
    if not log:
        print("[Tracker] No outreach log entries yet")
        return

    filepath = os.path.join(DATA_DIR, "outreach_tracker.csv")
    fields = ["influencer", "email", "message_type", "sent_at", "status"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(log)

    print(f"[Tracker] CSV saved: {filepath} ({len(log)} records)")
    return filepath


def export_tracker_json():
    log = get_outreach_log()
    if not log:
        print("[Tracker] No outreach log entries yet")
        return

    filepath = os.path.join(DATA_DIR, "outreach_tracker.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, default=str)

    print(f"[Tracker] JSON saved: {filepath} ({len(log)} records)")
    return filepath


def print_tracker_summary():
    log = get_outreach_log()
    if not log:
        print("[Tracker] No records found")
        return

    statuses = {}
    for entry in log:
        s = entry["status"]
        statuses[s] = statuses.get(s, 0) + 1

    print("\n[Outreach Tracker Summary]")
    for status, count in statuses.items():
        print(f"  {status}: {count}")
    print(f"  Total: {len(log)}")

    print("\n[Recent Outreach Log]")
    for entry in log[:10]:
        print(f"  {entry['influencer']:<20} {entry['email']:<30} {entry['status']:<12} {entry['sent_at']}")
