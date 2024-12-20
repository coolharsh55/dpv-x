#!/usr/bin/env python3
#AI_GENERATED=true
# author: Harshvardhan J. Pandit
# This code was generated using GPT 4o-mini with the following prompt
# Write a python script which reads a JSON file containing github issue metadata, 
# takes a parameter -n for the issue number, and returns the following statement 
# "20:10:04 <ghurlbot> https://github.com/w3c/dpv/issues/[NO] -> Issue [NO] [TITLE] (by [AUTHOR])" 
# where [NO] is replaced by issue number, [TITLE] by issue title, 
# and [AUTHOR] by issue author. Only provide the output python. 
# (Added in second prompt: 
# Add a parameter called -l that prints a list of issues in the format [NO] [TITLE] )
# Example JSON: [
#   {
#     "author": {
#       "id": "MDQ6VXNlcjYzNzc5MDY=",
#       "is_bot": false,
#       "login": "coolharsh55",
#       "name": "Harshvardhan Pandit"
#     },
#     "id": "I_kwDOFjF_V86jdvZV",
#     "labels": [
#       {
#         "id": "LA_kwDOFjF_V88AAAABrE4Dcg",
#         "name": "WIP",
#         "description": "",
#         "color": "0B0524"
#       },
#       {
#         "id": "LA_kwDOFjF_V88AAAAB1lZeyg",
#         "name": "sector",
#         "description": "",
#         "color": "D5B5C0"
#       }
#     ],
#     "milestone": {
#       "number": 5,
#       "title": "dpv v2.1",
#       "description": "",
#       "dueOn": "2024-12-17T00:00:00Z"
#     },
#     "number": 204,
#     "title": "Create Sector Extension"
#   } ]

import json
import argparse

# Function to read JSON file and retrieve issue metadata
def get_issue_details(file_name, issue_number):
    with open(file_name, 'r') as f:
        issues = json.load(f)
        for issue in issues:
            if issue['number'] == issue_number:
                return issue
    return None


# Function to list all issues in the format [NO] [TITLE]
def list_issues(file_name):
    with open(file_name, 'r') as f:
        issues = json.load(f)
        for issue in issues:
            print(f"{issue['number']} {issue['title']}")


# Main function
def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Fetch issue metadata from a JSON file.")
    parser.add_argument("-n", "--number", type=int, help="Issue number to retrieve")
    parser.add_argument("-l", "--list", action="store_true", help="List all issues")
    args = parser.parse_args()

    # JSON file containing the issues
    file_name = 'issues.json'

    # If -l flag is provided, list all issues
    if args.list:
        list_issues(file_name)
        return

    # If -n flag is provided, get the issue details
    if args.number:
        # Get the issue details from the JSON file
        issue = get_issue_details(file_name, args.number)

        if issue:
            # Format and print the output statement
            print(f"20:10:04 <ghurlbot> https://github.com/w3c/dpv/issues/{issue['number']} -> Issue {issue['number']} {issue['title']} (by {issue['author']['login']})")
        else:
            print(f"Issue {args.number} not found in the JSON file.")

if __name__ == "__main__":
    main()
