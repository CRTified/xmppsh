from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout

class XmppshBot(ClientXMPP):

    def __init__(self, jid, password, parser, connection):
        ClientXMPP.__init__(self, jid, password)
#        parser.registerCommand([("muc", ), ("join", "Joins a given MUC", self.cmdjoinMuc)])

        self.parser = parser
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
        self.joinMUC("its_babos@conference.ruhr-uni-bochum.de", "l33tbot") # TODO

    def cmdjoinMuc(self, param, fromUser):
        try:
            muc = param[0]
            nick = param[1]
            passwd = param[2] if len(param) == 3 else ""

            self.joinMUC(muc, nick, passwd)
        except:
            return ("Something went wrong", 2)

    def joinMUC(self, room, nick=None, mucpassword=None):
        if mucpassword is not None:
            self.plugin['xep_0045'].joinMUC(room, nick, password=mucpassword, wait=True)
        else:
            self.plugin['xep_0045'].joinMUC(room, nick, wait=True)

    def mucmessage(self, msg):
        if msg['from'] != self.plugin['xep_0045'].getOurJidInRoom(msg['from'].bare) and msg['body']:
            response = self.parser.parseMessage(msg)
            self.connection.commit()
            if response is not None:
                print(msg['from'])
                replymsg = msg.reply(response[0])
                replymsg.send()


    def message(self, msg):
        if msg['body'] and msg['type'] != 'groupchat':
            response = self.parser.parseMessage(msg)
            self.connection.commit()
            if response is not None:
                msg.reply(response[0]).send()

