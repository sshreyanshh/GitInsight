from collections import Counter
from datetime import datetime

class Analysis:

    def __init__(self, repos, events):
        repos = repos or []
        events = events or []
        self.repos = [repo for repo in repos if not repo.get('fork')]
        self.events = events
        
    def mostUsedLanguage(self):
        langCount = []
        for repo in self.repos:
            lang = repo.get('language') or "N/A"
            langCount.append(lang)
        
        highestFreq = Counter(langCount).most_common(1)[0][0]
        #most_common(1) returns highest frequency language as a list containing tuple
        #example: [("python", 3)] -> hence [0][0] is necessary to get lang name

        return highestFreq
    
    def getTotalStars(self):
        total = 0
        for repo in self.repos:
            stars = repo.get('stargazers_count')
            if stars:
                total = total + stars
        
        return total
    
    def mostStarredRepo(self):
        sortedData = sorted(self.repos, key = lambda x: x['stargazers_count'], reverse = True)

        return sortedData[0]
    
    def langWiseData(self):
        data = {}
        for repo in self.repos:
            if (repo.get('language') or "N/A") in data:
                data[repo.get('language') or "N/A"] += 1
            else:
                data[repo.get('language') or "N/A"] = 1
        
        sortedData = dict(sorted(data.items(), key = lambda item: item[1], reverse = True))
        return sortedData
    
    def countEventType(self):
        data = {}
        for event in self.events:
            eventType = event.get('type', 'N/A')
            if eventType in data:
                data[eventType] += 1
            else:
                data[eventType] = 1
        
        sortedData = dict(sorted(data.items(), key = lambda x: x[1], reverse = True))
        return sortedData
    
    def mostActiveDay(self):
        days = []
        for event in self.events:
            dateObj = datetime.strptime(event.get('created_at'), "%Y-%m-%dT%H:%M:%SZ")
            day = dateObj.strftime("%A")
            days.append(day)
        
        mostActive = Counter(days).most_common(1)[0][0]
        return mostActive
    
    def mostActiveRepo(self):
        repos = []
        for event in self.events:
            currRepo = event.get('repo').get('name')
            if currRepo:
                repos.append(currRepo)
        
        mostActive = Counter(repos).most_common(1)[0][0]
        return mostActive