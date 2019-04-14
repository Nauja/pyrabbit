import sys

from .__pkginfo__ import version as __version__


from .rabbit import *


def Run():
    from . import rabbit

    try:
        rabbit.Run(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit(1)
