def select_top_jobs(jobs, min_score=60, limit=5):
    filtered = [j for j in jobs if j.get('score', 0) >= min_score]
    filtered.sort(key=lambda x: x.get('score', 0), reverse=True)
    return filtered[:limit]
