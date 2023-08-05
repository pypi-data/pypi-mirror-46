import json

from .errors import JrsNodeNotFound
from .refs_resolver import RefsResolver


class Context(object):

    def __init__(self):
        self.schemas = {}
        self.nodes = {}
        self.refsResolver = RefsResolver(self)

    def addSchema(self, schema):
        self.schemas[schema.id] = schema

    def addNode(self, schemaId, path, node):
        self.nodes["{}#{}".format(schemaId, path)] = node

    def getNode(self, schemaId, path):
        fullPath = "{}#{}".format(schemaId, path.replace("/", "."))
        if fullPath not in self.nodes:
            raise JrsNodeNotFound("Not found node with schemaId: {}, path: {}".format(schemaId, path))

        return self.nodes[fullPath]

    def initNodes(self):
        for schema in self.schemas.values():
            schema.root.initNodes()

    def resolveRefs(self):
        self.refsResolver.resolveRefs()

    def toJson(self, prettyPrint):
        schemas = {}
        for item in self.schemas.values():
            schemas[item.id] = item.root.value

        if prettyPrint:
            return json.dumps(schemas, separators=(",", ": "), indent=4) + "\n"
        else:
            return json.dumps(schemas, separators=(",", ":"))
