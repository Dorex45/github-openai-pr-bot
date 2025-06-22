import os
import openai
import requests

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

repo      = os.getenv("GITHUB_REPO")
token     = os.getenv("GH_TOKEN")
pr_number = os.getenv("PR_NUMBER")
pr_body   = os.getenv("PR_BODY")

# ➜ request with the new interface
response = client.chat.completions.create(
    model="gpt-4o-mini",          # or gpt-4o if you have access
    messages=[
        {"role": "system", "content": "You are a professional GitHub reviewer."},
        {"role": "user",   "content": f"Summarize this pull-request description:\n\n{pr_body}"}
    ]
)
summary = response.choices[0].message.content

# comment on the PR
url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}
requests.post(url, headers=headers, json={"body": f"🤖 **Auto-summary by GPT-4**\n\n{summary}"})
