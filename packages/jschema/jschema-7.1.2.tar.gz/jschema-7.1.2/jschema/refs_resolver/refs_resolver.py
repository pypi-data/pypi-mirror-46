from jschema.errors import JrsSchemaNotFound
from jschema.errors import JrsCircularRefs

from .refs_group import RefsGroup


class Ref(object):

    def __init__(self, schemaId, path, targetNode):
        self.schemaId = schemaId
        self.path = path
        self.target = targetNode
        self.refNode = None
        self.resolved = False


class RefsResolver(object):
    Ref = Ref

    def __init__(self, ctx):
        self.ctx = ctx
        self.targets = RefsGroup("targets")
        self.refs = []

    def addRef(self, ref):
        if ref.schemaId not in self.ctx.schemas:
            raise JrsSchemaNotFound("Schema not found, schemaId: {}".format(ref.schemaId))

        self.targets.add(
            schemaId=ref.target.root.key,
            path=ref.target.path,
            ref=ref
        )
        self.refs.append(ref)

    def _resolveRefs(self, ref, fromRefs):
        if ref.resolved:
            return

        ref.refNode = self.ctx.getNode(ref.schemaId, ref.path)

        relatedRef = None
        for path in self.targets.getPathes(ref.schemaId):
            if path.startswith(ref.target.path):
                relatedRef = self.targets.getRef(ref.schemaId, path)
                break;

        if relatedRef in fromRefs:
            raise JrsCircularRefs(JrsCircularRefs.make_message([relatedRef, ref] + fromRefs))

        if relatedRef is not None:
            self._resolveRefs(relatedRef, [ref] + fromRefs)

        ref.target.parent.value[ref.target.key] = ref.refNode.value
        ref.resolved = True

    def resolveRefs(self):
        for ref in self.refs:
            self._resolveRefs(ref, fromRefs=[])
