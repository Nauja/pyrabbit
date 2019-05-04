__all__ = ["run", "walk", "analyze", "render", "get_checkers"]
import sys
import argparse
import ast
from . import report
from . import checkers
from .analyzer import DefaultAnalyzer
from typing import List, Optional, Callable, Any
import json


def get_checkers() -> List[Any]:
    """Get default checkers to run on code.

    :returns: List of default checkers to run.
    """
    return [checkers.function, checkers.readability]


def walk(tree: ast.AST, *, checkers: Optional[List[Any]] = None) -> report.ASTReport:
    """Run static code analysis over an :class:`ast.AST` node.

    :param tree: The node to analyze.
    :param checkers: List of checks to run on node.
    :returns: A complete report of analysis.
    """
    analyzer = DefaultAnalyzer(checkers)
    analyzer.visit(tree)
    return analyzer.report


def _read_file(filename: str) -> str:
    """Simply read content of a file.

    :param filename: File to read.
    :returns: File's content.
    """
    with open(filename, "r") as f:
        return f.read()


def analyze(
    targets: List[Any],
    *,
    load: Callable[[Any, Optional[bool]], Any] = None,
    checkers: Optional[List[Any]] = None
) -> report.Report:
    """Run static code analysis on multiple target.

    By default `targets` is expected to be a list of files to analyze.
    You can use this function as is to create a report from a file:

    .. code-block:: python

        report = pysachi.analyze(["/some/path"])

    You can pass your own `load` callable for targets of custom type.
    Here is the signature of this callable alongside with an example of using it
    to return source code of a module:

    .. code-block:: python

        import inspect

        def get_module_sources(target):
            return inspect.getsource(target)

        report = pysachi.analyze([pysachi], load=get_module_sources)

    :param targets: List of targets to analyze.
    :param load: A callable to convert targets to :obj:`str`.
    :param checkers: List of checks to run on node.
    :returns: Complete report of static code analysis.
    """
    load = load or _read_file

    def _analyze(target: Any) -> report.ASTReport:
        """
        Convert target to :class:`ast.AST` and run analysis.
        """
        tree = ast.parse(load(target))
        return walk(tree, checkers=checkers)

    return report.Report(
        targets,
        [_analyze(_) for _ in targets]
    )


def render(report: report.Report, *, renderer=None):
    """Render a report.

    Report is written to stdout is output is omitted.
    """
    return json.dumps(report)


def run(
    targets: List[Any],
    *,
    checkers: Optional[List[Any]] = None,
    analyze: Callable[[Any, Optional[bool]], report.Report] = analyze,
    render: Callable[[report.Report, Optional[bool]], None] = render,
    output: Optional[str] = None
):
    """Run static code analysis on multiple targets and output report to file.

    By default `targets` must be a list of files to analyze. You
    can use this function as is to output report to a specific file (omitting
    `output` parameter will output report to `sys.stdout`):

    .. code-block:: python

        pysachi.run(["/input/path"], output="/output/path")

    Here is an example of how to pass your own `analyze` method to
    handle `targets` of custom type. The `load` lambda is called for
    each `target` to convert it to a :obj:`str` object that will be analyzed:

    .. code-block:: python

        def analyze_string(targets, **kwargs):
            # load simply return the target
            return pysachi.analyze(
                targets,
                load=lambda target: target,
                **kwargs
            )

        source = '''
        def foo():
            pass
        '''

        pysachi.run([source], analyze=analyze_string, output="/output/path")

    Example for modules using :class:`inspect` to get source code of a module:

    .. code-block:: python

        import inspect

        def analyze_module(targets, **kwargs):
            return pysachi.analyze(
                targets,
                load=lambda target: inspect.getsource(target),
                **kwargs
            )

        pysachi.run([pysachi], analyze=analyze_module, output="/output/path")

    See also :meth:`analyze` for more informations on `load` parameter.

    :param targets: List of targets to analyze.
    :param checkers: List of checks to run on node.
    :param render: Custom analyze method or :meth:`analyze` (default).
    :param render: Custom render method or :meth:`render` (default).
    :param output: File to write report to.
    """
    checkers = checkers or get_checkers()

    result = render(
        analyze(targets, checkers=checkers)
    )

    if output:
        with open(output, "w") as f:
            f.write(result)
    else:
        print(result, end='')


def Run(argv):
    """Run from command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("targets", type=str, nargs="+", help="files to analyze")
    parser.add_argument("-o", "--output", type=str, help="report file")
    args = parser.parse_args(argv)

    run(args.targets, output=args.output)


if __name__ == "__main__":
    Run(sys.argv[1:])
