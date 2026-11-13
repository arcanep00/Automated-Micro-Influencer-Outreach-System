import sys
from database import init_db, insert_influencer, get_all_influencers
from discovery.mock_data import load_mock_data
from filtering.filter import run_filtering, print_filter_summary
from enrichment.enrich import run_enrichment, print_enrichment_summary
from enrichment.export import export_to_csv, export_to_json
from config import NICHE, MIN_INFLUENCERS_REQUIRED


def phase1():
    print("\n=== Phase 1: Foundation & Discovery ===\n")
    init_db()
    print("[DB] Database initialized")
    total = load_mock_data()
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


if __name__ == "__main__":
    phase1()
    phase2()
