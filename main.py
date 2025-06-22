import os
import openai
import requests

openai.api_key = os.getenv("OPENAI_API_KEY")
repo = os.getenv("GITHUB_REPO")
token = os.getenv("GH_TOKEN")
pr_number = os.getenv("PR_NUMBER")
pr_body = os.getenv("PR_BODY")

# Generate summary with GPT-4
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a professional GitHub reviewer."},
        {"role": "user", "content": f"Summarize this pull request description:\n\n{pr_body}"}
    ]
)
summary = response['choices'][0]['message']['content']

# Comment on PR
url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}
payload = {
    "body": f"🤖 **Auto Summary by GPT-4**:\n\n{summary}"
}
requests.post(url, headers=headers, json=payload)
