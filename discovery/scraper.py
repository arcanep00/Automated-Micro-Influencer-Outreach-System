import requests
from bs4 import BeautifulSoup
import time
import random
from config import RAPIDAPI_KEY, NICHE, MIN_FOLLOWERS, MAX_FOLLOWERS


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

NICHE_HASHTAGS = {
    "fitness": ["fitness", "fitnessmotivation", "workout", "gym", "healthylifestyle"],
    "fashion": ["fashion", "style", "ootd", "fashionblogger", "streetstyle"],
    "beauty": ["beauty", "skincare", "makeup", "beautytips", "glowup"],
    "tech": ["tech", "technology", "gadgets", "coding", "programming"],
    "gaming": ["gaming", "gamer", "esports", "videogames", "gamingsetup"],
    "lifestyle": ["lifestyle", "dailylife", "contentcreator", "influencer", "vlog"],
    "fintech": ["fintech", "personalfinance", "investing", "crypto", "moneymanagement"],
    "parenting": ["parenting", "momlife", "dadlife", "parenthood", "newborn"],
}


def fetch_from_collabstr(niche: str, max_pages: int = 5) -> list:
    influencers = []
    niche_map = {
        "fitness": "health-fitness",
        "fashion": "fashion",
        "beauty": "beauty",
        "tech": "technology",
        "gaming": "gaming",
        "lifestyle": "lifestyle",
        "fintech": "finance",
        "parenting": "family-parenting",
    }
    category = niche_map.get(niche, "lifestyle")

    for page in range(1, max_pages + 1):
        url = f"https://collabstr.com/influencers?category={category}&page={page}"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code != 200:
                break
            soup = BeautifulSoup(resp.text, "lxml")
            cards = soup.select(".influencer-card, .creator-card, [class*='influencer']")

            for card in cards:
                name_el = card.select_one("[class*='name'], h3, h4")
                url_el = card.select_one("a[href]")
                follower_el = card.select_one("[class*='follower'], [class*='count']")

                if not name_el or not url_el:
                    continue

                profile_url = url_el.get("href", "")
                if profile_url and not profile_url.startswith("http"):
                    profile_url = "https://collabstr.com" + profile_url

                follower_text = follower_el.get_text(strip=True) if follower_el else "0"
                follower_count = parse_follower_count(follower_text)

                influencers.append({
                    "name": name_el.get_text(strip=True),
                    "platform": "Instagram",
                    "profile_url": profile_url,
                    "follower_count": follower_count,
                    "engagement_rate": 0.0,
                    "niche": niche,
                    "content_themes": niche,
                })

            time.sleep(random.uniform(1.5, 3.0))

        except Exception:
            break

    return influencers


def fetch_from_rapidapi_instagram(niche: str, max_results: int = 60) -> list:
    if not RAPIDAPI_KEY:
        return []

    hashtags = NICHE_HASHTAGS.get(niche, ["lifestyle"])
    influencers = []
    seen_usernames = set()

    for hashtag in hashtags[:2]:
        url = "https://instagram-scraper-api2.p.rapidapi.com/v1/hashtag"
        params = {"hashtag": hashtag}
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "instagram-scraper-api2.p.rapidapi.com"
        }
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=15)
            if resp.status_code != 200:
                continue
            data = resp.json()
            posts = data.get("data", {}).get("medias", [])

            for post in posts:
                user = post.get("user", {})
                username = user.get("username", "")
                if not username or username in seen_usernames:
                    continue

                followers = user.get("follower_count", 0)
                if not (MIN_FOLLOWERS <= followers <= MAX_FOLLOWERS):
                    continue

                seen_usernames.add(username)
                influencers.append({
                    "name": user.get("full_name") or username,
                    "platform": "Instagram",
                    "profile_url": f"https://www.instagram.com/{username}/",
                    "follower_count": followers,
                    "engagement_rate": calculate_engagement(post),
                    "niche": niche,
                    "content_themes": hashtag,
                })

                if len(influencers) >= max_results:
                    break

        except Exception:
            continue

        time.sleep(1)

    return influencers


def fetch_from_youtube_rapidapi(niche: str, max_results: int = 20) -> list:
    if not RAPIDAPI_KEY:
        return []

    keywords = NICHE_HASHTAGS.get(niche, [niche])
    influencers = []

    for keyword in keywords[:2]:
        url = "https://youtube-search-and-download.p.rapidapi.com/search"
        params = {"query": f"{keyword} channel", "type": "c", "hl": "en", "gl": "US"}
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "youtube-search-and-download.p.rapidapi.com"
        }
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=15)
            if resp.status_code != 200:
                continue
            data = resp.json()
            contents = data.get("contents", [])

            for item in contents:
                channel = item.get("video", {})
                channel_id = channel.get("channelId", "")
                channel_name = channel.get("channelName", "")
                subscriber_text = channel.get("viewCountText", "0")

                if not channel_id or not channel_name:
                    continue

                influencers.append({
                    "name": channel_name,
                    "platform": "YouTube",
                    "profile_url": f"https://www.youtube.com/channel/{channel_id}",
                    "follower_count": parse_follower_count(subscriber_text),
                    "engagement_rate": 0.0,
                    "niche": niche,
                    "content_themes": keyword,
                })

        except Exception:
            continue

        time.sleep(1)

    return influencers


def calculate_engagement(post: dict) -> float:
    likes = post.get("like_count", 0)
    comments = post.get("comment_count", 0)
    followers = post.get("user", {}).get("follower_count", 1)
    if followers == 0:
        return 0.0
    return round(((likes + comments) / followers) * 100, 2)


def parse_follower_count(text: str) -> int:
    text = text.strip().upper().replace(",", "").replace(" ", "")
    try:
        if "K" in text:
            return int(float(text.replace("K", "")) * 1000)
        elif "M" in text:
            return int(float(text.replace("M", "")) * 1000000)
        else:
            digits = "".join(filter(str.isdigit, text))
            return int(digits) if digits else 0
    except ValueError:
        return 0


def run_discovery(niche: str = None) -> list:
    target_niche = niche or NICHE
    all_influencers = []

    print(f"[Discovery] Starting for niche: {target_niche}")

    instagram_results = fetch_from_rapidapi_instagram(target_niche)
    all_influencers.extend(instagram_results)
    print(f"[Discovery] Instagram: {len(instagram_results)} found")

    youtube_results = fetch_from_youtube_rapidapi(target_niche)
    all_influencers.extend(youtube_results)
    print(f"[Discovery] YouTube: {len(youtube_results)} found")

    if len(all_influencers) < 50:
        collabstr_results = fetch_from_collabstr(target_niche)
        all_influencers.extend(collabstr_results)
        print(f"[Discovery] Collabstr: {len(collabstr_results)} found")

    seen = set()
    unique = []
    for inf in all_influencers:
        url = inf.get("profile_url", "")
        if url and url not in seen:
            seen.add(url)
            unique.append(inf)

    print(f"[Discovery] Total unique influencers: {len(unique)}")
    return unique
