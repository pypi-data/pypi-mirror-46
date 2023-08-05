

class RefsGroup(object):

    def __init__(self, name):
        self._name = name
        self._group = {}
        self._cachedPathes = {}

    def add(self, schemaId, path, ref):
        if schemaId not in self._group:
            self._group[schemaId] = {}

        self._group[schemaId][path] = ref

    def getPathes(self, schemaId):
        if schemaId not in self._group:
            return []

        if schemaId not in self._cachedPathes:
            self._cachedPathes[schemaId] = reversed(sorted(
                self._group[schemaId].keys()
            ))
        return self._cachedPathes[schemaId]

    def getRef(self, schemaId, path):
        return self._group[schemaId][path]
