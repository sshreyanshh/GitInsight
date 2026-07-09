from dotenv import load_dotenv
import os
import logging
from pathlib import Path

load_dotenv()

def resolveToken(newToken=None):
    configFile = Path.home() / ".gitinsight"

    if newToken is not None:
        newToken = newToken.strip()
        if not newToken:
            if configFile.exists():
                try:
                    configFile.unlink()
                    print(f"Token removed from {configFile}.")
                except Exception as e:
                    print(f"Error removing token from {configFile}: {e}")
            else:
                print(f"No saved token found at {configFile}.")
            return None
        try:
            with open(configFile, "w") as f:
                f.write(newToken)
            if os.name != 'nt':
                os.chmod(configFile, 0o600)  # Set file permissions to be readable and writable only by the owner
            print(f"Token saved to {configFile}.")
        except Exception as e:
            print(f"Error saving token to {configFile}: {e}")
        return newToken

    token = os.getenv("GITHUB_TOKEN")
    if token:
        return token

    if configFile.exists():
        with open(configFile, "r") as f:
            token = f.read().strip()
            if token:
                return token
    
    # print("No GitHub PAT token found. proceeding with unauthenticated requests (lower rate limits). Use --token to set one.")
    return None


class config:

    GITHUB_TOKEN = resolveToken()
    BASE_URL = "https://api.github.com/users"
    PER_PAGE = 100

def setupLogging(verbose=False):
    if verbose:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
        )