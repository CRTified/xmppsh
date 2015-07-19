from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout

class XmppshBot(ClientXMPP):

    def __init__(self, jid, password, parser):
        ClientXMPP.__init__(self, jid, password)

        self.parser = parser
        self.register_plugin('xep_0045')

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.add_event_handler('groupchat_message', self.mucmessage)
	


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

    def mucmessage(self, msg):
        if msg['mucnick'] != self.nick and msg['body']:
            response = self.parser(msg)
            if response is not None:
                msg.reply(response[0]).send()

    def message(self, msg):
        response = self.parser(msg)
        if response is not None:
            msg.reply(response[0]).send()

