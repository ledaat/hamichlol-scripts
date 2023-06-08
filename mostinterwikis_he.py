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
        result = requests.get("https://he.wikipedia.org/w/api.php", params=req).json()
        if "error" in result:
            raise Error(result["error"])
        if "warnings" in result:
            print(result["warnings"])
        if "query" in result:
            yield result["query"]["querypage"]
        if "continue" not in result:
            break
        lastContinue = result["continue"]


with open("mostinterwikis_he.csv", "w", encoding="utf-8") as f:
    f.write("נאמען|וויקיס|גרויס\n")
    for result in query({"list": "querypage", "qppage": "Mostinterwikis"}):
        # print(result)
        for page in result["results"]:
            # print(page)
            title = page["title"]
            wikis = page["value"]
            # print(title + ' + ' + wikis)
            time.sleep(0.1)
            info = requests.get(
                "https://he.wikipedia.org/w/api.php",
                {"format": "json", "action": "query", "titles": title, "prop": "info"},
            ).json()
            # print(info)
            for i in info["query"]["pages"]:
                # print(i)
                size = info["query"]["pages"][i]["length"]
            f.write(title + "|" + str(wikis) + "|" + str(size) + "\n")
