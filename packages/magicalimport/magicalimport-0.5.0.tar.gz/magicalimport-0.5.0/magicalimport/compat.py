import sys

__ALL__ = [
    "import_module",
    "_create_module",
    "ModuleNotFoundError",
    "FileNotFoundError",
]


try:
    from importlib import import_module  # NOQA
    from importlib.util import spec_from_file_location
    from importlib.util import module_from_spec

    def _create_module(module_id, path):
        spec = spec_from_file_location(module_id, path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module_id] = module
        return module


except ImportError:
    try:
        # for 3.3, 3.4
        from importlib import machinery

        def _create_module(module_id, path):
            return machinery.SourceFileLoader(module_id, path).load_module()

    except ImportError:
        # patching for import machinery
        # https://bitbucket.org/ericsnowcurrently/importlib2/issues/8/unable-to-import-importlib2machinery
        import importlib2._fixers as f

        fix_importlib_original = f.fix_importlib

        def fix_importlib(ns):
            if ns["__name__"] == "importlib2.machinery":

                class _LoaderBasics:
                    load_module = object()

                ns["_LoaderBasics"] = _LoaderBasics

                class FileLoader:
                    load_module = object()

                ns["FileLoader"] = FileLoader

                class _NamespaceLoader:
                    load_module = object()
                    module_repr = object()

                ns["_NamespaceLoader"] = _NamespaceLoader
            fix_importlib_original(ns)

        f.fix_importlib = fix_importlib
        from importlib2 import machinery
        from importlib2 import import_module  # NOQA

        def _create_module(module_id, path):
            return machinery.SourceFileLoader(module_id, path).load_module()


try:
    ModuleNotFoundError = ModuleNotFoundError
except NameError:
    try:
        from importlib2 import ModuleNotFoundError

        ModuleNotFoundError = ModuleNotFoundError
    except ImportError:
        # for <3.6
        class ModuleNotFoundError(ImportError):
            fake = True


try:
    FileNotFoundError = FileNotFoundError
except NameError:

    class FileNotFoundError(OSError):
        fake = True
