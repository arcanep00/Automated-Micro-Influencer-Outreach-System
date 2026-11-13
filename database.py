import sqlite3
from config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS influencers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            platform TEXT NOT NULL,
            profile_url TEXT UNIQUE NOT NULL,
            follower_count INTEGER,
            engagement_rate REAL,
            niche TEXT,
            content_themes TEXT,
            contact_email TEXT DEFAULT 'Not Found',
            website TEXT,
            audience_age TEXT,
            audience_gender TEXT,
            audience_geography TEXT,
            filter_status TEXT DEFAULT 'pending',
            filter_reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            influencer_id INTEGER NOT NULL,
            email_pitch TEXT,
            instagram_dm TEXT,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (influencer_id) REFERENCES influencers(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS outreach_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            influencer_id INTEGER NOT NULL,
            email TEXT,
            message_type TEXT,
            sent_at TIMESTAMP,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (influencer_id) REFERENCES influencers(id)
        )
    """)

    conn.commit()
    conn.close()


def insert_influencer(data: dict):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT OR IGNORE INTO influencers 
            (name, platform, profile_url, follower_count, engagement_rate, niche, content_themes)
            VALUES (:name, :platform, :profile_url, :follower_count, :engagement_rate, :niche, :content_themes)
        """, data)
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_all_influencers():
    conn = get_connection()
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM influencers").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_influencer(influencer_id: int, fields: dict):
    conn = get_connection()
    cur = conn.cursor()
    set_clause = ", ".join(f"{k} = :{k}" for k in fields)
    fields["id"] = influencer_id
    cur.execute(f"UPDATE influencers SET {set_clause} WHERE id = :id", fields)
    conn.commit()
    conn.close()
