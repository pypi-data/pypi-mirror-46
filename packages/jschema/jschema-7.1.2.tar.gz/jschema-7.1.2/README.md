# jschema

Library for compiling json-schemas specifications with $refs from yaml to json with resolved $refs.
Expected json-schemas with unique field id, and type in method, definitions


## Json Schema compiler

1. Read yaml files from --root directory
2. Resolve $ref in this files
3. Remove comments keys
4. Write result to stdout in json format

**Usage in python3:**

```python3
from jschema import loadSchemas
ctx = loadSchemas("tests/sources/multirefs")
ctx.initNodes(clear=True)
ctx.resolveRefs()
ctx.toJson(prettyPrint=True)
```


**Usage in bash:**

```bash
jschema --root tests/sources/multirefs --prettyPrint > multirefs.json
```


## JsonSchema Docs generator

1. Read yaml files from --root directory
2. Resolve $ref in this files
3. Generate documentation to --destination

**Usage:**
```bash

jschema-docs --root tests/sources/multirefs --destination tests/build

```


## Develop

**Login container:**

```
lxc exec jschema-dev -- sudo --login --user ubuntu
```

**Create container:**

```
lxc init ubuntu:18.04 jschema-dev
lxc config set jschema-dev raw.idmap "both $UID 1000"
lxc config device add jschema-dev project disk source=$PWD path=/home/ubuntu/jschema
lxc start jschema-dev
```
