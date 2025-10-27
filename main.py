import requests
from collections import Counter, defaultdict

GITHUB_API_URL = "https://api.github.com/users/{username}/events/public"
GITHUB_API_USER_URL = "https://api.github.com/users/{username}/repos"

def get_user_events(username):
    url = GITHUB_API_URL.format(username=username)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_user_repos(username):
    url = GITHUB_API_USER_URL.format(username=username)
    response = requests.get(url)
    response.raise_for_status()
    return set(repo['full_name'] for repo in response.json())

def activity(username):
    events = get_user_events(username)
    owned_repos = get_user_repos(username)
    repo_events = defaultdict(list)

    # Aggregate event types by repo
    for event in events:
        repo_name = event['repo']['name']
        repo_events[repo_name].append(event['type'])

    results = []
    for repo, event_types in repo_events.items():
        most_common = Counter(event_types).most_common(3)
        result = {
            'repo': repo,
            'owned_by_user': repo in owned_repos,
            'top_3_event_types': most_common
        }
        results.append(result)

    return results

if __name__ == '__main__':
    username = "cheshire137"  # replace with any GitHub username
    activity_results = activity(username)
    for item in activity_results:
        print(f"Repo for ref: {item['repo']}")
        print(f"Owned by user flag: {item['owned_by_user']}")
        print(f"Three Most Common Event Types: {item['top_3_event_types']}\n")
