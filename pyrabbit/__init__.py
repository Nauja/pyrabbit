import sys

from .__pkginfo__ import version as __version__


def run():
    from pyrabbit import run

    try:
        pyrabbit.run(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit(1)
