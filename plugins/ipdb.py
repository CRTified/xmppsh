import socket
import sqlite3

class Plugin:
    def __init__(self, parser, sqlitecur):
        self._cursor = sqlitecur
        self._cursor.execute("CREATE TABLE IF NOT EXISTS IPs(Id INT, Name TEXT, IP TEXT, MUC TEXT)")
        parser.registerCommand([(u"ip", ), (u"list", "List all registered IPs", self._list)])
        parser.registerCommand([(u"ip", ), (u"register", "Register your IP", self._register)])

    def _list(self, ignore, fromUser):
        self._cursor.execute("SELECT Name, IP FROM IPs WHERE MUC=?", (fromUser.bare, ))
        rows = self._cursor.fetchall()
        msgtext = ""
        for r in rows:
            msgtext += "%s - %s\n" % (r[1], r[0])
        return (msgtext, 0)

    def _register(self, ip, fromUser):
        try:
            socket.inet_aton(ip[0])
            name = fromUser.resource
            muc = fromUser.bare
            self._cursor.execute("UPDATE OR IGNORE IPs SET IP=? WHERE Name=? AND MUC=?", (ip[0], name, muc))
            if self._cursor.rowcount == 0:
                self._cursor.execute("INSERT OR IGNORE INTO IPs (IP, Name, MUC) VALUES (?, ?, ?)", (ip[0], name, muc))
            return ("Your IP %s has been added" % (ip[0]), 1)
        except socket.error:
            return ("Your IP looks malformed", 1)
        except:
            return ("You omitted the IP", 1)

