from datetime import datetime

def generate_html_report(jobs_with_letters, output_file="shortlist.html"):
    today = datetime.now().strftime('%Y-%m-%d')
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">;
    <title>Job Shortlist - {today}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 30px; background: #f9f9f9; }}
        h1 {{ color: #333; }}
        .job {{ border: 1px solid #ccc; margin: 20px 0; padding: 20px; background: white; border-radius: 6px; }}
        .score {{ font-weight: bold; color: green; font-size: 1.1em; }}
        .score.low {{ color: orange; }}
        .reasoning {{ background: #eef7f2; padding: 10px; border-left: 4px solid #28a745; margin: 10px 0; border-radius: 4px; font-style: italic; }}
        a {{ color: #0066cc; font-size: 1.05em; text-decoration: none; font-weight: bold; }}
        a:hover {{ text-decoration: underline; }}
        pre {{ white-space: pre-wrap; background: #f5f5f5; padding: 12px; border-radius: 4px; font-size: 0.95em; border: 1px solid #ddd; }}
        .meta {{ color: #666; margin-bottom: 8px; font-size: 1.1em; }}
    </style>
</head>
<body>
    <h1>📋 Job Shortlist – {today}</h1>
    <p>Top matches today. Click each link to apply manually, then copy the cover letter below it.</p>
"""
    for item in jobs_with_letters:
        job = item['job']
        letter = item['letter']
        score = job.get('score', 0)
        reasoning = job.get('reasoning', 'Ingen motivering tillgänglig.')
        
        score_class = "score" if score >= 80 else "score low"
        url = job.get('url', 'Ingen länk')
        link_html = f'<a href="{url}" target="_blank">Öppna ansökningslänk →</a>' if url != 'Ingen länk' else '<em>Ingen länk tillgänglig</em>'

        html += f"""
        <div class="job">
            <h2>{job.get('title', 'Okänd titel')}</h2>
            <p class="meta">🏢 <strong>{job.get('company', 'Okänt företag')}</strong></p>
            <p class="{score_class}">Matchpoäng: {score}/100</p>
            
            <div class="reasoning"><strong>AI Analys:</strong> {reasoning}</div>
            
            <p style="margin-top: 15px;">{link_html}</p>
            <h3>Personligt brev (svenska):</h3>
            <pre>{letter}</pre>
        </div>
        """

    html += """
</body>
</html>
"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    return output_file