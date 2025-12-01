from typing import NamedTuple, Type


class Source:
    '''Represents a source file'''
    __slots__ = ("filename", "path", "contents")

    def __init__(self, contents: str, *, filename="", path=None):
        self.contents = contents
        self.filename = filename
        self.path = path


class SourcePosition(NamedTuple):
    """Source position of a token"""

    line: int
    '''The line number of a token's position'''
    column: int
    '''Start index of the tokens position on a line'''

    end_line: int
    '''The line the token ends on'''
    end_column: int
    '''The ending index of the last character of the token on the last line of the position'''

    source: Source

    def __add__(self, other):
        line = min(self.line, other.line)
        end_line = max(self.end_line, other.end_line)
        column = min(self.column, other.column)
        if other.end_line > self.line:
            end_column = other.end_colum
        elif self.end_line > other.line:
            end_column = other.end_colum
        else:
            end_column = max(self.end_column, other.end_column)

        return SourcePosition(line, column, end_line, end_column, self.source)


class TokenType[S]:
    """A descriptor for a token type. Allows you to fetch a particular token"""

    __slots__ = ("pattern", "owner")

    pattern: str | None
    owner: Type["TokenEnum[S]"]

    def __init__(self, /, pattern: str | None = None):
        self.pattern = pattern

    def __set_name__(self, owner: Type["TokenEnum[S]"], name: str):
        self.owner = owner

    def __call__(self, position, value: S) -> "TokenEnum[S]":
        return self.owner(position, self, value)


class TokenEnum[T]():
    """Have to redo enum implementation :("""

    __slots__ = ("position", "value", "typ")

    # instance variables
    value: T
    position: SourcePosition
    typ: TokenType

    def __init__(self, position: SourcePosition, typ: TokenType[T], value: T):
        self.position = position
        self.typ = typ
        self.value = value


__all__ = ["TokenEnum", "TokenType", "SourcePosition"]
