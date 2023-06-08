import requests
import time


def query(request):
    request["action"] = "query"
    request["format"] = "json"
    lastContinue = {}
    lastplContinue = {}
    while True:
        # Clone original request
        req = request.copy()
        # Modify with the values returned in the 'continue' section of the last result.
        req.update(lastContinue)
        req.update(lastplContinue)
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
        if "plcontinue" in result:
            lastplContinue = result["plcontinue"]


for result in query(
    {
        "generator": "categorymembers",
        "gcmtitle": "קאטעגאריע:באדייטן בלעטער",
        "prop": "links",
        "pllimit": "max",
    }
):
    for page in result["pages"]:
        links = 0
        title = result["pages"][page]["title"]
        if "links" in result["pages"][page]:
            links = len(result["pages"][page]["links"])
        print(title + "|" + str(links))
