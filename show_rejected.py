import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'jobs.db')

def show_rejected():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, company, score, reasoning, batch_date
        FROM rejected_log
        ORDER BY batch_date DESC, score DESC
    """)
    rows = cursor.fetchall()
    if not rows:
        print("No rejected jobs logged.")
        return
    print("\n=== REJECTED JOBS (with AI improvement suggestions) ===\n")
    for i, (title, company, score, reasoning, date) in enumerate(rows, 1):
        print(f"{i}. {title} at {company} (Score: {score}/100) – {date}")
        # Display full reasoning (which includes suggestions)
        print(f"   AI analysis: {reasoning}\n")
    conn.close()

if __name__ == "__main__":
    show_rejected()