from mwclient import Site

he = Site("www.hamichlol.org.il")
yi = Site("yi.hamichlol.org.il")
category = yi.categories["עלעמענטארע ארטיקלען צו פארברייטערן"]


with open("elementary.csv", "w", encoding="utf-8") as f:
    f.write("ארטיקל|גרויס|ערך|גודל\n")
    for page in category:
        result = yi.api("query", prop="info", titles=page.name)
        for p in result["query"]["pages"].values():
            if "length" in p:
                size = p["length"]
        for link in page.langlinks():
            if link[0] == "he":
                result = he.api("query", redirects=True, prop="info", titles=link[1])
                for p in result["query"]["pages"].values():
                    if "length" in p:
                        f.write(
                            page.name
                            + "|"
                            + str(size)
                            + "|"
                            + p["title"]
                            + "|"
                            + str(p["length"])
                            + "\n"
                        )
