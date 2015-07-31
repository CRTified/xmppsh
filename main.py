import os
import sys
from msgParse import msgParse
from connector import XmppshBot
import sqlite3
import logging
import getpass



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

def main(user, password):
    sqlitecon = sqlite3.connect('storage.db', check_same_thread=False, isolation_level=None)
    commandParser = msgParse()
    loadPlugins(commandParser, sqlitecon)

    xmpp = XmppshBot(user, password, commandParser, sqlitecon)
    xmpp.connect()
    xmpp.process(block=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')
    main(sys.argv[1], getpass.getpass())
