import os
from openai import OpenAI

openai_api_key = os.getenv("OPENAI_API_KEY")
repo = os.getenv("GITHUB_REPO")
pr_number = os.getenv("PR_NUMBER")
pr_body = os.getenv("PR_BODY")

client = OpenAI(api_key=openai_api_key)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful GitHub assistant that summarizes pull requests."},
        {"role": "user", "content": f"Summarize the following pull request from {repo}, PR #{pr_number}:

{pr_body}"}
    ]
)

print("🤖 PR Summary:
")
print(response.choices[0].message.content)