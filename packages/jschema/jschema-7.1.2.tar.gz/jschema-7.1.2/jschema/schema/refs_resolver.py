from copy import deepcopy

from jschema.errors import JrsSchemaNotFound
from jschema.errors import JrsCircularRefs

from .nodes_cache import NodesCache


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
        if schemaId not in self._cachedPathes:
            self._cachedPathes[schemaId] = reversed(sorted(
                self._group[schemaId].keys()
            ))
        return self._cachedPathes[schemaId]

    def getRef(self, schemaId, path):
        return self._group[schemaId][path]


class Ref(object):

    def __init__(self, schemaId, path, targetNode):
        self.schemaId = schemaId
        self.path = path
        self.target = targetNode
        self.refNode = None
        self.resolved = False

class RefsResolver(object):

    @classmethod
    def init(cls):
        cls._schemas = {}
        cls._targets = RefsGroup("targets")
        cls._refs = []

    @classmethod
    def addSchema(cls, schema):
        cls._schemas[schema.id] = schema

    @classmethod
    def addRef(cls, ref):
        if ref.schemaId not in cls._schemas:
            raise JrsSchemaNotFound("Schema not found, schemaId: {}".format(ref.schemaId))

        cls._targets.add(
            schemaId=ref.target.root.key,
            path=ref.target.path,
            ref=ref
        )
        cls._refs.append(ref)

    @classmethod
    def _resolveRefs(cls, ref, fromRefs):
        if ref.resolved:
            return

        ref.refNode = NodesCache.get(ref.schemaId, ref.path)

        relatedRef = None
        for path in cls._targets.getPathes(ref.schemaId):
            if path.startswith(ref.target.path):
                relatedRef = cls._targets.getRef(ref.schemaId, path)
                break;

        if relatedRef in fromRefs:
            raise JrsCircularRefs(JrsCircularRefs.make_message([relatedRef, ref] + fromRefs))

        if relatedRef is not None:
            cls._resolveRefs(relatedRef, [ref] + fromRefs)

        ref.target.parent.value[ref.target.key] = ref.refNode.value
        ref.resolved = True

    @classmethod
    def resolveRefs(cls):
        for ref in cls._refs:
            cls._resolveRefs(ref, fromRefs=[])
