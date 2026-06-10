import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'jobs.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT id, title, company, score, status, daily_batch_date, reasoning FROM jobs ORDER BY score DESC;")
rows = cursor.fetchall()

if not rows:
    print("No jobs found in database.")
else:
    print(f"\n{'ID':<15} {'Title':<35} {'Company':<20} {'Score':<5} {'Status':<13} {'Date':<12}")
    print("-" * 110)
    for row in rows:
        print(f"{row[0]:<15} {row[1][:35]:<35} {row[2][:20]:<20} {str(row[3]):<5} {row[4]:<13} {str(row[5]):<12}")
        if row[6]:  # reasoning exists
            print(f"   Reasoning: {row[6]}")
        else:
            print("   Reasoning: None")
        print()  # empty line between jobs

conn.close()