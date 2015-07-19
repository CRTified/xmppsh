import random
from datetime import timedelta

class Plugin:
    def __init__(self, parser, sqlitecur):
        self._templates = [ "Uhm, I think my age is %s."
                , "My age is: %s"
                , "Notice me, Senpai. I'm already %s"
                , "%s ~desu~"
                , "%s ~degeso" ]
        parser.registerCommand([(u"age", "Prints the uptime of the System I'm living on", self._uptime)])

    def _uptime(self, ignore, fromUser):
        uptime_string = ""
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds = uptime_seconds))
        return (random.choice(self._templates) % (uptime_string), 0)


