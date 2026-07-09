import logging
from gitinsight.client import GitHubClient
from gitinsight.display import Display
from gitinsight.analysis import Analysis
from rich.console import Console
from gitinsight.report import GitInsightReport
from gitinsight.config import config, resolveToken
import argparse
from gitinsight.config import setupLogging
import asyncio
from gitinsight._async import AsyncGitHubClient

con = Console()

def main():
    parser = argparse.ArgumentParser(description = "GitInsight - A CLI tool to analyze GitHub user data and generate reports.")
    parser.add_argument("username", help = "GitHub username to analyze")
    parser.add_argument("-r", "--report", action = "store_true", help = "Generate PDF report")
    parser.add_argument("-v", "--verbose", action = "store_true", help = "Enable verbose output")
    parser.add_argument("--token", help = "GitHub PAT to increase limits")

    args = parser.parse_args()

    setupLogging(args.verbose)

    if args.token:
        config.GITHUB_TOKEN = resolveToken(args.token)

    _token = config.GITHUB_TOKEN

    if not args.username:
        if args.token:
            return
        parser.error("username is required")
    if not _token:
        logging.info("No token found. Proceeding with unauthenticated GitHub API requests.\nAdd a GitHub PAT to increase limits.")

    client = AsyncGitHubClient(token = _token, username = args.username)

    with con.status("[bold green]Fetching Data....", spinner = "dots"):
        data, repodata, eventData = asyncio.run(client.fetchAll())

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

if __name__ == "__main__":
    main()