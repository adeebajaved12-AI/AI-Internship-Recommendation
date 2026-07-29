import os
import sqlite3
import requests

def init_db():
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mentors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            expertise TEXT NOT NULL,
            contact TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_mentor(name, expertise, contact):
    init_db()
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO mentors (name, expertise, contact) VALUES (?, ?, ?)', (name, expertise, contact))
    conn.commit()
    conn.close()

def get_dynamic_mentors():
    init_db()
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, expertise, contact FROM mentors')
    mentors = cursor.fetchall()
    conn.close()
    return mentors

# 2. Updated GitHub Validation with Optional API Token Support
def validate_github_profile_and_repo(profile_url, github_token=None):
    if not profile_url:
        return {"valid": False, "error": "GitHub URL cannot be empty."}

    profile_url = profile_url.strip().rstrip("/")
    parts = profile_url.split("/")

    if "github.com" not in parts:
        return {"valid": False, "error": "Invalid GitHub domain format."}

    headers = {}
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    try:
        if len(parts) == 4:  # Format: github.com/username
            username = parts[-1]
            api_url = f"https://api.github.com/users/{username}"
            res = requests.get(api_url, headers=headers, timeout=5)

            if res.status_code == 200:
                data = res.json()
                return {
                    "valid": True,
                    "type": "user",
                    "name": data.get("login"),
                    "public_repos": data.get("public_repos", 0),
                    "followers": data.get("followers", 0),
                }
            elif res.status_code == 403:
                return {
                    "valid": False,
                    "error": "GitHub API rate limit exceeded. Please configure a token.",
                }
            else:
                return {
                    "valid": False,
                    "error": "GitHub user profile does not exist or is invalid.",
                }

        elif len(parts) >= 5:  # Format: github.com/owner/repo
            owner = parts[-2]
            repo = parts[-1]
            api_url = f"https://api.github.com/repos/{owner}/{repo}"
            res = requests.get(api_url, headers=headers, timeout=5)

            if res.status_code == 200:
                data = res.json()
                return {
                    "valid": True,
                    "type": "repo",
                    "language": data.get("language", "Not Specified"),
                    "stars": data.get("stargazers_count", 0),
                    "forks": data.get("forks_count", 0),
                }
            elif res.status_code == 403:
                return {
                    "valid": False,
                    "error": "GitHub API rate limit exceeded. Please configure a token.",
                }
            else:
                return {
                    "valid": False,
                    "error": "GitHub repository does not exist, is private, or URL is incorrect.",
                }
    except Exception as e:
        return {
            "valid": False,
            "error": f"Connection error while verifying GitHub: {str(e)}",
        }

    return {"valid": False, "error": "Unrecognized GitHub URL structure."}