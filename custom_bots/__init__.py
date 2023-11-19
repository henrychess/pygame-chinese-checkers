import importlib
from glob import glob

for module in glob("custom_bots/*py"):
    if not module.endswith("__init__.py"):
        importlib.import_module(module.replace(
            "/", ".").replace("\\", ".").removesuffix(".py"))
