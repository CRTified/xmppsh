import os
import sys
from msgParse import msgParse
from connector import XmppshBot
import sqlite3
import logging


def loadPlugins(parser, sqlitecon):
    path = "plugins/"
    plugins = {}
    # Load plugins
    sys.path.insert(0, path)
    for f in os.listdir(path):
        fname, ext = os.path.splitext(f)
        if ext == ".py":
            print("Loading %s" % fname) # TODO: Move to logging
            mod = __import__(fname)
            plugins[fname] = mod.Plugin(parser, sqlitecon.cursor())
    sys.path.pop(0)

def main(user, password, muc):
    commandParser = msgParse()
    sqlitecon = sqlite3.connect("storage.db")

    loadPlugins(commandParser, sqlitecon)

    xmpp = XmppshBot(user, password, commandParser.parseMessage)
    xmpp.connect()
    xmpp.process(block=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, format='%(levelname)-8s %(message)s')
    main(sys.argv[1], sys.argv[2])
