from importlib import import_module


def import_class(path):
    parts = path.split(".")
    module_path = ".".join(parts[:-1])
    cls_name = parts[-1]

    try:
        m = import_module(module_path)
        cls = getattr(m, cls_name)
        if cls is None:
            raise Exception(f"Could not import {path}")
        return cls
    except ImportError:
        raise Exception(f"Could not import {path}")
