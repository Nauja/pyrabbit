__all__ = ["load", "html", "raw"]
from . import html
from . import raw
import pkg_resources
from typing import Any


def load(name: str) -> Any:
    """Get the first renderer identified by `name`.

	The renderer must have been registered as an entry point for
	`pysachi.renderers` via setuptools.

    .. code-block:: python

        renderer = pysachi.renderers.load("raw")

	:param name: Renderer's name.
	:returns: Found renderer or None.
	"""
    for entry_point in pkg_resources.iter_entry_points("pysachi.renderers"):
        if entry_point.name == name:
            return entry_point.load()
    return None
