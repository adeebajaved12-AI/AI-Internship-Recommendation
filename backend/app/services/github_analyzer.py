import requests

def analyze_github_repos(username: str) -> dict:
    url = f"https://api.github.com/users/{username}/repos"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return {"repos_count": 0, "languages": [], "status": "User not found or rate limited"}
        
        repos = response.json()
        languages = set()
        repo_names = []
        
        for repo in repos:
            repo_names.append(repo.get("name"))
            lang = repo.get("language")
            if lang:
                languages.add(lang.lower())
                
        return {
            "repos_count": len(repos),
            "languages": list(languages),
            "top_repos": repo_names[:5],
            "status": "Success"
        }
    except Exception as e:
        return {"repos_count": 0, "languages": [], "status": f"Error: {str(e)}"}