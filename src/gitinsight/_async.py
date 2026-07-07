import aiohttp
import asyncio
import logging
from gitinsight.config import config
from rich.console import Console

con = Console()

class AsyncGitHubClient:

    def __init__(self, token, username):
        self.token = token 
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }               
        self.url = config.BASE_URL + f"/{username}"

    async def _makeRequest(self, session, url, params = None):
        try:
            async with session.get(url, headers = self.headers, params = params) as response:
                if response.status == 404:
                    logging.error(f"User '{self.username}' not found.")
                    logging.info("Check Username and try again.")
                    con.print("[bold red]EXITING PROGRAM[/bold red]")
                    exit()

                if response.status != 200:
                    logging.error(f"Error Occurred. Status Code: {response.status}")
                    return None
                
                return await response.json()
        
        except aiohttp.ClientConnectionError:
            logging.critical("No Internet Connection. Connect to internet and retry")
            return None
        
    async def fetchUser(self, session):
        url = self.url
        return await self._makeRequest(session, url)
    
    async def fetchRepos(self, session):
        repos = []
        page = 1

        while True:
            params = {
                "per_page": config.PER_PAGE,
                "page": page
            }
            
            url = self.url + "/repos"

            _json = await self._makeRequest(session, url, params = params)

            if _json is None:
                return None
            
            if not _json:
                break

            repos.extend(_json)
            page += 1

        return repos
    
    async def fetchEvents(self, session):
        events = []
        page = 1

        url = self.url + "/events"

        while True:
            params = {
                "per_page" : config.PER_PAGE,
                "page": page
            }

            _json = await self._makeRequest(session, url, params)

            if _json is None:
                return None
            
            if not _json:
                break

            events.extend(_json)
            page += 1

        return events
    
    async def fetchAll(self): #function that calls everything at once
        async with aiohttp.ClientSession() as session:
            user, repos, events = await asyncio.gather(
                self.fetchUser(session),
                self.fetchRepos(session),
                self.fetchEvents(session)
            )
        
        return user, repos, events