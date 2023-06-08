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


for result in query(
    {
        "generator": "allpages",
        "gapnamespace": "8000",
        "gapfilterredir": "nonredirects",
        "gapfilterlanglinks": "withlanglinks",
        "gapfrom": "רבי שמחה זיסל",
    }
):
    time.sleep(1)
    for page in result["pages"]:
        title = result["pages"][page]["title"]
        # print(title)
        for hebRes in query({"prop": "langlinks", "titles": title, "lllang": "he"}):
            # print(hebRes)
            for p in hebRes["pages"]:
                if "langlinks" in hebRes["pages"][p]:
                    hebTitle = hebRes["pages"][p]["langlinks"][0]["*"]
                    # print(hebTitle)
                    hebInfo = requests.get(
                        "https://www.hamichlol.org.il/w/api.php",
                        {
                            "format": "json",
                            "action": "query",
                            "titles": hebTitle,
                            "redirects": 1,
                            "prop": "info",
                        },
                    ).json()
                    for q in hebInfo["query"]["pages"]:
                        if "length" in hebInfo["query"]["pages"][q]:
                            size = hebInfo["query"]["pages"][q]["length"]
                            # print(size)
                            print(title + "|" + hebTitle + "|" + str(size))
