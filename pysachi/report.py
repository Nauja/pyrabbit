__all__ = [
    "ERule",
    "CheckReport",
    "Report",
    "ASTReport",
    "ClassReport",
    "FunctionReport",
]
from enum import IntEnum
from typing import List, Dict, Any
from abc import ABC


class ERule(IntEnum):
    R1001 = 1
    R1002 = 2


class DictObj(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


class _BaseReport(ABC, DictObj):
    def __init__(self):
        self.classes: List[ClassReport] = []
        self.functions: List[FunctionReport] = []
        self.checks: List[CheckReport] = []
        self.calls = 0


class CheckReport(DictObj):
    def __init__(
        self, rule: ERule, *, value: float, goal: float, extra: Dict[str, Any] = None
    ):
        self.rule = rule
        self.value = value
        self.goal = goal
        self.extra = extra


class FunctionReport(_BaseReport):
    def __init__(self, lineno: int):
        super().__init__()
        self.lineno = lineno


class ClassReport(_BaseReport):
    def __init__(self, lineno: int):
        super().__init__()
        self.lineno = lineno


class ASTReport(_BaseReport):
    def __init__(self):
        super().__init__()


class Report(DictObj):
    def __init__(self, targets: List[Any], reports: List[ASTReport]):
        self.targets = targets
        self.reports = reports
