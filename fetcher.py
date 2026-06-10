import requests

def fetch_jobs():
    url = "https://jobsearch.api.jobtechdev.se/search"
    headers = {"accept": "application/json"}

    # FIX 1: Remove the literal 'OR' text. The API treats space-separated 
    # exact phrases inside quotes as a compound multi-phrase search.
    keywords = (
        '"data engineer" "data analyst" "data scientist" '
        '"data architect" "data developer" "machine learning" '
        '"ML engineer" "AI engineer" "business intelligence"'
    )

    params = {
        # FIX 2: Uncomment this safety rail! It locks the search strictly to the Data/IT industry.
        "occupation-field": "apaJ_2ja_LuF",  
        "q": keywords,
        "limit": 100,  # Increased limit since your results will be drastically cleaner now
        "offset": 0,
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    jobs = []
    
    # Words to exclude from job titles (case-insensitive)
    exclude_words = {"senior", "lead", "expert", "principal", "manager", "director"}
    
    for hit in data.get("hits", []):
        title = hit.get("headline", "")
        title_lower = title.lower()
        
        # Double check that your local exclusion loop checks substrings cleanly
        if any(word in title_lower for word in exclude_words):
            continue
        
        jobs.append({
            "id": hit.get("id"),
            "title": title,
            "company": hit.get("employer", {}).get("name"),
            "description": hit.get("description", {}).get("text", ""),
            "url": hit.get("webpage_url", "")
        })
        
    return jobs