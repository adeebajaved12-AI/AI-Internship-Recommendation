import requests

def analyze_github_profile(username: str):
    """
    Fetches public repositories for a given GitHub username, 
    extracts programming languages, total stars, and computes an activity score.
    """
    if not username:
        return {"error": "Username not provided", "score": 0, "projects_count": 0, "languages": []}
        
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return {
                "error": "GitHub user not found or rate limited", 
                "repositories_analyzed": 0,
                "languages_found": [],
                "total_stars": 0,
                "github_activity_score": 0
            }
        
        repos = response.json()
        languages = set()
        total_stars = 0
        
        for repo in repos:
            if repo.get("language"):
                languages.add(repo["language"])
            total_stars += repo.get("stargazers_count", 0)
            
        # Activity score calculation logic based on repos and stars
        score = min(100, (len(repos) * 6) + (total_stars * 3))
        
        return {
            "repositories_analyzed": len(repos),
            "languages_found": list(languages),
            "total_stars": total_stars,
            "github_activity_score": score
        }
    except Exception as e:
        return {"error": str(e), "github_activity_score": 0}

def evaluate_portfolio(portfolio_data: dict):
    """
    Evaluates external portfolio links, projects, and certifications.
    """
    projects_count = len(portfolio_data.get("projects", []))
    certs_count = len(portfolio_data.get("certifications", []))
    
    score = min(100, (projects_count * 15) + (certs_count * 10))
    
    return {
        "portfolio_score": score,
        "verified_projects": projects_count,
        "certifications_count": certs_count,
        "evaluation_status": "Strong Portfolio" if score > 50 else "Moderate Portfolio"
    }