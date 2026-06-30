from rich.panel import Panel
from rich.console import Console
from rich.table import Table
from datetime import datetime

con = Console()

def display_user(data):
    name = data.get('name', 'N/A')
    login = data.get('login', 'N/A')
    public_repos = data.get('public_repos', 'N/A')
    followers = data.get('followers', 'N/A')
    following = data.get('following', 'N/A')
    location = data.get('location', 'N/A')
    created_at = data.get('created_at', 'N/A')

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

def display_repos(repoList):
    if not repoList:
        print("User does not have any repository.")
        return
    
    repoList = [repo for repo in repoList if not repo.get('fork')] 
    #filtering out forked repositories, as they are not original work of the user
    sortedData = sorted(repoList, key = lambda x: x['stargazers_count'], reverse = True)

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

def displayStats(stats):
    con.print(Panel(
        f"Most Used Language        :       {stats["lang"]}\n"
        f"Total Stars               :       {stats["totalstars"]}\n"
        f"Most Starred Repository   :       {stats["moststarred"]["name"]} ({stats["moststarred"]["stars"]} stars)",
        title = "Statistics",
        expand = False
    ))
    print()

    table = Table(title = "Language Breakdown")
    table.add_column("Language", justify = "left", header_style = "bold")
    table.add_column("Number of Repositories", justify = "center", header_style = "bold")
    
    for key, value in stats["langwise"].items():
        table.add_row(f"{key}", f"{value}")

    con.print(table)
    
    print()

def displayActivity(activity):
    table = Table(title = "Event Frequency")
    table.add_column("Event Type", justify = "left", header_style = "bold")
    table.add_column("Frequency", justify = "center", header_style = "bold")
    
    for key, value in activity[0].items():
        table.add_row(f"{key}", f"{value}")
    
    con.print(table)
    print()

    con.print(Panel(
        f"Most Active Day of the week   :   {activity[1]}\n"
        f"Most Active Repository        :   {activity[2]}",
        title = "Activity",
        expand = False
    ))
    print()