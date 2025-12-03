"""Compilation Exceptions.
You pass a source position to these kind of exceptions"""

from .tokens import SourcePosition


class CompilerError(Exception):
    def __init__(self, positions: list[SourcePosition] | SourcePosition, msg: str):
        self.msg = ...
        super().__init__(msg)


__all__ = ["CompilerError"]
