from database import get_all_influencers, update_influencer
from config import MIN_FOLLOWERS, MAX_FOLLOWERS, MIN_ENGAGEMENT_RATE


VALID_NICHES = {"fitness", "beauty", "fashion", "tech", "gaming", "fintech", "parenting", "lifestyle"}


def run_filtering(target_niche: str = None):
    influencers = get_all_influencers()
    passed, failed = 0, 0

    for inf in influencers:
        reason = check_criteria(inf, target_niche)
        if reason is None:
            update_influencer(inf["id"], {"filter_status": "passed", "filter_reason": "Meets all criteria"})
            passed += 1
        else:
            update_influencer(inf["id"], {"filter_status": "failed", "filter_reason": reason})
            failed += 1

    print(f"\n[Filtering] Done — Passed: {passed} | Failed: {failed} | Total: {passed + failed}")
    return passed, failed


def check_criteria(inf: dict, target_niche: str = None) -> str | None:
    followers = inf.get("follower_count", 0)
    engagement = inf.get("engagement_rate", 0.0)
    niche = (inf.get("niche") or "").lower().strip()

    if followers < MIN_FOLLOWERS:
        return f"Follower count {followers} below minimum {MIN_FOLLOWERS}"

    if followers > MAX_FOLLOWERS:
        return f"Follower count {followers} above maximum {MAX_FOLLOWERS}"

    if engagement < MIN_ENGAGEMENT_RATE:
        return f"Engagement rate {engagement}% below minimum {MIN_ENGAGEMENT_RATE}%"

    if niche not in VALID_NICHES:
        return f"Niche '{niche}' not in supported categories"

    if target_niche and niche != target_niche.lower():
        return f"Niche '{niche}' does not match target '{target_niche}'"

    if not inf.get("profile_url"):
        return "Missing profile URL"

    return None


def get_passed_influencers():
    all_inf = get_all_influencers()
    return [i for i in all_inf if i.get("filter_status") == "passed"]


def print_filter_summary():
    all_inf = get_all_influencers()
    passed = [i for i in all_inf if i["filter_status"] == "passed"]
    failed = [i for i in all_inf if i["filter_status"] == "failed"]

    print("\n--- PASSED ---")
    for i in passed:
        print(f"  ✓ {i['name']} | {i['platform']} | {i['follower_count']:,} followers | {i['engagement_rate']}% eng | {i['niche']}")

    print("\n--- FAILED ---")
    for i in failed:
        print(f"  ✗ {i['name']} | Reason: {i['filter_reason']}")
