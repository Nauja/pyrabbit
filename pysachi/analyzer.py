__all__ = ["DefaultAnalyzer"]
import ast
from typing import List, Any
from .report import *
from .stack import Stack


class DefaultAnalyzer(ast.NodeVisitor, Stack):
    """An analyzer holds a list of checkers to run
    on the :class:`ast.AST` tree while visiting its nodes.

    A checker can be a module or class defining the same
    functions as :class:`ast.NodeVisitor` but with the instance
    of this `analyzer` for additional parameter.

    .. code-block:: python

        # ast.NodeVisitor function
        def visit_Foo(self, node):
            pass

        # checker function
        def visit_Foo(self, analyzer, node):
            pass
    """

    def __init__(self):
        super().__init__()
        self._is_root = True

    def visit(self, *args, checkers: List[Any] = None, **kwargs) -> ASTReport:
        if self._is_root:
            self._is_root = False
            self._checkers = checkers
            self._report = ASTReport()
            super().visit(*args, **kwargs)
            self._is_root = True
            return self._report
        else:
            super().visit(*args, **kwargs)

    def _visit_with_context(self, node: ast.AST, fun: str) -> None:
        """Wrap the visit of a node inside of a context.

        `fun` is the name of the function to call on checkers
        for this node.

        This is equivalent to calling `pre_fun` on all checkers
        before visiting the node and `post_fun` after; letting
        them perform operations both before and after visiting
        the node.

        The `fun` method of a checker can either return a
        context on which `__enter__` and `__exit__` will be
        called or :obj:`None` meaning that it doesn't need to
        be called after visiting the node.

        :param fun: Name of an :class:`ast.NodeVisitor` function.
        :param node: Node to visit.
        """
        ctxs = [
            getattr(_, fun)(_, self, node) for _ in self._checkers if hasattr(_, fun)
        ]
        for _ in ctxs:
            if _ and hasattr(_, "__enter__"):
                _.__enter__()
        self.generic_visit(node)
        for _ in ctxs:
            if _ and hasattr(_, "__exit__"):
                _.__exit__()

    def visit_Module(self, node):
        self._push(self._report)
        self._visit_with_context(node, "visit_Module")
        self.pop()

    def visit_ClassDef(self, node):
        report = ClassReport(node.lineno)
        self.peek.classes.append(report)

        self._push(report)
        self._visit_with_context(node, "visit_ClassDef")
        self.pop()

    def visit_FunctionDef(self, node):
        report = FunctionReport(node.lineno)
        self.peek.functions.append(report)

        self._push(report)
        self._visit_with_context(node, "visit_FunctionDef")
        self.pop()

    def visit_Call(self, node):
        self._visit_with_context(node, "visit_Call")
