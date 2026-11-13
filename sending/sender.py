import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import GMAIL_SENDER_EMAIL, GMAIL_APP_PASSWORD, DB_PATH


def get_outreach_queue() -> list:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute("""
        SELECT i.id as influencer_id, i.name, i.contact_email, i.niche,
               m.email_pitch, m.instagram_dm
        FROM influencers i
        JOIN messages m ON m.influencer_id = i.id
        WHERE i.filter_status = 'passed'
          AND i.contact_email != 'Not Found'
          AND i.contact_email IS NOT NULL
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def already_sent(influencer_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    row = cur.execute("""
        SELECT id FROM outreach_log
        WHERE influencer_id = ? AND status IN ('sent', 'simulated')
    """, (influencer_id,)).fetchone()
    conn.close()
    return row is not None


def log_outreach(influencer_id: int, email: str, status: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO outreach_log (influencer_id, email, message_type, sent_at, status)
        VALUES (?, ?, 'email', ?, ?)
    """, (influencer_id, email, datetime.utcnow().isoformat(), status))
    conn.commit()
    conn.close()


def send_email(to_email: str, name: str, body: str) -> bool:
    if not GMAIL_SENDER_EMAIL or not GMAIL_APP_PASSWORD:
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Collaboration Opportunity — {name}"
    msg["From"] = GMAIL_SENDER_EMAIL
    msg["To"] = to_email
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_SENDER_EMAIL, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_SENDER_EMAIL, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"  [SMTP error] {e}")
        return False


def run_sending(simulate: bool = None):
    queue = get_outreach_queue()

    if simulate is None:
        simulate = not (GMAIL_SENDER_EMAIL and GMAIL_APP_PASSWORD)

    mode = "SIMULATION" if simulate else "LIVE"
    print(f"\n[Sending] Mode: {mode}")
    print(f"[Sending] {len(queue)} influencers with valid emails in queue\n")

    sent, skipped, failed = 0, 0, 0

    for inf in queue:
        if already_sent(inf["influencer_id"]):
            print(f"  [skip] {inf['name']} — already sent")
            skipped += 1
            continue

        if simulate:
            log_outreach(inf["influencer_id"], inf["contact_email"], "simulated")
            print(f"  [simulated] {inf['name']} <{inf['contact_email']}>")
            sent += 1
        else:
            success = send_email(inf["contact_email"], inf["name"], inf["email_pitch"])
            status = "sent" if success else "failed"
            log_outreach(inf["influencer_id"], inf["contact_email"], status)

            if success:
                print(f"  [sent] {inf['name']} <{inf['contact_email']}>")
                sent += 1
            else:
                print(f"  [failed] {inf['name']} <{inf['contact_email']}>")
                failed += 1

    print(f"\n[Sending] Done — Sent/Simulated: {sent} | Skipped: {skipped} | Failed: {failed}")
    return sent, skipped, failed
