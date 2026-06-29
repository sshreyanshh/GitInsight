from client import fetch_user, fetch_repos
from display import display_user, display_repos

username = input("Enter GitHub Username:    ")

data = fetch_user(username)
if data:
    display_user(data)

repodata = fetch_repos(username)
if repodata: #to play safe if fetch_repos returns None, due to any error
    display_repos(repodata)