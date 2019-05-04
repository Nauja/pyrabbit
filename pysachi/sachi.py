__all__ = ["run", "walk", "analyze", "render", "get_checkers"]
import sys
import argparse
import ast
from . import report
from . import checkers
from .analyzer import DefaultAnalyzer
from typing import List, Optional, Callable, Any
import json


def _read_file(filename: str) -> str:
    """Simply read content of a file.

    :param filename: File to read.
    :returns: File's content.
    """
    with open(filename, "r") as f:
        return f.read()


def get_checkers() -> List[Any]:
    """Get default checkers to run on code.

    :returns: List of default checkers to run.
    """
    return [checkers.function, checkers.readability]


def walk(tree: ast.AST, *, checkers: Optional[List[Any]] = None) -> report.ASTReport:
    """Run static code analysis over an :class:`ast.AST` node.

    Walking the tree is done by :class:`analyzer.DefaultAnalyzer`
    which run `checkers` on important nodes.

    :param tree: The root node to analyze.
    :param checkers: List of checks to run on nodes.
    :returns: A complete report of analysis.
    """
    checkers = checkers if checkers is not None else get_checkers()

    analyzer = DefaultAnalyzer(checkers)
    analyzer.visit(tree)
    return analyzer.report


def analyze(
    target: Any,
    *,
    get_source: Optional[Callable[[Any], str]] = None,
    checkers: Optional[List[Any]] = None
) -> report.ASTReport:
    """Run static code analysis on a target.

    By default `target` is expected to be a file to analyze.
    You can use this function as is to create a report from a file:

    .. code-block:: python

        report = pysachi.analyze("/some/path/file.py")

    You can pass your own `get_source` callable for custom targets.
    Here is the signature of this callable alongside with an example of using it
    to return source code of a module:

    .. code-block:: python

        import inspect

        def get_module_source(target):
            return inspect.getsource(target)

        report = pysachi.analyze(pysachi, get_source=get_module_source)

    :param targets: List of targets to analyze.
    :param get_source: A callable to convert a target to source code.
    :param checkers: List of checks to run on node.
    :returns: Reports of static code analysis for all targets.
    """
    get_source = get_source or _read_file

    return walk(
        ast.parse(get_source(target)),
        checkers=checkers
    )


def render(report: report.Report, *, renderer=None) -> str:
    """Render a report as :obj:`str`.

    """
    return json.dumps(report)


def run(
    targets: List[Any],
    *,
    checkers: Optional[List[Any]] = None,
    analyze: Optional[Callable[[Any], report.ASTReport]] = analyze,
    render: Optional[Callable[[report.Report], Any]] = render
) -> Any:
    """Run static code analysis on multiple targets and render analysis report.

    By default `targets` must be a list of files to analyze. You
    can use this function as is to get report from a specific file:

    .. code-block:: python

        report = pysachi.run(["/some/path/file.py"])

    Here is an example of how to pass your own `analyze` method to
    handle `targets` of custom type. The `get_source` lambda is called for
    each `target` to convert it to source code to analyze:

    .. code-block:: python

        def analyze_string(target, **kwargs):
            # get_source simply return the target
            return pysachi.analyze(target, get_source=str, **kwargs)

        source = '''
        def foo():
            pass
        '''

        report = pysachi.run([source], analyze=analyze_string)

    Example for modules using :class:`inspect` to get source code of a module:

    .. code-block:: python

        import inspect

        def analyze_module(target, **kwargs):
            return pysachi.analyze(target, get_source=inspect.getsource, **kwargs)

        report = pysachi.run([pysachi], analyze=analyze_module)

    See also :meth:`analyze` for more informations on `get_source` parameter.

    By default, `run` returns the report processed by `render` parameter. It
    can be disabled to get the raw report as this:

    .. code-block:: python

        raw_report = pysachi.run(["/some/path/file.py"], render=None)

    :param targets: List of targets to analyze.
    :param checkers: List of checks to run on node.
    :param analyze: Custom analyze method or :meth:`analyze` (default).
    :param render: Custom render method or :meth:`render` (default).
    :returns: :class:`report.Report` rendered by `render`.
    """
    targets = targets or []

    result = report.Report(
        targets,
        [analyze(_, checkers=checkers) if analyze else report.ASTReport() for _ in targets]
    )

    return render(result) if render else result


def Run(argv):
    """Run from command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("targets", type=str, nargs="+", help="files to analyze")
    parser.add_argument("-o", "--output", type=str, help="report file")
    args = parser.parse_args(argv)

    result = run(args.targets)

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
    else:
        print(result, end='')


if __name__ == "__main__":
    Run(sys.argv[1:])
