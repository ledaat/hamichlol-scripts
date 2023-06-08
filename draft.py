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
        result = requests.get(
            "https://yi.hamichlol.org.il/w/api.php", params=req
        ).json()
        if "error" in result:
            raise Error(result["error"])
        if "warnings" in result:
            print(result["warnings"])
        if "query" in result:
            yield result["query"]
        if "continue" not in result:
            break
        lastContinue = result["continue"]


with open("drafts.csv", "w", encoding="utf-8") as f:
    f.write("נאמען|גרויס|דורך|געשאפן|לעצט געטוישט\n")
    for result in query(
        {"generator": "categorymembers", "gcmtitle": "קאטעגאריע:דרעפטס", "prop": "info"}
    ):
        for page in result["pages"]:
            title = result["pages"][page]["title"]
            size = result["pages"][page]["length"]
            touched = result["pages"][page]["touched"]
            # print(title)
            time.sleep(0.1)
            revision = requests.get(
                "https://yi.hamichlol.org.il/w/api.php",
                {
                    "format": "json",
                    "action": "query",
                    "titles": title,
                    "prop": "revisions",
                    "rvlimit": 1,
                    "rvprop": "timestamp|user",
                    "rvdir": "newer",
                },
            ).json()
            # print(hebRes)
            for p in revision["query"]["pages"]:
                timestamp = revision["query"]["pages"][p]["revisions"][0]["timestamp"]
                user = revision["query"]["pages"][p]["revisions"][0]["user"]
                f.write(
                    title
                    + "|"
                    + str(size)
                    + "|"
                    + user
                    + "|"
                    + timestamp
                    + "|"
                    + touched
                    + "\n"
                )
