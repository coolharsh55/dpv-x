#!/usr/bin/env python3

import requests
import sys
import os

def comment_on_issue(issue_number, date, comment=None):
    repo = "w3c/dpv"
    # repo = "coolharsh55/dpv-x"
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    meeting_url = f"https://w3id.org/dpv/meetings/meeting-{date}.html"
    comment_text = f"(using [dpvbot](https://github.com/coolharsh55/dpv-x/tree/master/dpvbot):) This was discussed in [Meeting {date}]({meeting_url})"
    if comment:
        comment_text += f" \n{comment}"
    comment_body = { "body": comment_text }
    
    token_path = os.path.expanduser("~/.private/github/dpvbot")
    try:
        with open(token_path, "r") as token_file:
            github_token = token_file.read().strip()
    except FileNotFoundError:
        print(f"Error: Token file not found at {token_path}")
        sys.exit(1)
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.post(url, json=comment_body, headers=headers)
    
    if response.status_code == 201:
        print(f"Successfully commented on issue #{issue_number}")
    else:
        print(f"Failed to comment on issue #{issue_number}: {response.status_code}, {response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <date> <issue_number> [<comment>]")
        sys.exit(1)
    
    date = sys.argv[1]
    issue_number = sys.argv[2]
    comment = " ".join(sys.argv[3:])
    
    comment_on_issue(issue_number, date, comment)