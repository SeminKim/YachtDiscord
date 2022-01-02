import requests

# Some useful configuration options are here.

### IMPORTANT PARAMETERS ###
# Bot token.
BOT_TOKEN = open('data/token.txt', 'r').readline().strip()
# Point API url.
NG_SERVER_URL = open('data/server.txt', 'r').readline().strip()
# Whitelisted channel IDs.
CHANNEL_WHITELIST = [686599527200981040, 739495597916028939]

### Options ###
# If False, bet with points will not work.
USE_NG_API = True
# If False, logs will not be generated.
ENABLE_LOGGING = True
# Send message to whitelisted channels when bot starts.
ALERT_AT_START = False

### Checks ###
# If API is not available, USE_NG_API will be always set to False.
if USE_NG_API:
    if requests.get(f'{NG_SERVER_URL}?id=0&guild=0').status_code != 200:
        USE_NG_API = False
