import os, requests, openai

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

repo      = os.getenv("GITHUB_REPO")          # e.g. Dorex45/github-openai-pr-bot
token     = os.getenv("GH_TOKEN")
pr_number = os.getenv("PR_NUMBER")
pr_body   = os.getenv("PR_BODY") or ""

# 1️⃣  Ask GPT-4 for a summary
chat = client.chat.completions.create(
    model="gpt-4o-mini",                      # use gpt-4o if enabled
    messages=[
        {"role": "system",
         "content": "You are a professional GitHub reviewer."},
        {"role": "user",
         "content": f"Summarise this pull-request description:\n\n{pr_body}"}
    ]
)
summary = chat.choices[0].message.content

# 2️⃣  Post the summary back to the PR
comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
requests.post(
    comment_url,
    headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    },
    json={"body": f"🤖 **Auto-summary by GPT-4**\n\n{summary}"}
)
