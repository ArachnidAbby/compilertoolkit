from abc import ABC
from typing import TYPE_CHECKING, Generator

from compilertoolkit.tokens import TokenEnum


if TYPE_CHECKING:
    from compilertoolkit.ast import AbstractAstNode


class TokenPattern(ABC):
    """A way to match an individual token"""

    __slots__ = "idx"

    idx: int
    """Index of the token in a parser pattern"""

    def __init__(self):
        self.idx = 0

    def __set_name__(self, name, owner):
        owner._IDX += 1

    def __get__(self, inst, owner):
        if inst is None:
            return self
        return inst._children[self.idx]

    def __set__(self, value, inst):
        inst._children[self.idx] = value


class ParsingPattern:
    """Matching multiple tokens, acts similarly to a namedtuple"""

    __slots__ = "_children"

    # class attributes
    _PATTERNS: dict[str, TokenPattern]
    _IDX = 0

    # instance variables
    _children: list[TokenEnum]

    def __init_subclass__(cls) -> None:
        cls._IDX = 0  # reset this tracking variable
        cls._PATTERNS = {
            name: value
            for name, value in cls.__dict__.items()
            if isinstance(value, TokenPattern)
        }

    def __init__(self, items: list[TokenEnum]):
        self._children = items

    def __iter__(self) -> Generator[TokenEnum, None, None]:
        yield from self._children

    def set_parents(self, parent: "AbstractAstNode"):
        for child in self._children:
            if isinstance(child, AbstractAstNode):
                child.value.set_parent(parent)


__all__ = ["ParsingPattern", "TokenPattern"]
