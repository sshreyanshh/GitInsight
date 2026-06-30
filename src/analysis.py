from collections import Counter
from datetime import datetime

def mostUsedLanguage(repos):
    repos = [repo for repo in repos if not repo.get('fork')]
    #filtering out forked repositories, as they are not original work of the user
    langCount = []
    for repo in repos:
        lang = repo.get('language') or "N/A"
        langCount.append(lang)
    
    highestFreq = Counter(langCount).most_common(1)[0][0]
    #most_common(1) returns highest frequency language as a list containing tuple
    #example: [("python", 3)] -> hence [0][0] is necessary to get lang name

    return highestFreq

def mostStarredRepo(repos):
    if not repos:
        return None
    
    repos = [repo for repo in repos if not repo.get('fork')]
    sortedData = sorted(repos, key = lambda x: x['stargazers_count'], reverse = True)

    return sortedData[0]

def getTotalStars(repos):
    repos = [repo for repo in repos if not repo.get('fork')]
    total = 0
    for repo in repos:
        stars = repo.get('stargazers_count')
        if stars:
            total = total + stars
    
    return total

def languageWiseData(repos):
    repos = [repo for repo in repos if not repo.get('fork')]
    data = {}
    for repo in repos:
        if (repo.get('language') or "N/A") in data:
            data[repo.get('language') or "N/A"] += 1
        else:
            data[repo.get('language') or "N/A"] = 1
    
    sortedData = dict(sorted(data.items(), key = lambda item: item[1], reverse = True))
    return sortedData

def countEventType(events):
    data = {}
    for event in events:
        eventType = event.get('type', 'N/A')
        if eventType in data:
            data[eventType] += 1
        else:
            data[eventType] = 1
    
    sortedData = dict(sorted(data.items(), key = lambda x: x[1], reverse = True))
    return sortedData

def mostActiveDay(events):
    days = []
    for event in events:
        dateObj = datetime.strptime(event.get('created_at'), "%Y-%m-%dT%H:%M:%SZ")
        day = dateObj.strftime("%A")
        days.append(day)
    
    mostActive = Counter(days).most_common(1)[0][0]
    return mostActive

def mostActiveRepo(events):
    repos = []
    for event in events:
        currRepo = event.get('repo').get('name')
        if currRepo:
            repos.append(currRepo)
    
    mostActive = Counter(repos).most_common(1)[0][0]
    return mostActive