import requests
import time


def query(request):
    request["action"] = "query"
    request["format"] = "json"
    lastContinue = {}
    while True:
        # Clone original request
        req = request.copy()
        # Modify with the values returned in the 'continue' section of the last result.
        req.update(lastContinue)
        # Call API
        time.sleep(1)
        result = requests.get("https://yi.wikipedia.org/w/api.php", params=req).json()
        if "error" in result:
            raise Error(result["error"])
        if "warnings" in result:
            print(result["warnings"])
        if "query" in result:
            yield result["query"]
        if "continue" not in result:
            break
        lastContinue = result["continue"]


for result in query(
    {
        "generator": "allpages",
        "gapnamespace": 0,
        "gapfilterredir": "nonredirects",
        "gaplimit": "max",
        "prop": "info",
    }
):
    for page in result["pages"]:
        title = result["pages"][page]["title"]
        size = result["pages"][page]["length"]
        touched = result["pages"][page]["touched"]
        # print(title)
        time.sleep(0.1)
        revision = requests.get(
            "https://yi.wikipedia.org/w/api.php",
            {
                "format": "json",
                "action": "query",
                "titles": title,
                "prop": "revisions",
                "rvlimit": 1,
                "rvprop": "timestamp",
                "rvdir": "newer",
            },
        ).json()
        # print(hebRes)
        for p in revision["query"]["pages"]:
            timestamp = revision["query"]["pages"][p]["revisions"][0]["timestamp"]
            print(title + "|" + str(size) + "|" + timestamp + "|" + touched)
