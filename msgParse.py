from commandTree import commandTree
import re
import traceback


class msgParse:
    def __init__(self):
        self._command = commandTree(None, None, None, None)
        self._trigger = []
        self.registerCommand([(u"help", "Displays the help for registered Commands", self._help)])
        pass

    def _getPermission(self, fromUser): # TODO!
        return 1

    def _executeCommand(self, cmd, fromUser):
        (c, param) = self._command.findByName(cmd[:])
        if c is not None and c._executeFunction is not None:
            if not c.isPermitted(self._getPermission(fromUser)):
                return ("You are lacking the permission to execute this Command", 2)
            try:
                return c._executeFunction(param, fromUser)
            except Exception as e:
                return (traceback.format_exc(), 3)
        else:
            return None

    def _executeTrigger(self, messageText, fromUser):
        returnLines = []
        returnRange = 1
        for trigger in self._trigger:
            for mat in trigger[0].finditer(messageText):
                tmpreturn = self._executeCommand(trigger[1] + [mat.group(0)], fromUser)
                returnLines.append(tmpreturn[0])
                returnRange = tmpreturn[1] if tmpreturn[1] >= returnRange else returnRange
            if len(returnLines) > 0:
                return ("\n".join(returnLines), returnRange)
        return None

    def parseMessage(self, message):
        messageText = message['body']
        comRet = self._executeCommand(messageText.split(" "), message.getFrom()) #['from'])

        if comRet is None:
            comRet = self._executeTrigger(messageText, message.getFrom())
        return comRet


    def registerCommand(self, cmd):
        try:
            cmdname = " ".join([str(c[0]) for c in cmd])
            self._command.integrateCMD(cmd)
            print("Command has been registered: %s" % (cmdname))
            return True
        except Exception:
            print(Exception.message)
            return False

    def registerTrigger(self, regex, cmd):
        if self._command.findByName(cmd[:]) is not None:
            newTrigger = (re.compile(regex), cmd)
            self._trigger.append(newTrigger)
            print("Trigger has been registered: %s maps to %s" % (regex, cmd))
            return True
        print("Trigger has not been registered: Command missing")
        return False

    def _help(self, cmd, fromUser):
        (c, param) = self._command.findByName(cmd)
        if c is not None:
            return ("Help:\n\n.\n" + c.manpage(-1), 1)
        return self._help(["help"], fromUser)
