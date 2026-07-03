from dotenv import load_dotenv
import os
import logging

load_dotenv()

class config:

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    BASE_URL = "https://api.github.com/users"
    PER_PAGE = 100

def setupLogging(verbose = False):
    if verbose:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
        )
