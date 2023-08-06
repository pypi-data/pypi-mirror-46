# IMPORTS
from pathlib import Path
#################################################################################
# CONSTANTS
path = Path("apikeys.txt")
keys = "apikeys.txt"

if not path.exists():  # Checks if the txt file the stores the API Keys exists
    open("apikeys.txt", "w+").close()


def key_validator():
    global currentAPIKey
    newlst = open(keys).readline().split(", ")
    for keyss in newlst:
        currentAPIKey = [i for i in newlst if get('https://api.hypixel.net/key?key=%s' % keyss).json()["success"] is True]
    if len(currentAPIKey) == 0:
        return "Invalid"
    curr = ""
    for i in range(len(currentAPIKey) - 2):
        curr += currentAPIKey[i] + ", "
    curr += currentAPIKey[-1]
    open(keys, "a").write(curr)


def addkeys(apikeys):  # Add api keys
    apikeys = apikeys.split(", ")
    for apikeyy in range(len(apikeys) - 1):
        if not apikeys[apikeyy] in open(keys).readline():
            # Checks if the API key was already added if it wasn't it continues.
            r = get('https://api.hypixel.net/key?key=%s' % apikeys[apikeyy]).json()["success"]
            if r is True:
                open(keys, "a").write(apikeys[apikeyy] + ", ")  # Adds the api key to the txt file
    if not apikeys[-1] in open(keys).readline():
        if get('https://api.hypixel.net/key?key=%s' % apikeys[-1]).json()["success"]:
            open(keys, "a").write(apikeys[-1])
    if not ", ".join(apikeys) in open(keys).readline():
        key_validator()


def stat_grab(specify, variable):
    for take in variable:
        if specify in take and ":" in specify:
            return "".join(take.split(specify + " "))
        elif specify in take:
            return "".join(take.split(specify + ": "))
