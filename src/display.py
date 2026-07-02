from rich.panel import Panel
from rich.console import Console
from rich.table import Table
from datetime import datetime

con = Console()

class Display:

    def __init__(self, data, repoList, stats, activity):
        self.data = data
        self.repoList = repoList
        self.stats = stats
        self.activity = activity

    def displayUser(self):
        name = self.data.get('name', 'N/A')
        login = self.data.get('login', 'N/A')
        public_repos = self.data.get('public_repos', 'N/A')
        followers = self.data.get('followers', 'N/A')
        following = self.data.get('following', 'N/A')
        location = self.data.get('location', 'N/A')
        created_at = self.data.get('created_at', 'N/A')

        formatted = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%d %B %Y")

        con.print(Panel(
            f"Name:                     {name}\n"
            f"Username:                 {login}\n"
            f"Public Repositories:      {public_repos}\n"
            f"Followers:                {followers}\n"
            f"Following:                {following}\n"
            f"Location:                 {location}\n"
            f"Account Created on:       {formatted}",
            title = "Profile",
            expand = False
        ))

        print()

    def displayRepos(self):
        if not self.repoList:
            con.print("[bold red]User does not have any repository.[/bold red]")
            return
        
        repoList = [repo for repo in self.repoList if not repo.get('fork')] 
        #filtering out forked repositories, as they are not original work of the user
        sortedData = sorted(self.repoList, key = lambda x: x['stargazers_count'], reverse = True)

        table = Table(title = "Repositories")
        table.add_column("Name", justify = "left", header_style = "bold")
        table.add_column("Language", justify = "left", header_style = "bold")
        table.add_column("Stars", justify = "center", header_style = "bold")
        table.add_column("Forks", justify = "center", header_style = "bold")

        for repo in sortedData:
            name = repo.get('name')
            lang = repo.get('language') or "N/A" #when first arg is None (false), or evaluates second argument
            stars = str(repo.get('stargazers_count'))
            fork = str(repo.get('forks'))

            table.add_row(name, lang, stars, fork)
        
        con.print(table)

        print()

    def displayStats(self):
        if not self.stats:
            con.print("[bold red]Stats cannot be displayed. No repository found.[/bold red]")
            return
        
        con.print(Panel(
            f"Most Used Language        :       {self.stats["lang"]}\n"
            f"Total Stars               :       {self.stats["totalstars"]}\n"
            f"Most Starred Repository   :       {self.stats["moststarred"]["name"]} ({self.stats["moststarred"]["stars"]} stars)",
            title = "Statistics",
            expand = False
        ))
        print()

        table = Table(title = "Language Breakdown")
        table.add_column("Language", justify = "left", header_style = "bold")
        table.add_column("Number of Repositories", justify = "center", header_style = "bold")
        
        for key, value in self.stats["langwise"].items():
            table.add_row(f"{key}", f"{value}")

        con.print(table)
        
        print()

    def displayActivity(self):
        if not self.activity:
            con.print("[bold red]User does not have any activity.[/bold red]")
            return
        
        table = Table(title = "Event Frequency")
        table.add_column("Event Type", justify = "left", header_style = "bold")
        table.add_column("Frequency", justify = "center", header_style = "bold")
        
        for key, value in self.activity[0].items():
            table.add_row(f"{key}", f"{value}")
        
        con.print(table)
        print()

        con.print(Panel(
            f"Most Active Day of the week   :   {self.activity[1]}\n"
            f"Most Active Repository        :   {self.activity[2]}",
            title = "Activity",
            expand = False
        ))
        print()