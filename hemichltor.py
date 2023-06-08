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
            "https://www.hamichlol.org.il/w/api.php", params=req
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


with open("torani.csv", "w", encoding="utf-8") as f:
    for result in query(
        {
            "generator": "categorymembers",
            "gcmtitle": "קטגוריה:המכלול: ערכים הנכללים בזים תורני",
            "prop": "info",
        }
    ):
        for page in result["pages"]:
            title = result["pages"][page]["title"]
            size = result["pages"][page]["length"]
            touched = result["pages"][page]["touched"]
            f.write(title + "|" + str(size) + "|" + touched + "\n")
