from dotenv import load_dotenv
import os
import logging
from pathlib import Path

load_dotenv()

def resolveToken():
    token = os.getenv("GITHUB_TOKEN")
    if token:
        return token
    
    configFile = Path.home() / ".gitinsight"
    if configFile.exists():
        with open(configFile, "r") as f:
            token = f.read().strip()
            if token:
                return token
    
    print("Welcome to GitInsight! Setup Required.")
    userToken = input("Please enter your GitHub Personal Access Token: ").strip()

    if not userToken:
        print("GitHub Personal Access Token cannot be empty.")
        exit(1)
    
    try:
        with open(configFile, "w") as f:
            f.write(userToken)
        if os.name != 'nt':
            os.chmod(configFile, 0o600)  # Set file permissions to be readable and writable only by the owner
            print(f"Token saved to {configFile} with restricted permissions.")
    except Exception as e:
        print(f"Error saving token to {configFile}: {e}")

    return userToken


class config:

    GITHUB_TOKEN = resolveToken()
    BASE_URL = "https://api.github.com/users"
    PER_PAGE = 100

def setupLogging(verbose = False):
    if verbose:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
        )