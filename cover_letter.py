import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from cv_reader import extract_cv_text

# Load environment variables from .env file
load_dotenv()

# Initialize the model (it will automatically use the GOOGLE_API_KEY from environment)
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.7,
    # Pass directly as a top-level LangChain parameter (must be lowercase)
    thinking_level="medium" 
)
CV_TEXT = extract_cv_text()

def generate_swedish_cover_letter(job):
    prompt = f"""
    Du är en professionell karriärrådgivare. Skriv ett övertygande personligt brev på svenska för jobbet nedan.
    Använd specifika detaljer från kandidatens CV (se nedan) för att visa varför han passar rollen. Koppla detaljer från cv till jobb beskrivning. Jobben togs från arbetsförmedlingen webbplats

    CV:
    {CV_TEXT[:3000]}

    Jobbtitel: {job['title']}
    Företag: {job['company']}
    Arbetsbeskrivning: {job['description'][:1000]}

    Krav:
    - Kring 225 ord
    - Professionell ton
    - Nämn minst två relevanta erfarenheter eller färdigheter från CV:t
    - Lägg till i slutet: "P.S. Jag är berättigad till nystartsjobb via Arbetsförmedlingen, vilket innebär ekonomiskt stöd till arbetsgivaren vid en anställning."
    - Skriv ENDAST brevet, ingen inledning eller förklaring
    """
    response = llm.invoke(prompt)
    
    # Handle the response if it's a list (just like in scorer.py)
    raw = response.content
    if isinstance(raw, list):
        raw = "".join([block.get("text", "") if isinstance(block, dict) else str(block) for block in raw])
    
    return raw.strip()