import logging
from gitinsight.client import GitHubClient
from gitinsight.display import Display
from gitinsight.analysis import Analysis
from rich.console import Console
from gitinsight.report import GitInsightReport
from gitinsight.config import config
import argparse
from gitinsight.config import setupLogging
import asyncio
from gitinsight._async import AsyncGitHubClient, UserNotFoundError, APIError, NoInternetConnectionError

con = Console()

def main():
    parser = argparse.ArgumentParser(description = "GitInsight - A CLI tool to analyze GitHub user data and generate reports.")
    parser.add_argument("username", help = "GitHub username to analyze")
    parser.add_argument("-r", "--report", action = "store_true", help = "Generate PDF report")
    parser.add_argument("-v", "--verbose", action = "store_true", help = "Enable verbose output")

    args = parser.parse_args()

    setupLogging(args.verbose)

    _token = config.GITHUB_TOKEN

    if not _token:
        logging.critical("GitHub token not found. Please set the GITHUB_TOKEN environment variable.")
        exit(1)

    client = AsyncGitHubClient(token = _token, username = args.username)

    try:
        with con.status("[bold green]Fetching Data....", spinner = "dots"):
            data, repodata, eventData = asyncio.run(client.fetchAll())
    except NoInternetConnectionError as e:
        logging.critical(str(e))
        con.print("[bold red]EXITING PROGRAM[/bold red]")
        exit(1)
    except UserNotFoundError as e:
        logging.critical(str(e))
        logging.error("Check Username and try again.")
        con.print("[bold red]EXITING PROGRAM[/bold red]")
        exit(1)
    except APIError as e:
        logging.critical(str(e))
        con.print("[bold red]EXITING PROGRAM[/bold red]")
        exit(1)

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