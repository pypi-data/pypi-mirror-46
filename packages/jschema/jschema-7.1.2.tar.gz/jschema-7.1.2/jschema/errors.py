import json


class JrsError(Exception):
    pass

class JrsSchemaError(JrsError):
    pass

class JrsSchemaNotFound(JrsError):
    pass

class JrsNodeNotFound(JrsError):
    pass

class JrsCircularRefs(JrsError):
    @staticmethod
    def make_message(refs):
        return "Circular references: {}".format(
            " -> ".join([
                "{}#{}".format(ref.schemaId, ref.path)
                for ref in reversed(refs)
            ])
        )
