from slixmpp import ClientXMPP
from slixmpp.exceptions import IqError, IqTimeout

class XmppshBot(ClientXMPP):

    def __init__(self, jid, password, cmdparser, connection):
        ClientXMPP.__init__(self, jid, password)
#        cmdparser.registerCommand([("muc", ), ("join", "Joins a given MUC", self.cmdjoinMuc)])

        self.cmdparser = cmdparser
        self.connection = connection
        self.cursor = connection.cursor()
        self.register_plugin('xep_0045')

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.add_event_handler('groupchat_message', self.mucmessage)

        self.cursor.execute("CREATE TABLE IF NOT EXISTS MUC(Id INT, MUC TEXT, Nick TEXT, Pass TEXT)")


    def session_start(self, event):
        self.send_presence()
        try:
            self.get_roster()
        except IqError as err:
            logging.error('There was an error getting the roster')
            logging.error(err.iq['error']['condition'])
            self.disconnect()
        except IqTimeout:
            logging.error('Server is taking too long to respond')
            self.disconnect()
        self.join_muc("xmppshtest@example.com", "l33tbot") # TODO

    def cmdjoinMuc(self, param, fromUser):
        try:
            muc = param[0]
            nick = param[1]
            passwd = param[2] if len(param) == 3 else ""

            self.join_muc(muc, nick, passwd)
        except:
            return ("Something went wrong", 2)

    def join_muc(self, room, nick=None, mucpassword=None):
        if mucpassword is not None:
            self.plugin['xep_0045'].join_muc(room, nick, password=mucpassword, wait=True)
        else:
            self.plugin['xep_0045'].join_muc(room, nick, wait=True)

    def mucmessage(self, msg):
        if msg['from'] != self.plugin['xep_0045'].get_our_jid_in_room(msg['from'].bare) and msg['body']:
            response = self.cmdparser.parseMessage(msg)
            self.connection.commit()
            if response is not None:
                print(msg['from'])
                replymsg = msg.reply(response[0])
                replymsg.send()


    def message(self, msg):
        if msg['body'] and msg['type'] != 'groupchat':
            response = self.cmdparser.parseMessage(msg)
            self.connection.commit()
            if response is not None:
                msg.reply(response[0]).send()

