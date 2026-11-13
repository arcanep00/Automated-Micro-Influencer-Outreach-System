import sys
from database import init_db, insert_influencer, get_all_influencers
from discovery.scraper import run_discovery
from config import NICHE, MIN_INFLUENCERS_REQUIRED


def phase1_discover():
    print("\n=== Phase 1: Influencer Discovery ===\n")
    init_db()
    print("[DB] Database initialized")

    influencers = run_discovery(NICHE)

    if not influencers:
        print("[ERROR] No influencers found. Check your API keys or network.")
        sys.exit(1)

    saved = 0
    for inf in influencers:
        row_id = insert_influencer(inf)
        if row_id:
            saved += 1

    all_in_db = get_all_influencers()
    print(f"\n[Done] {saved} new influencers saved. Total in DB: {len(all_in_db)}")

    if len(all_in_db) < MIN_INFLUENCERS_REQUIRED:
        print(f"[WARNING] Only {len(all_in_db)} influencers found. Target is {MIN_INFLUENCERS_REQUIRED}+")
    else:
        print(f"[OK] Target of {MIN_INFLUENCERS_REQUIRED}+ influencers met.")

    return all_in_db


if __name__ == "__main__":
    phase1_discover()
