__all__ = ["run", "walk", "analyze", "render", "load_file"]
import sys
import argparse
import ast
from . import report
from .analyzer import DefaultAnalyzer
from typing import List, Optional, Callable, Any


def walk(tree: ast.AST) -> report.ASTReport:
    """Run static code analysis over an :class:`ast.AST` node.

    :param tree: The node to analyze.
    :returns: A complete report of analysis.
    """
    return DefaultAnalyzer().visit(tree)


def load_file(filename: str) -> str:
    """Simply read content of a file.

    :param str filename: File to read.
    :returns: File's content.
    """
    with open(filename, "r"):
        return filename.read()


def analyze(
    targets: List[Any],
    *,
    load: Callable[[Any], Any] = None,
    verbose: Optional[bool] = False
) -> report.Report:
    """Run static code analysis on files.
    """
    load = load or load_file

    def _analyze(target):
        """
        Analyze a single file and report results.
        """
        with open(target, "r") as f:
            if verbose:
                print("Process", target)
            return walk(ast.parse(f.read()))

    return report.Report([_analyze(_) for _ in targets])


def render(
    report: report.Report, *, renderer=None, verbose: Optional[bool] = False
):
    """Render a report.

    Report is written to stdout is output is omitted.
    """


def run(
    targets: List[Any],
    *,
    analyze: Callable[[Any, Optional[bool]], report.Report] = analyze,
    render: Callable[[report.Report, Optional[bool]], None] = render,
    output: Optional[str] = None,
    verbose: Optional[bool] = False
):
    """Run static code analysis on multiple targets and output report to file.

    By default `targets` must be a list of files to analyze. You
    can use this function as is to output report to a specific file (omitting
    `output` parameter will output report to `sys.stdout`):

    .. code-block:: python

        pyrabbit.run(["/input/path"], output="/output/path")

    Here is an example of how to pass your own `analyze` method to
    handle `targets` of custom type. The `load` lambda is called for
    each `target` to convert it to a :obj:`str` object that will be analyzed:

    .. code-block:: python

        def analyze_string(targets, **kwargs):
            # load simply return the target
            return pyrabbit.analyze(
                targets,
                load=lambda target: target,
                **kwargs
            )

        source = '''
        def foo():
            pass
        '''

        pyrabbit.run([source], analyze=analyze_string, output="/output/path")

    Example for modules using :class:`inspect` to get source code of a module:

    .. code-block:: python

        import inspect

        def analyze_module(targets, **kwargs):
            return pyrabbit.analyze(
                targets,
                load=lambda target: inspect.getsource(target),
                **kwargs
            )

        pyrabbit.run([pyrabbit], analyze=analyze_module, output="/output/path")

    :param targets: List of targets to analyze.
    :param render: Custom analyze method or :meth:`analyze` (default).
    :param render: Custom render method or :meth:`render` (default).
    :param output: File to write report to.
    :param verbose: Verbosity level.
    """
    result = render(analyze(targets, verbose=verbose), verbose=verbose)

    if output:
        with open(output, "w") as f:
            f.write(result)
    else:
        print(result)


def Run(argv):
    """Run from command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("targets", type=str, nargs="+", help="file to analyze")
    parser.add_argument("-o", "--output", type=str, help="report file")
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true"
    )
    args = parser.parse_args(argv)

    run(args.targets, output=args.output)


if __name__ == "__main__":
    Run(sys.argv[1:])
