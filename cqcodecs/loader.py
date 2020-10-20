import os
import importlib
import pkgutil

def load_codecs():
    cq_codecs = {}

    # Search all of the modules in the current directory to find codecs
    for finder, name, ispkg in pkgutil.iter_modules([os.path.join(".", "cqcodecs")]):
        if name.startswith('cq_codec_'):
            cq_codecs[name] = importlib.import_module("cqcodecs." + name)

    return cq_codecs