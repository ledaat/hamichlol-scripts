from mwclient import Site

he = Site("www.hamichlol.org.il")
he.login("מוטי בוט", "my_password") # change this
yi = Site("yi.hamichlol.org.il")
category = yi.categories["המכלול ארטיקלען"]


def addLink(hebrew, yiddish):
    """
     Add a link to the hebrew page.
     
     :param hebrew: the name of the article
     :param yiddish: the name of the link to add
     :returns: whether the link was added ( True ) or not ( False )
    """
    article = he.pages[hebrew]
    article = article.resolve_redirect()  # just to make sure
    # returns the interlanguage links on page as tuple (language code, name)
    for kishur in article.langlinks():
        # linked yi kishur 0 is yi
        if kishur[0] == "yi":  # already linked
            return False
    article.append(
        "\n[[yi:" + yiddish + "]]",
        summary="הוספת קישור בינוויקי " + "[[yi:" + yiddish + "]]",
        minor=True,
        bot=True,
    )
    return True


def main():
    """
     Add links to each page in category. This is called when the program starts.
     We iterate through category and check if there are interlanguage links to hebrew.
    """
    # Add links to the category
    for page in category:
        # Add the page s langlinks to the page.
        for link in page.langlinks():
            # Add a link to the page
            if link[0] == "he":
                addLink(link[1], page.name)


# main function for the main module
if __name__ == "__main__":
    main()
