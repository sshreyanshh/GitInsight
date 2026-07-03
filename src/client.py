import requests
from rich.console import Console
from config import config

con = Console()

class GitHubClient:

    def __init__(self, token, username):
        self.token = token 
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }               
        self.baseURL = config.BASE_URL
        self.username = username
    
    def fetchUser(self):
        url = self.baseURL + f"/{self.username}"
        response = self._makeRequest(url = url)

        if response is None:
            return None
        
        return response.json()
    
    def fetchRepos(self):
        repos = []
        page = 1

        while True:
            params = {
                "per_page": config.PER_PAGE,
                "page": page
            }

            response = self._makeRequest(url = self.baseURL + f"/{self.username}/repos", params = params)
            
            if response is None:
                return None
            
            repoList = response.json()

            if not repoList:
                break

            repos.extend(repoList)
            page += 1
        
        return repos
    
    def fetchEvents(self):
        events = []
        page = 1

        while True:
            params = {
                "per_page": config.PER_PAGE,
                "page": page
            }

            response = self._makeRequest(url = self.baseURL + f"/{self.username}/events", params = params)
            
            if response is None:
                return None
            
            eventList = response.json()

            if not eventList:
                break

            events.extend(eventList)
            page += 1
        
        return events
    
    def _makeRequest(self, url, params = None):
        try:
            response = requests.get(url, params = params, headers = self.headers)
        except requests.exceptions.ConnectionError:
            print("No Internet Connection. Connect to internet and retry")
            return None
        
        if response.status_code == 404:
            print(f"User '{self.username}' not found.")
            print("Check Username and try again.")
            print()
            con.print("[bold red]EXITING PROGRAM[/bold red]")
            exit()

        if response.status_code != 200:
            print(f"Error Occurred. Status Code: {response.status_code}")
            return None
        
        return response