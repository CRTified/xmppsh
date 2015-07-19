import traceback

class commandTree:
    def __init__(self, name, parent, manual="", executeFunction=None, permissionNeeded=1):
        self._name = name
        self._parent = parent
        self._executeFunction = executeFunction
        self._manual = manual
        self._childs = []
        self._permissionNeeded = permissionNeeded

    def isPermitted(self, permission):
        return self._permissionNeeded <= permission

    def _addChild(self, child):
        self._childs.append(child)

    def integrateCMD(self, cmd):
        nextNodeVals = cmd.pop(0)
        if len(nextNodeVals) == 5:
            nextNode = commandTree(nextNodeVals[0], self, nextNodeVals[1], nextNodeVals[2], nextNodeVals[3], nextNodeVals[4])
        elif len(nextNodeVals) == 4:
            nextNode = commandTree(nextNodeVals[0], self, nextNodeVals[1], nextNodeVals[2], nextNodeVals[3])
        elif len(nextNodeVals) == 3:
            nextNode = commandTree(nextNodeVals[0], self, nextNodeVals[1], nextNodeVals[2])
        elif len(nextNodeVals) == 2:
            nextNode = commandTree(nextNodeVals[0], self, nextNodeVals[1])
        elif len(nextNodeVals) == 1:
            nextNode = commandTree(nextNodeVals[0], self)
        else:
            raise Exception("A Command is defined in an unclean way.")
        c = self.findChildByName(nextNodeVals[0])
        if c is not None:
            c.integrateCMD(cmd)
        else:
            self._addChild(nextNode)
            if len(cmd) > 0:
                nextNode.integrateCMD(cmd)

    def findChildByName(self, cmd):
        for c in self._childs:
            if c._name == cmd:
                return c
        return None

    def findByName(self, cmd):
        if len(cmd) is 0:
            return (self, [])

        nextCmd = cmd.pop(0)
        c = self.findChildByName(nextCmd)
        if c is not None:
            return c.findByName(cmd)

        if self._executeFunction is not None:
            return (self, [nextCmd] + cmd)
        return (None, None)

    def __str__(self):
        if self._parent is None:
            return ""
        return "%s\t%s" % (self._name, self._manual)

    def manpage(self, depth=-1):
        childManpage = [c.manpage(depth + 1) for c in self._childs]

        if self._parent is None:
            fullHelp = "\n".join(childManpage)
        else:
            fullHelp = "\n".join(["%s%s|-+ %s" % ("| " if depth > 0 else "", "  " * (depth - 1), str(self))] + childManpage)
        return fullHelp

    def getListOfParents(self):
        if self._parent is None:
            return []
        return self._parent.getListOfParents() + [self]

