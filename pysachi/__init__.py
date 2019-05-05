import sys

from .__pkginfo__ import version as __version__

from .sachi import *


def Run():
    from . import sachi

    try:
        sachi.main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit(1)
