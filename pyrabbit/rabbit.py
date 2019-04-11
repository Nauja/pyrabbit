import sys
import argparse
import ast
from functools import reduce
from .rules import function

MAX_CALLS = 5


def percent(v):
    return int(v * 100.0)


class Stack:

    def __init__(self):
        self.__inner = []
        self.__depth = -1

    def push(self, e):
        self.__inner.append(e)
        self.__depth += 1

    def pop(self):
        e = self.__inner[self.__depth]
        del self.__inner[self.__depth]
        self.__depth -= 1
        return e

    @property
    def peek(self):
        return self.__inner[self.__depth]

    def __len__(self):
        return len(self.__inner)


class Analyzer(ast.NodeVisitor):

    def __init__(self):
        self.stack = Stack()

    def visit_ClassDef(self, node):
        self.stack.push({
            "type": "class",
            "functions": []
        })
        self.generic_visit(node)
        infos = self.stack.pop()
        entropy = reduce(lambda x, y: x * y, infos["functions"])
        print("class", node.name)
        print(len(infos["functions"]), "functions")
        print("{}% entropy".format(percent(entropy)))
        print()

    def visit_FunctionDef(self, node):
        self.stack.push({
            "type": "func",
            "calls": 0
        })
        self.generic_visit(node)
        infos = self.stack.pop()
        entropy = function.responsibilities(infos["calls"], MAX_CALLS)
        print("function", node.name)
        print(infos["calls"], "calls")
        print("{}% entropy".format(percent(entropy)))
        print()

        if len(self.stack) and self.stack.peek["type"] == "class":
            self.stack.peek["functions"].append(entropy)

    def visit_Call(self, node):
        if self.stack:
            self.stack.peek["calls"] += 1
        self.generic_visit(node)


def analyze(source):
    tree = ast.parse(source)
    analyzer = Analyzer()
    analyzer.visit(tree)


def run(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=str, help="file to analyze")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args(argv)

    with open(args.target, "r") as f:
        analyze(f.read())


if __name__ == '__main__':
    run(sys.argv[1:])
