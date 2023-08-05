from .node import Node

class Schema(object):

    def __init__(self, ctx, source, sourceDir):
        self.id = source["id"]
        self.dir = sourceDir
        self.root = Node(ctx, self.id, source, parent=None)
