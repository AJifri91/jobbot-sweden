import sqlite3
import os
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'jobs.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Main jobs table (only shortlisted jobs go here)
    c.execute('''CREATE TABLE IF NOT EXISTS jobs
                 (id TEXT PRIMARY KEY,
                  title TEXT,
                  company TEXT,
                  description TEXT,
                  url TEXT,
                  score INTEGER,
                  status TEXT,
                  daily_batch_date DATE,
                  reasoning TEXT)''')
    # Separate table for rejected jobs (not marked as seen)
    c.execute('''CREATE TABLE IF NOT EXISTS rejected_log
                 (id TEXT PRIMARY KEY,
                  title TEXT,
                  company TEXT,
                  score INTEGER,
                  reasoning TEXT,
                  batch_date DATE)''')
    conn.commit()
    conn.close()

def save_job(job, status='shortlisted'):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO jobs 
                 (id, title, company, description, url, score, status, daily_batch_date, reasoning)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (job['id'], job['title'], job['company'], job['description'],
               job['url'], job.get('score'), status, date.today(), job.get('reasoning', '')))
    conn.commit()
    conn.close()

def save_rejected_job(job):
    """Store rejected job in separate log – not considered 'seen'."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO rejected_log
                 (id, title, company, score, reasoning, batch_date)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (job['id'], job['title'], job['company'],
               job.get('score'), job.get('reasoning', ''), date.today()))
    conn.commit()
    conn.close()

def is_job_seen(job_id):
    """Check only the main jobs table (shortlisted jobs)."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT 1 FROM jobs WHERE id = ?", (job_id,))
    result = c.fetchone()
    conn.close()
    return result is not None