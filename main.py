import os
import openai
import requests

# ✅ Use new OpenAI client (v1.0+)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

repo = os.getenv("GITHUB_REPO") or ""
token = os.getenv("GH_TOKEN") or ""
pr_number = os.getenv("PR_NUMBER") or ""
pr_body = os.getenv("PR_BODY") or ""

# ✅ Ask OpenAI for a summary
response = client.chat.completions.create(
    model="gpt-4o",  # use "gpt-4o-mini" if that's what you prefer
    messages=[
        {"role": "system", "content": "You are a professional GitHub reviewer."},
        {"role": "user", "content": f"Summarize this pull request:\n\n{pr_body}"}
    ]
)

summary = response.choices[0].message.content

# ✅ Post comment back to GitHub PR
url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}
requests.post(url, headers=headers, json={"body": f"🤖 **Auto-summary by GPT-4**\n\n{summary}"})
