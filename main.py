from database import init_db, get_all_influencers
from discovery.mock_data import load_mock_data
from filtering.filter import run_filtering, print_filter_summary
from enrichment.enrich import run_enrichment, print_enrichment_summary
from enrichment.export import export_to_csv, export_to_json
from personalization.generate import run_personalization
from personalization.export_messages import export_messages_csv, export_messages_json, print_sample_messages
from sending.sender import run_sending
from tracker.tracker import export_tracker_csv, export_tracker_json, print_tracker_summary
from config import NICHE, MIN_INFLUENCERS_REQUIRED


def phase1():
    print("\n=== Phase 1: Foundation & Discovery ===\n")
    init_db()
    print("[DB] Database initialized")
    load_mock_data()
    all_in_db = get_all_influencers()
    print(f"[Done] Total influencers in DB: {len(all_in_db)}")
    if len(all_in_db) < MIN_INFLUENCERS_REQUIRED:
        print(f"[WARNING] Only {len(all_in_db)} found. Target is {MIN_INFLUENCERS_REQUIRED}+")
    else:
        print(f"[OK] Target of {MIN_INFLUENCERS_REQUIRED}+ met")


def phase2():
    print("\n=== Phase 2: Filtering, Enrichment & Export ===\n")
    run_filtering()
    print_filter_summary()
    run_enrichment()
    print_enrichment_summary()
    export_to_csv("influencers_all.csv")
    export_to_csv("influencers_passed.csv", passed_only=True)
    export_to_json("influencers_passed.json", passed_only=True)


def phase3():
    print("\n=== Phase 3: AI Personalization ===\n")
    run_personalization()
    export_messages_csv()
    export_messages_json()
    print_sample_messages(count=3)


def phase4():
    print("\n=== Phase 4: Sending Layer & Outreach Tracker ===\n")
    run_sending()
    export_tracker_csv()
    export_tracker_json()
    print_tracker_summary()


if __name__ == "__main__":
    phase1()
    phase2()
    phase3()
    phase4()
