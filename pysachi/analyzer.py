__all__ = ["DefaultAnalyzer"]
import ast
from .rules import function
from functools import reduce

MAX_CALLS = 5


def percent(v):
    return int(v * 100.0)


def r1001(node, *, fun, calls, entropy):
    """Check: Function has too many responsibilities.

    """
    print(
        "{}:{}@R1001:{}:{}:{}".format(node.lineno, node.col_offset, fun, calls, entropy)
    )


class DefaultAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.stack = []

    def __call__(self, target):
        pass

    @property
    def _depth(self):
        return len(self.stack)

    @property
    def _peek(self):
        return self.stack[self._depth - 1] if self._depth > 0 else None

    def visit_ClassDef(self, node):
        self.stack.append({"type": "class", "functions": []})
        self.generic_visit(node)
        infos = self.stack.pop()
        entropy = reduce(lambda x, y: x * y, infos["functions"])
        print("class", node.name)
        print(len(infos["functions"]), "functions")
        print("{}% entropy".format(percent(entropy)))
        print()

    def visit_FunctionDef(self, node):
        self.stack.append({"type": "func", "calls": 0})
        self.generic_visit(node)
        infos = self.stack.pop()
        entropy = function.responsibilities(infos["calls"], MAX_CALLS)
        r1001(node, fun=node.name, calls=infos["calls"], entropy=entropy)

        if len(self.stack) and self._peek["type"] == "class":
            self._peek["functions"].append(entropy)

    def visit_Call(self, node):
        if self.stack:
            self._peek["calls"] += 1
        self.generic_visit(node)
