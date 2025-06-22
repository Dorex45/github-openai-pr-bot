import os
import openai
import requests

# ---------- Configuration ----------
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

repo      = os.getenv("GITHUB_REPO")       # e.g. Dorex45/github-openai-pr-bot
token     = os.getenv("GH_TOKEN")          # GitHub PAT from secrets
pr_number = os.getenv("PR_NUMBER")         # Numeric ID of pull request
pr_body   = os.getenv("PR_BODY") or ""     # PR description text
# ------------------------------------

# 1️⃣  Ask GPT-4 (or GPT-4o-mini) for a summary
response = client.chat.completions.create(
    model="gpt-4o-mini",     # use gpt-4o or gpt-4o-mini if you have it; fallback to gpt-4o-mini
    messages=[
        {"role": "system", "content": "You are a professional GitHub reviewer."},
        {"role": "user",   "content": f"Summarize this pull-request description:\n\n{pr_body}"}
    ]
)
summary = response.choices[0].message.content

# 2️⃣  Post the summary as a PR comment
comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}
requests.post(comment_url, headers=headers, json={
    "body": f"🤖 **Auto-summary by GPT-4**\n\n{summary}"
})
