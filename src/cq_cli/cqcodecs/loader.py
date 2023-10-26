import os
import importlib
import pkgutil


def load_codecs():
    cq_codecs = {}

    # Search all of the modules in the current directory to find codecs
    for finder, name, ispkg in pkgutil.iter_modules([os.path.dirname(__file__)]):
        if name.startswith("cq_codec_"):
            cq_codecs[name] = importlib.import_module("cq_cli.cqcodecs." + name)

    return cq_codecs
