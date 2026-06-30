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

eventData = fetchEvents(username)
if eventData:
    activity = [countEventType(eventData), mostActiveDay(eventData), mostActiveRepo(eventData)]
    displayActivity(activity)