#!/usr/bin/env python3

import os
import json
import re

# Function to extract issues from the .irc file based on the given date
def extract_issues_from_irc(date):
    file_path = os.path.expanduser(f"~/code/dpvcg/dpv/code/minutes-generator/data/meeting-{date}.irc")
    issues = []

    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                # Look for the pattern "github.com/w3c/dpv/issues/<issue>"
                match = re.search(r"github\.com/w3c/dpv/issues/(\d+)", line)
                if match:
                    issues.append(match.group(1))  # Extract the issue number
    else:
        print(f"File {file_path} does not exist.")
    
    return issues

# Function to load issue data from the issues.json file
def load_issue_data():
    issue_file_path = "issues.json"
    if os.path.exists(issue_file_path):
        with open(issue_file_path, 'r') as file:
            return json.load(file)
    else:
        print("issues.json file does not exist.")
        return []

# Main function to process the issues
def main():
    # Ask for the date
    date = input("Enter the date (YYYY-MM-DD): ")
    
    # Extract issues from the .irc file
    issues_to_check = extract_issues_from_irc(date)
    
    # Load issue data from the issues.json file
    issue_data = load_issue_data()

    # Prepare a list to hold selected issues
    selected_issues = []

    # Check if the issues extracted from the .irc file are in the issues.json file
    for issue_number in issues_to_check:
        # Find the issue in the loaded data
        matched_issue = next((issue for issue in issue_data if str(issue['number']) == issue_number), None)
        
        if matched_issue:
            # Display the issue number and title
            print(f"Issue {matched_issue['number']}: {matched_issue['title']}")
            
            # Ask the user if it should post a comment on the issue
            response = input("Do you want to post a comment on this issue? (Y/N): ").strip().upper()

            if response == 'Y':
                selected_issues.append((matched_issue['number'], matched_issue['title']))

    # Print the list of selected issues
    if selected_issues:
        print("\nSelected Issues for Commenting:")
        for issue in selected_issues:
            print(f"Issue {issue[0]}: {issue[1]}")
    else:
        print("No issues selected for commenting.")

if __name__ == "__main__":
    main()
