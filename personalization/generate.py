import sqlite3
from openai import OpenAI
from config import OPENAI_API_KEY, DB_PATH
from filtering.filter import get_passed_influencers


client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def build_email_prompt(inf: dict) -> str:
    return f"""Write a collaboration outreach email pitch from a brand to an influencer. Keep it 60-90 words.

Influencer details:
- Name: {inf['name']}
- Platform: {inf['platform']}
- Niche: {inf['niche']}
- Content themes: {inf['content_themes']}
- Followers: {inf['follower_count']:,}
- Engagement rate: {inf['engagement_rate']}%
- Audience: {inf.get('audience_age', 'N/A')} age, {inf.get('audience_gender', 'N/A')}

The email should feel personal, not templated. Reference their niche and content. Propose a collaboration angle that fits them. No subject line, just the email body."""


def build_dm_prompt(inf: dict) -> str:
    return f"""Write a short Instagram DM from a brand to an influencer. Keep it 15-30 words.

Influencer details:
- Name: {inf['name']}
- Niche: {inf['niche']}
- Content themes: {inf['content_themes']}
- Platform: {inf['platform']}

The DM should feel natural and conversational, referencing their content. No hashtags, no emojis overload."""


def generate_with_openai(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85,
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()


def generate_email_fallback(inf: dict) -> str:
    name = inf["name"]
    niche = inf["niche"]
    themes = inf["content_themes"]
    followers = f"{inf['follower_count']:,}"
    eng = inf["engagement_rate"]

    templates = {
        "fitness": f"Hi {name}, your dedication to {themes} content is exactly what our fitness brand is looking for. With your {followers} engaged followers and {eng}% engagement, we'd love to explore a collaboration — whether that's a sponsored post, affiliate deal, or brand ambassador role. Let's connect and see what works best for you.",
        "beauty": f"Hi {name}, your {themes} content genuinely stands out — the way you connect with your audience is impressive. We're reaching out because we think there's a natural fit between your work and our beauty brand. We'd love to discuss a UGC campaign or product collaboration. Would you be open to a quick chat?",
        "fashion": f"Hi {name}, your eye for {themes} is exactly the aesthetic our brand resonates with. We've been following your content and think your audience would genuinely love what we're building. We'd love to explore a paid collaboration or affiliate partnership. Let us know if you're interested.",
        "tech": f"Hi {name}, your {themes} content is both informative and engaging — exactly the kind of creator voice we look for. We'd love to explore a sponsored review or affiliate collaboration with you. Your audience's trust in your recommendations makes this a compelling opportunity for both sides.",
        "gaming": f"Hi {name}, your {themes} content has the kind of authentic energy our brand is looking for. We'd love to partner on a sponsored stream, product placement, or affiliate deal that fits naturally with your content. Let's see if there's a good fit here.",
        "fintech": f"Hi {name}, your ability to break down {themes} for a broad audience is a skill we deeply respect. We'd love to explore a collaboration — whether it's a sponsored video, affiliate campaign, or brand partnership. Your audience's trust makes this a great opportunity.",
        "parenting": f"Hi {name}, your honest and relatable {themes} content is exactly what parents need — and what our brand values. We'd love to discuss a collaboration that feels genuine to your audience, whether that's a product feature, affiliate deal, or ambassador role.",
        "lifestyle": f"Hi {name}, your {themes} content has a natural, authentic quality that really resonates. We'd love to explore a collaboration opportunity that aligns with your personal brand. Let us know if you'd be open to a quick conversation about a partnership.",
    }

    return templates.get(niche, f"Hi {name}, we love your {niche} content and would love to explore a collaboration. Your engaged audience and authentic voice make you a great fit for our brand. Let's connect!")


def generate_dm_fallback(inf: dict) -> str:
    name = inf["name"]
    niche = inf["niche"]
    themes = (inf["content_themes"] or niche).split(",")[0].strip()

    dms = {
        "fitness": f"Hi {name}, your {themes} content is exactly what we've been looking for — would love to chat about a collab!",
        "beauty": f"Hi {name}, loved your recent {themes} content. Think your audience would be a perfect fit for our upcoming campaign!",
        "fashion": f"Hi {name}, your {themes} style is stunning. We'd love to explore a collab — are you open to it?",
        "tech": f"Hi {name}, your {themes} reviews are genuinely helpful. We'd love to work together on something — interested?",
        "gaming": f"Hi {name}, your {themes} content is awesome. We'd love to discuss a partnership that fits your style!",
        "fintech": f"Hi {name}, your {themes} breakdowns are top notch. Would love to explore a collab — open to chat?",
        "parenting": f"Hi {name}, your {themes} content is so relatable. We'd love to partner with you on something authentic!",
        "lifestyle": f"Hi {name}, your {themes} content really connects. We'd love to explore a collaboration with you!",
    }

    return dms.get(niche, f"Hi {name}, love your {niche} content! Would love to discuss a potential collab with you.")


def generate_messages_for(inf: dict) -> tuple[str, str]:
    if client:
        try:
            email_pitch = generate_with_openai(build_email_prompt(inf))
            dm = generate_with_openai(build_dm_prompt(inf))
            return email_pitch, dm
        except Exception as e:
            print(f"  [OpenAI error] {e} — using fallback")

    return generate_email_fallback(inf), generate_dm_fallback(inf)


def save_messages(influencer_id: int, email_pitch: str, instagram_dm: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO messages (influencer_id, email_pitch, instagram_dm)
        VALUES (?, ?, ?)
    """, (influencer_id, email_pitch, instagram_dm))
    conn.commit()
    conn.close()


def messages_already_generated(influencer_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    row = cur.execute("SELECT id FROM messages WHERE influencer_id = ?", (influencer_id,)).fetchone()
    conn.close()
    return row is not None


def run_personalization():
    influencers = get_passed_influencers()
    print(f"\n[Personalization] Generating messages for {len(influencers)} influencers...")
    mode = "OpenAI" if client else "Fallback templates"
    print(f"[Personalization] Mode: {mode}\n")

    for inf in influencers:
        if messages_already_generated(inf["id"]):
            print(f"  [skip] {inf['name']} — already generated")
            continue

        email_pitch, dm = generate_messages_for(inf)
        save_messages(inf["id"], email_pitch, dm)
        print(f"  [done] {inf['name']}")

    print(f"\n[Personalization] Complete — {len(influencers)} messages generated")


def get_all_messages():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute("""
        SELECT i.name, i.platform, i.niche, i.contact_email,
               m.email_pitch, m.instagram_dm, m.generated_at
        FROM messages m
        JOIN influencers i ON i.id = m.influencer_id
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]
