# jobbot-sweden

AI job searcher for the Swedish market. Fetches live jobs from Arbetsförmedlingen, scores them against resume with Gemini 3.1 Flash-Lite, and generates Swedish cover letters.

# 🇸🇪 JobBot – AI Job Searcher for the Swedish Market

JobBot is a Python tool that automates daily job hunting from Arbetsförmedlingen's official JobTech API. It uses Google Gemini AI to score jobs against your CV and generates tailored Swedish cover letters – all locally.

## ✨ Features

- Fetches live job ads from the Swedish JobTech API
- Scores each job (0–100) based on your CV using Gemini 3.1 Flash‑Lite
- Provides AI reasoning and improvement tips for rejected jobs
- Saves shortlisted jobs to a SQLite database (prevents re‑scoring)
- Generates professional Swedish cover letters
- Outputs a clean HTML report with links and cover letters

## 🧰 Requirements

- Python 3.11 or higher
- Google Gemini API key (free tier from [Google AI Studio](https://aistudio.google.com/))
- Internet connection (for API calls)

## 🚀 Installation

Clone the repository and set up the environment:

```bash
git clone https://github.com/yourusername/jobbot-sweden.git
cd jobbot-sweden
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

## 🔑 API Key Setup

1. Go to [Google AI Studio](https://aistudio.google.com/), sign in, and create an API key.
2. Create a file named `.env` in the project root with:

```bash
GOOGLE_API_KEY=your_actual_key_here
```

## 📄 Prepare Your CV

Place your CV as a PDF file in the project folder and name it `cv.pdf`.

## 🎯 Customise Job Search

By default, JobBot targets **Data/IT** roles (e.g., “data engineer”, “data scientist”, “ML engineer”).  
To change the search:

- Edit `fetcher.py`: modify the `keywords` variable (space‑separated job title phrases, for example: `"project manager" "business consultant"`).
- The `occupation-field` parameter (Swedish taxonomy for Data/IT) is **not** included by default. If you know the taxonomy code for your field, you can add it to the `params` dictionary:  
  `"occupation-field": "your_taxonomy_code"`.  
  (You can find codes on the [JobTech API documentation](https://jobtechdev.se/).)

By default, the bot excludes job titles containing words like **senior**, **lead**, **manager**, **expert**, **principal**, or **director**. If you want to include such roles, simply remove the unwanted words from the `exclude_words` set in `fetcher.py`.

## 🏃 Running the Bot

```bash
python main.py
```

The bot will:

- Fetch up to 100 new jobs (excluding already‑seen ones)
- Score each job with Gemini
- Save shortlisted jobs (score ≥ 60) to `jobs.db`
- Log rejected jobs (with improvement tips) to `rejected_log`
- Generate an HTML report `shortlist.html` and open it in your browser

## 📊 Understanding the Output

- **`shortlist.html`** – Contains the top 5 jobs (or fewer) with score, AI reasoning, apply link, and a tailored Swedish cover letter.
- **`jobs.db`** – SQLite database with shortlisted jobs (used for deduplication).
- **`rejected_log`** – Stores rejected jobs and the AI’s suggestions for improving your CV.

To view rejected jobs with their improvement tips, run:

```bash
python show_rejected.py
```

## ⚙️ Configuration Options (in `main.py`)

- `min_score`: Minimum score to be shortlisted (default `60`)
- `limit`: Maximum number of jobs in the daily shortlist (default `5`)

## 🛡️ Rate Limits & Model Choice

We use **Gemini 3.1 Flash‑Lite** because its free tier offers:

- 15 requests per minute (RPM)
- 500 requests per day (RPD)
- 250,000 tokens per minute (TPM)

The bot automatically sleeps 4 seconds between API calls to stay under 15 RPM. For 100 jobs/day, the free quota is more than sufficient.

## ❗ Limitations

- The bot does **not** automatically submit applications – you must manually apply via the provided links and cover letters.
- Designed exclusively for the Swedish JobTech API. For other job boards, you would need to write a different `fetcher`.

## 🤝 Contributing

Feel free to fork and adapt. If you find a bug, open an issue.

## 📄 License

