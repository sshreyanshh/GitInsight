import logging
import os
from gitinsight.client import GitHubClient
from gitinsight.display import Display
from gitinsight.analysis import Analysis
from rich.console import Console
from gitinsight.report import GitInsightReport
from gitinsight.config import config, resolveToken
import argparse
from gitinsight.config import setupLogging
import asyncio
from gitinsight._async import AsyncGitHubClient, UserNotFoundError, APIError, NoInternetConnectionError

con = Console()

def main():
    parser = argparse.ArgumentParser(description = "GitInsight - A CLI tool to analyze GitHub user data and generate reports.")
    parser.add_argument("username", nargs = "?", help = "GitHub username to analyze")
    parser.add_argument("-r", "--report", action = "store_true", help = "Generate PDF report")
    parser.add_argument("-v", "--verbose", action = "store_true", help = "Enable verbose output")
    parser.add_argument("--token", help = "GitHub PAT to increase limits")
    parser.add_argument("--clear-token", action = "store_true", help = "Remove the saved GitHub PAT")

    args = parser.parse_args()

    setupLogging(args.verbose)

    if args.token and args.clear_token:
        parser.error("--token and --clear-token cannot be used together")

    if args.clear_token:
        resolveToken("")
        config.GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
        if not args.username:
            return

    if args.token:
        config.GITHUB_TOKEN = resolveToken(args.token)

    _token = config.GITHUB_TOKEN

    if not args.username:
        if args.token or args.clear_token:
            return
        parser.error("username is required")
    if not _token:
        logging.info("No token found. Proceeding with unauthenticated GitHub API requests.\nAdd a GitHub PAT to increase limits.")
        con.print("[bold yellow]No token found. \nProceeding with unauthenticated GitHub API requests. \nAdd a GitHub PAT to increase limits. Use --token to set one.[/bold yellow]")

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