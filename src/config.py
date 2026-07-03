from dotenv import load_dotenv
import os

load_dotenv()

class config:

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    BASE_URL = "https://api.github.com/users"
    PER_PAGE = 100