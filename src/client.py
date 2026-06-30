import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_user(username):
    token = os.getenv("GITHUB_TOKEN")

    url = f"https://api.github.com/users/{username}"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.get(url, headers = headers)
    except requests.exceptions.ConnectionError:
        print("No Internet Connection. Kindly Connect to internet and retry.")
        return None
    
    if response.status_code == 404:
        print(f"User {username} does not exist.")
        return None

    if response.status_code != 200:
        print(f"Something went wrong. Status: {response.status_code}")
        return None
    
    return response.json()


def fetch_repos(username):
    token = os.getenv("GITHUB_TOKEN")

    url = f"https://api.github.com/users/{username}/repos"

    repos = []
    page = 1
    while True:
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

        params = {
            "per_page": 100,
            "page": page
        }

        try:
            response = requests.get(url, headers = headers, params = params)
        except requests.exceptions.ConnectionError:
            print("No Internet Connection. Kindly connect to internet and retry.")
            return None
        
        if response.status_code != 200:
            print(f"Error Occurred while fetching repositories. Status: {response.status_code}")
            return None
        
        repo_per_page = response.json()

        if not repo_per_page:
            break
        else:
            repos.extend(repo_per_page) #repos is a list of dictionaries
            page = page + 1

    return repos

def fetchEvents(username):
    token = os.getenv("GITHUB_TOKEN")

    url = f"https://api.github.com/users/{username}/events"

    events = []
    page = 1
    while True:
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

        params = {
            "per_page": 100,
            "page": page
        }

        try:
            response = requests.get(url, params = params, headers = headers)
        except requests.exceptions.ConnectionError:
            print("No Internet Connection. Please connect to internet and try again.")
            return None
        
        if response.status_code != 200:
            print(f"Error Occurred. Status Code: {response.status_code}")
            return None
        
        currEventList = response.json()
        
        if not currEventList:
            break

        events.extend(currEventList)
        page += 1
    
    return events