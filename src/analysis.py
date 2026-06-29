from collections import Counter

def mostUsedLanguage(repos):
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
    
    sortedData = sorted(repos, key = lambda x: x['stargazers_count'], reverse = True)

    return sortedData[0]

def getTotalStars(repos):
    total = 0
    for repo in repos:
        stars = repo.get('stargazers_count')
        if stars:
            total = total + stars
    
    return total

def languageWiseData(repos):
    data = {}
    for repo in repos:
        if (repo.get('language') or "N/A") in data:
            data[repo.get('language') or "N/A"] += 1
        else:
            data[repo.get('language') or "N/A"] = 1
    
    sortedData = dict(sorted(data.items(), key = lambda item: item[1], reverse = True))
    return sortedData