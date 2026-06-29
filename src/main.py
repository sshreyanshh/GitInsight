from client import fetch_user, fetch_repos
from display import display_user, display_repos, displayStats
from analysis import (
    mostUsedLanguage,
    mostStarredRepo,
    getTotalStars,
    languageWiseData
)

username = input("Enter GitHub Username:    ")

data = fetch_user(username)
if data:
    display_user(data)

repodata = fetch_repos(username)
if repodata: #to play safe if fetch_repos returns None, due to any error
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