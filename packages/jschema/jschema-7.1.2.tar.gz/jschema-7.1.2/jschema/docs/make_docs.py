import os
import json
import shutil
from jinja2 import Environment, FileSystemLoader

curDir = os.path.abspath(os.path.dirname(__file__))

def makeDocs(ctx, dstDir):
    jinjaEnv = Environment(
        loader=FileSystemLoader(os.path.join(curDir, "templates")),
        trim_blocks=True,
        lstrip_blocks=True,
        extensions=["jinja2.ext.with_"]
    )
    jinjaEnv.filters["omitKeys"] = lambda obj, keys: {key: value for key, value in obj.items() if key not in keys}
    jinjaEnv.filters["jsonPrettyDump"] = lambda value: json.dumps(value, separators=(',', ': '), indent=4)
    schemasDir = os.path.join(dstDir, "schemas")
    if not os.path.exists(schemasDir):
        os.mkdir(schemasDir)

    vendorDir = os.path.join(dstDir, "vendor")
    if not os.path.exists(vendorDir):
        shutil.copytree(os.path.join(curDir, "vendor"), vendorDir)

    indexTemplate = jinjaEnv.get_template("index.j2")

    methods = []
    structs = []
    for schema in ctx.schemas.values():
        if schema.root.value["type"] == "method":
            methods.append(schema.id)
        else:
            structs.append(schema.id)
    indexPath = os.path.join(dstDir, "index.html")
    with open(indexPath, "w") as fstream:
        fstream.write(indexTemplate.render(methods=sorted(methods), structs=sorted(structs)))
    print(" - Created: " + indexPath)

    schemaTemplate = jinjaEnv.get_template("schema.j2")
    for schema in ctx.schemas.values():
        schemaPath = os.path.join(schemasDir, schema.id + ".html")
        with open(schemaPath, "w") as fstream:
            fstream.write(schemaTemplate.render(schema=schema.root.value))
        print(" - Created: " + schemaPath)
