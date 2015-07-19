class Plugin:
    def __init__(self, parser, sqlitecur):
        parser.registerCommand([(u"ping", "Allows you to test your connection", self._ping)])

    def _ping(self, ping, fromUser):
        return ( "pong [%s]" % (" ".join(ping)), 1)
