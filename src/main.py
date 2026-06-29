from client import fetch_user
from display import display_user

username = input("Enter GitHub Username:    ")

data = fetch_user(username)

if data:
    display_user(data)