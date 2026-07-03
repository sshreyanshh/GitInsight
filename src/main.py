from client import GitHubClient
from display import Display
from analysis import Analysis
from rich.console import Console
from report import GitInsightReport
from config import config
import argparse

con = Console()

parser = argparse.ArgumentParser(description = "GitInsight - A CLI tool to analyze GitHub user data and generate reports.")
parser.add_argument("username", help = "GitHub username to analyze")
parser.add_argument("-r", "--report", action = "store_true", help = "Generate PDF report")

args = parser.parse_args()

client = GitHubClient(token = config.GITHUB_TOKEN, username = args.username)

with con.status("[bold green]Fetching User Data....", spinner = "dots"):
    data = client.fetchUser()

with con.status("[bold green]Fetching Repository Data....", spinner = "dots"):
    repodata = client.fetchRepos()

with con.status("[bold green]Fetching Events Data....", spinner = "dots"):
    eventData = client.fetchEvents()

analysis = Analysis(repos = repodata, events = eventData)

if repodata:
    lang = analysis.mostUsedLanguage()
    totalstars = analysis.getTotalStars()
    starred = analysis.mostStarredRepo()
    langwise = analysis.langWiseData()

    userstats = {
        "lang": lang,
        "totalstars": totalstars,
        "moststarred" : {
            "name": starred.get('name'),
            "stars": starred.get('stargazers_count')
        },
        "langwise" : langwise
    }
else:
    userstats = {}

if eventData:
    activity = [analysis.countEventType(), analysis.mostActiveDay(), analysis.mostActiveRepo()]
else:
    activity = []

display = Display(data = data, repoList = repodata, stats = userstats, activity = activity)

display.displayUser()
print()
display.displayRepos()
print()
display.displayStats()
print()
display.displayActivity()
print()

if args.report:
    report = GitInsightReport(args.username)
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