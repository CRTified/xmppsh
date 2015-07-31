import hashlib

class Plugin:
    def __init__(self, parser, sqlitecur):
        parser.registerCommand([("hash", "Calculates all hashes", self._allHash)])
        for h in hashlib.algorithms_available:
            parser.registerCommand([("hash",), (h, "Calculates the %s" % h, self._hashCurry(h))])


    def _allHash(self, params, fromUser):
        if len(params) == 0:
            return ("No data supplied", 1)
        retLines = []
        paramstr = " ".join(params).encode()
        for h in hashlib.algorithms_available:
            n = hashlib.new(h)
            n.update(paramstr)
            retLines.append("%s\t%s" % (h, n.hexdigest()))
        return ("\n".join(retLines), 1)
            

    def _hashCurry(self, hashfunction):
        def hashIt(params, fromUser):
            if len(params) == 0:
                return ("No data supplied", 1)
            n = hashlib.new(hashfunction)
            n.update(' '.join(params).encode())
            return (n.hexdigest(), 1)
        return hashIt
