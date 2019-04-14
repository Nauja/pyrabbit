__all__ = ["NodeReport", "ASTReport", "FileReport", "Report"]
from typing import List


class NodeReport:
    pass


class ASTReport:
    pass


class FileReport:
    pass


class Report:
    def __init__(self, files: List[FileReport]):
        self.files = files
