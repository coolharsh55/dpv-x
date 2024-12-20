#!/usr/bin/env python3
#AI_GENERATED=true
# author: Harshvardhan J. Pandit
# This code was generated using GPT 4o-mini with the following prompt
# Write a separate python script called export_html.py that does the 
# same as above but instead of taking a issue number or -l as parameter, 
# it reads the file and produces a HTML5 document with a table where 
# each row contains issue number, issue title, and copy button, 
# where the copy button on clicking copies the following string 
# to the clipboard "20:10:04 <ghurlbot> [URL] -> Issue [NO] [TITLE] (by [AUTHOR]". 
# Only show the output python.

import json
import os

# Function to read JSON file and generate HTML content
def generate_html(file_name):
    with open(file_name, 'r') as f:
        issues = json.load(f)
        
        # Start the HTML document
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>GitHub Issues</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    padding: 8px 12px;
                    text-align: left;
                    border: 1px solid #ddd;
                }
                th {
                    background-color: #f4f4f4;
                }
                .copy-btn {
                    background-color: #4CAF50;
                    color: white;
                    padding: 6px 10px;
                    border: none;
                    cursor: pointer;
                }
                .copy-btn:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <h1>GitHub Issues</h1>
            <table>
                <thead>
                    <tr>
                        <th>Issue Number</th>
                        <th>Title</th>
                        <th>Copy</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        # Add each issue to the table
        for issue in issues:
            issue_number = issue['number']
            issue_title = issue['title']
            issue_author = issue['author']['login']
            issue_url = f"https://github.com/w3c/dpv/issues/{issue_number}"
            copy_string = f"20:10:04 <ghurlbot> {issue_url} -> Issue {issue_number} {issue_title} (by {issue_author})"
            
            html_content += f"""
            <tr>
                <td>{issue_number}</td>
                <td>{issue_title}</td>
                <td><button class="copy-btn" onclick="copyToClipboard('{copy_string}')">Copy</button></td>
            </tr>
            """
        
        # End the HTML document
        html_content += """
                </tbody>
            </table>

            <script>
                function copyToClipboard(text) {
                    var textarea = document.createElement('textarea');
                    textarea.value = text;
                    document.body.appendChild(textarea);
                    textarea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textarea);
                    alert('Copied to clipboard!');
                }
            </script>
        </body>
        </html>
        """
        
        return html_content

# Main function to generate and save the HTML file
def main():
    # JSON file containing the issues
    file_name = 'issues.json'
    
    # Generate HTML content
    html_content = generate_html(file_name)
    
    # Save the HTML content to a file
    output_file = 'issues.html'
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"HTML file generated: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    main()
