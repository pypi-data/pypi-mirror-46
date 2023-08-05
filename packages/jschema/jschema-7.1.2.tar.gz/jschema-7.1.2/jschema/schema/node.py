

class NodeChilds(object):

    def __init__(self, nodes):
        self.nodes = nodes
        self.isArray = type(nodes) == list
        self.isObject = type(nodes) == dict

    def add(self, child):
        if self.isArray:
            self.node.append(child)
        elif self.isObject:
            self.node[child.key] = child


class Node(object):

    def __init__(self, ctx, key, value, parent):
        self.ctx = ctx
        self.key = key
        self.value = value
        self.parent = parent

        if parent is None:
            self.root = None
            self.path = ""
        elif parent.root is None:
            self.root = parent
            self.path = key
        else:
            self.root = parent.root
            self.path = "{}.{}".format(parent.path, key)

        self.childs = []

        if parent:
            ctx.addNode(self.root.key, self.path, self)

    def initNodes(self):
        valueType = type(self.value)
        isDict = valueType is dict
        isList = valueType is list

        if isDict and "$ref" in self.value:
            self._resolveRef()
        elif isDict:
            self._resolveDict()
        elif isList:
            self._resolveList()

    def _resolveRef(self):
        if self.value["$ref"].index("#") == 0:
            schemaId, path = self.root.key, self.value["$ref"][1:]
        else:
            schemaId, path = self.value["$ref"].split("#")

        path = path.lstrip("/")
        ref = self.ctx.refsResolver.Ref(schemaId, path, self)
        self.ctx.refsResolver.addRef(ref)

    def _resolveDict(self):
        for key, value in self.value.items():
            child = Node(self.ctx, key, value, parent=self)
            child.initNodes()
            self.childs.append(child)

    def _resolveList(self):
        for num, value in enumerate(self.value):
            child = Node(self.ctx, num, value, parent=self)
            child.initNodes()
            self.childs.append(child)
