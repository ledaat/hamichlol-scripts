from mwclient import Site

he = Site("www.hamichlol.org.il")
yi = Site("yi.hamichlol.org.il")


def addLinks(page, file):
    for article in page.links(namespace=8000):
        result = yi.api("query", redirects=True, prop="info", titles=article.name)
        for p in result["query"]["pages"].values():
            if "length" in p:
                size = p["length"]
        for link in article.langlinks():
            if link[0] == "he":
                result = he.api("query", redirects=True, prop="info", titles=link[1])
                for p in result["query"]["pages"].values():
                    if "length" in p:
                        file.write(
                            article.name
                            + "|"
                            + str(size)
                            + "|"
                            + p["title"]
                            + "|"
                            + str(p["length"])
                            + "\n"
                        )


names = [
    "המכלול:וויכטיגסטע ארטיקלען/געאגראפיע און היסטאריע",
    "המכלול:וויכטיגסטע ארטיקלען/געזעלשאפט און קונסט",
    "המכלול:וויכטיגסטע ארטיקלען/וויסנשאפט און טעכנאלאגיע",
    "המכלול:וויכטיגסטע ארטיקלען/תורה און אידישקייט",
]

with open("important.csv", "w", encoding="utf-8") as f:
    f.write("ארטיקל|גרויס|ערך|גודל\n")
    for name in names:
        page = yi.pages[name]
        addLinks(page, f)
