"""Checker for functions related rules """
from functools import reduce
from ..rules import function
from ..report import *

MAX_CALLS = 5


def percent(v):
    return int(v * 100.0)


def r1001(node, *, fun, calls, entropy):
    """Check: Function has too many responsibilities.

    """
    print(
        "{}:{}@R1001:{}:{}:{}".format(node.lineno, node.col_offset, fun, calls, entropy)
    )


def visit_ClassDef(self, analyzer, node):
    class Context:
        def __enter__(self):
            return self

        def __exit__(self):
            pass

    return Context()


def visit_FunctionDef(self, analyzer, node):
    class Context:
        def __enter__(self):
            return self

        def __exit__(self):
            report = analyzer.peek
            report.checks.append(
                CheckReport(
                    ERule.R1001,
                    value=function.responsibilities(report.calls, MAX_CALLS),
                    goal=1,
                    extra={"calls": report.calls, "max": MAX_CALLS},
                )
            )

    return Context()


def visit_Call(self, analyzer, node):
    analyzer.peek.calls += 1
