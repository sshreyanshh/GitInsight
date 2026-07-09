import aiohttp
import asyncio
import logging
from gitinsight.config import config
from rich.console import Console

con = Console()

class UserNotFoundError(Exception):
    pass

class APIError(Exception):
    pass

class NoInternetConnectionError(Exception):
    pass

class AsyncGitHubClient:

    def __init__(self, token, username):
        self.token = token 
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
        self.url = config.BASE_URL + f"/{username}"
        self.username = username

    async def _makeRequest(self, session, url, params = None):
        try:
            async with session.get(url, headers = self.headers, params = params) as response:
                if response.status in (403, 429):
                    if response.headers.get("X-RateLimit-Remaining") == "0":
                        logging.error("GitHub API rate limit reached for unauthenticated requests.")
                        logging.info("Add a GitHub Personal Access Token. read README.md/Getting Your Token")
                        return None

                if response.status == 404:
                    raise UserNotFoundError(f"User '{self.username}' not found.")

                if response.status != 200:
                    raise APIError(f"API Error. Status Code: {response.status}")

                return await response.json()
        
        except aiohttp.ClientConnectionError:
            raise NoInternetConnectionError("No Internet Connection. Connect to internet and retry")
        
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