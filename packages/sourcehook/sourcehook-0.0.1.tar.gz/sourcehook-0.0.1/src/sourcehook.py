import importlib.machinery
from importlib.machinery import SourceFileLoader
from typing import List
from unittest.mock import patch

import distutils.file_util


__all__ = ("patch_distutils",)


def _copy_and_maybe_modify_file(
    src,
    dst,
    preserve_mode=1,
    preserve_times=1,
    update=0,
    link=None,
    verbose=1,
    dry_run=0,
    _original_copy_file=distutils.file_util.copy_file,
):

    dest_name, copied = _original_copy_file(
        src, dst, preserve_mode, preserve_times, update, link, verbose, dry_run
    )

    if copied:
        with open(dest_name, "rb") as f:
            content = f.read()
        assert isinstance(content, bytes)
        modified_source = _maybe_modify_source(content)
        with open(dest_name, "wb") as f:
            f.write(modified_source)

    return dest_name, copied


def _maybe_modify_source(data: bytes):
    first_line, other = data.split(b"\n", 1)
    if first_line.strip() == b"# sourcehook: enable":
        return _modify_source(other)
    return data


def _modify_source(data: bytes):
    #
    # Here we patch source data so that all the module becomes defined
    # inside a function. Name of the function does not matter. This hack
    # allows cloudpickle to serialize all the objects, including classes
    # and functions without links to the main package. This replaces our
    # previous solution which used factories.
    #
    result: List[bytes] = (
        [b"def _global_scope():"]
        + [b"    " + line for line in data.splitlines()]
        + [b"    return locals()", b"", b"globals().update(_global_scope())"]
    )
    return b"\n".join(result)


def patch_distutils():
    return patch.object(distutils.file_util, "copy_file", _copy_and_maybe_modify_file)


class CustomSourceFileLoader(SourceFileLoader):
    def source_to_code(self, data: bytes, path, *, _optimize=-1):
        print(self.name)
        modified_source: bytes = _maybe_modify_source(data)
        return super().source_to_code(modified_source, path, _optimize=_optimize)


def source_file_loader_hook():
    return patch.object(importlib.machinery, "SourceFileLoader", CustomSourceFileLoader)
