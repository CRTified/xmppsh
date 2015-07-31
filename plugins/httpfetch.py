import urllib.request
from bs4 import BeautifulSoup


class Plugin:
    def __init__(self, parser, sqlitecur):
        parser.registerCommand([(u"http", ), (u"title", "Tries to fetch the page title", self._urlTitle)])
        parser.registerTrigger("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", [u"http", u"title"])


    def _urlTitle(self, url, fromUser):
        try:
            response = urllib.request.urlopen(url[0], None, 3).read()
            title = BeautifulSoup(response).html.head.title.string
        except:
            title = "[Not able to fetch the title]"
        title = "%s (%s)" % (title, url[0])
        return (title, 2)


