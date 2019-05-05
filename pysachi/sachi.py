__all__ = ["main", "run", "walk", "analyze", "render"]
import os
import sys
import argparse
import ast
from . import report
from .checkers import get_checkers
from .analyzer import DefaultAnalyzer
from . import renderers
from typing import List, Optional, Callable, Any
import json
from functools import reduce


def walk(tree: ast.AST, *, checkers: Optional[List[Any]] = None) -> report.ASTReport:
    """Run static code analysis over an :class:`ast.AST` node.

    Walking the tree is done by :class:`analyzer.DefaultAnalyzer`
    which run `checkers` on important nodes.

    :param tree: The root node to analyze.
    :param checkers: List of checks to run on nodes.
    :returns: A complete report of analysis.
    """
    checkers = checkers if checkers is not None else get_checkers()

    return DefaultAnalyzer().visit(tree, checkers=checkers)


def analyze(source: str, *, checkers: Optional[List[Any]] = None) -> report.ASTReport:
    """Run static code analysis on a source code.

    Example for a file:

    .. code-block:: python

        with open("/some/path/file.py", "r") as f:
            report = pysachi.analyze(f.read())

    Example for a module:

    .. code-block:: python

        import inspect

        report = pysachi.analyze(inspect.getsource(target))

    :param source: Source code to analyze.
    :param checkers: List of checks to run on source code.
    :returns: Analysis report.
    """
    return walk(ast.parse(source), checkers=checkers)


def render(report: report.ASTReport, *, renderer: str = None) -> str:
    """Render an :class:`report.ASTReport` to :obj:`str`.

    To use the default renderer `raw`:

    .. code-block:: python

        result = pysachi.render(report)

    To use a specific renderer:

    .. code-block:: python

        result = pysachi.render(report, renderer="html")

    Specified renderer will be loaded using `pkg_resources` and must
    have been registered as a `pysachi.renderers` entry point
    via setuptools for it to work. Fallback to `raw` renderer if
    the specified renderer can't be found.

    :param report: Analysis report.
    :param renderer: Name of renderer registered as entry point for `pysachi.renderers`.
    :returns: Rendered analysis report.
    """
    renderer = renderers.load(renderer or "raw")

    if not renderer:
        renderer = renderers.load("raw")

    return renderer.render(report)


def run(
    source: str, *, checkers: Optional[List[Any]] = None, renderer: str = None
) -> str:
    """Run static code analysis on a source code.

    This is a shortcut for:

    .. code-block:: python

        report = pysachi.analyze(source)
        result = pysachi.render(report)

    :param source: Source code to analyze.
    :param checkers: List of checkers to run on source code.
    :param renderer: Name of renderer to use.
    :returns: Rendered report.
    """
    return render(analyze(source, checkers=checkers), renderer=renderer)


def main(argv, file: List[str] = None) -> None:
    """Run from command line.

    This is meant to simulate `pysachi` usage from command line:

    .. code-block:: python

        pysachi.main("-o some/file.txt")

    It reads the source code from `sys.stdin` by default but this behavior
    can be modified like this:

    .. code-block:: python

        with open("some/file.py", "r") as f:
            pysachi.main("-o some/file.txt", file=f)


    :param argv: Command line arguments.
    :param file: File to read.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--renderer", type=str, default="raw", help="report renderer"
    )
    parser.add_argument(
        "-i", "--input", type=argparse.FileType("r"), help="source file"
    )
    parser.add_argument(
        "-o", "--output", type=argparse.FileType("w"), help="report file"
    )
    args = parser.parse_args(argv)

    file = file or args.input or sys.stdin
    source = reduce(lambda a, b: a + b, (line for line in sys.stdin))
    result = run(source, renderer=args.renderer)

    if args.output:
        args.output.write(result)
    else:
        print(result, end="")


if __name__ == "__main__":
    main(sys.argv[1:])
