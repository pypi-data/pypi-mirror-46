import os
import yaml
import subprocess

from .errors import JrsSchemaError
from .schema import Schema
from .context import Context


def loadSchemas(rootDir):
    ctx = Context()

    res = subprocess.check_output(["find", rootDir, "-name", "*.yaml"])
    for fpath in res.split():
        with open(fpath) as fstream:
            source = yaml.load(fstream, Loader=yaml.SafeLoader)

        if "id" not in source:
            raise JrsSchemaError("Attribute 'id' not exists: {}".format(fpath.decode()))

        source["type"] = "type" in source and source["type"]

        if source["type"] == "method" and "params" not in source:
            raise JrsSchemaError("Attribute 'params' not exists in method: {}".format(fpath.decode()))

        sourceDir = os.path.dirname(fpath).decode("utf-8").replace(rootDir, "", 1).lstrip("/")
        ctx.addSchema(Schema(ctx, source, sourceDir))

    return ctx
