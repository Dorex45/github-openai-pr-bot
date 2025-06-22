import os
import openai
import requests

# ✅ Load OpenAI with new v1 SDK interface
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Read GitHub env variables
repo = os.getenv("GITHUB_REPO")
token = os.getenv("GH_TOKEN")
pr_number = os.getenv("PR_NUMBER")
pr_body = os.getenv("PR_BODY") or ""

# ✅ Ask GPT-4 for a PR summary
response = client.chat.completions.create(
    model="gpt-4o",  # or gpt-4o-mini
    messages=[
        {"role": "system", "content": "You are a professional GitHub reviewer."},
        {"role": "user", "content": f"Summarize this pull request:\n\n{pr_body}"}
    ]
)

summary = response.choices[0].message.content

# ✅ Post summary back to GitHub as a comment
url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}
requests.post(url, headers=headers, json={"body": f"🤖 **Auto-summary by GPT-4**\n\n{summary}"})
