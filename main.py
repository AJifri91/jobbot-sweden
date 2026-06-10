import os
import webbrowser
from datetime import date

from db import init_db, save_job, save_rejected_job, is_job_seen
from fetcher import fetch_jobs
from scorer import score_all_jobs
from selector import select_top_jobs
from cover_letter import generate_swedish_cover_letter
from report_generator import generate_html_report

def main():
    print(f"=== JobBot starting – {date.today()} ===")
    init_db()

    print("Fetching jobs from JobTech API...")
    try:
        jobs = fetch_jobs()
        print(f"Fetched {len(jobs)} jobs total.")
    except Exception as e:
        print(f"❌ Fetching failed: {e}")
        return

    new_jobs = [job for job in jobs if not is_job_seen(job['id'])]
    print(f"{len(new_jobs)} new jobs to score (skipping {len(jobs) - len(new_jobs)} already seen).")

    if not new_jobs:
        print("Inga nya jobb idag.")
        return

    print("Scoring jobs...")
    try:
        scored_jobs = score_all_jobs(new_jobs)
    except Exception as e:
        print(f"❌ Scoring failed: {e}")
        return

    top_jobs = select_top_jobs(scored_jobs, min_score=60, limit=5)
    print(f"{len(top_jobs)} jobs made the shortlist (score ≥ 60).")

    top_ids = {job['id'] for job in top_jobs}
    rejected_jobs = [job for job in scored_jobs if job['id'] not in top_ids]

    if top_jobs:
        print("Saving top jobs to database...")
        for job in top_jobs:
            save_job(job, status='shortlisted')

    if rejected_jobs:
        print(f"Logging {len(rejected_jobs)} rejected jobs to database...")
        for job in rejected_jobs:
            save_rejected_job(job)

    if not top_jobs:
        print("Inga jobb över tröskeln idag. Försök igen imorgon.")
        return

    print("Generating Swedish cover letters...")
    jobs_with_letters = []
    for job in top_jobs:
        try:
            letter = generate_swedish_cover_letter(job)
            jobs_with_letters.append({'job': job, 'letter': letter})
            print(f"  ✅ Letter generated for: {job['title']} at {job['company']}")
        except Exception as e:
            print(f"  ⚠️ Cover letter failed for {job['title']}: {e}")
            jobs_with_letters.append({'job': job, 'letter': '[Misslyckades att generera brev]'})

    report_file = generate_html_report(jobs_with_letters)
    print(f"\n✅ Report saved to {report_file}. Opening browser...")
    report_path = os.path.abspath(report_file)
    webbrowser.open(f"file://{report_path}")

if __name__ == "__main__":
    main()