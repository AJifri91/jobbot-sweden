import os
import time
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from cv_reader import extract_cv_text

load_dotenv()

# FIX 1: Move response_mime_type to a top-level parameter to kill the UserWarning
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0,
    max_retries=5,
    response_mime_type="application/json" 
)

CV_TEXT = extract_cv_text()

def score_job(job):
    prompt = f"""
    You are an expert technical recruiter matching candidates to jobs.
    Compare the candidate's CV with the job description.

    CANDIDATE CV:
    {CV_TEXT[:8000]}

    JOB TITLE: {job['title']}
    JOB DESCRIPTION:
    {job['description'][:6000]}

    INSTRUCTIONS:
    1. Provide a matching score 0-100 based on technical skills, tools, and background.
    2. Provide a brief reasoning (2-3 sentences) explaining the score.
    3. If score <60, list 2-3 specific technical skills/experiences to add to reach 60+.

    OUTPUT FORMAT: valid JSON object: {{"score": 75, "reasoning": "..."}}
    """
    try:
        response = llm.invoke(prompt)
        
        # FIX 2: Intercept the response and flatten it if LangChain returns it as a list
        raw = response.content
        if isinstance(raw, list):
            raw = "".join([block.get("text", "") if isinstance(block, dict) else str(block) for block in raw])
            
        data = json.loads(raw.strip())
        score = int(data.get("score", 0))
        reasoning = data.get("reasoning", "Ingen motivering angiven.")
    except Exception as e:
        print(f"⚠️ Error scoring {job['title']}: {e}")
        score = 0
        reasoning = "Misslyckades att hämta score."
    return score, reasoning

def score_all_jobs(jobs):
    """Score all jobs respecting 15 RPM (4 sec sleep)."""
    scored = []
    for i, job in enumerate(jobs):
        score, reasoning = score_job(job)
        job['score'] = score
        job['reasoning'] = reasoning
        scored.append(job)
        print(f"  [{i+1}/{len(jobs)}] Scored: {job['title']} -> {score}/100")
        if i < len(jobs) - 1:
            time.sleep(4)
    return scored