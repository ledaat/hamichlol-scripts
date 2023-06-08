import requests
import time


def query(request):
    """
     Query Hamichlol's API with a list of data to return.
     This is a generator that yields query data as they arrive.
     
     :param request: A dict with (keys 'action' and 'format are added automatically)
    """
    request["action"] = "query"
    request["format"] = "json"
    lastContinue = {}
    # Yields the query results from Yi Hamichlol API.
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
        # If there is an error in the result, bark
        if "error" in result:
            raise Error(result["error"])
        # Print warnings in the result
        if "warnings" in result:
            print(result["warnings"])
        # Everything fine, yield the query from the result
        if "query" in result:
            yield result["query"]
        # nothing more to continue?
        if "continue" not in result:
            break
        lastContinue = result["continue"]


# get the names of all redirects
for result in query(
    {
        "generator": "allpages",
        "gapnamespace": 10,
        "gapfilterredir": "redirects",
        "gaplimit": "max",
    }
):
    # Are they cyclical redirects?
    for page in result["pages"]:
        title = result["pages"][page]["title"]
        time.sleep(0.1)
        for redir in query({"titles": title, "redirects": 1}):
            if title == redir["redirects"][0]["to"]:
                print(title)
