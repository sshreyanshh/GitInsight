from client import fetch_user, fetch_repos, fetchEvents
from display import (
    display_user, 
    display_repos, 
    displayStats,
    displayActivity
)
from analysis import (
    mostUsedLanguage,
    mostStarredRepo,
    getTotalStars,
    languageWiseData,
    countEventType,
    mostActiveDay,
    mostActiveRepo
)
from rich.console import Console
from report import GitInsightReport

con = Console()

username = input("Enter GitHub Username:    ")

with con.status("[bold green]Fetching User Data....", spinner = "dots"):
    data = fetch_user(username)
if data:
    display_user(data)

with con.status("[bold green]Fetching Repository Data....", spinner = "dots"):
    repodata = fetch_repos(username)
if repodata: #to play safe if fetch_repos returns None, due to any error like network error
    display_repos(repodata)

if repodata:
    lang = mostUsedLanguage(repodata)
    totalstars = getTotalStars(repodata)
    starred = mostStarredRepo(repodata)
    langwise = languageWiseData(repodata)

    userstats = {
        "lang": lang,
        "totalstars": totalstars,
        "moststarred" : {
            "name": starred.get('name'),
            "stars": starred.get('stargazers_count')
        },
        "langwise" : langwise
    }

    displayStats(userstats)

with con.status("[bold green]Fetching Events Data....", spinner = "dots"):
    eventData = fetchEvents(username)
if eventData:
    activity = [countEventType(eventData), mostActiveDay(eventData), mostActiveRepo(eventData)]
    displayActivity(activity)

print()
choice = str(input("Do you want to generate PDF report? (y/n):    "))
if choice.lower() == 'y':
    report = GitInsightReport(username)
    if data:
        report.addProfileSec(data)
    if userstats:
        report.addStats(userstats)
    if repodata and userstats:
        report.addRepo(repodata, userstats)
    if activity:
        report.addActivity(activity)

    filename = report.save()
    con.print(f"[bold green]Report Generated Successfully![/bold green] [bold blue]Saved to {filename}[/bold blue]")