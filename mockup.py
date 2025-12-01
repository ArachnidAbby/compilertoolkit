from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable, Generator, Self, Type


class SourcePosition:
    """Source position of a token"""

    def __add__(self, other: Self) -> Self: ...


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


class TokenPattern:
    """A way to match an individual token"""


class ParsingPattern:
    """Matching multiple tokens, acts similarly to a namedtuple"""

    __slots__ = "_children"

    # class attributes
    _PATTERNS: dict[str, TokenPattern]

    # instance variables
    _children: dict[str, TokenEnum]

    def __init_subclass__(cls) -> None:
        pass

    def __iter__(self) -> Generator[TokenEnum]:
        yield from self._children.values()

    def set_parents(self, parent: "AbstractAstNode"):
        for child in self._children.values():
            if isinstance(child, AbstractAstNode):
                child.value.set_parent(parent)


class AbstractAstNode[T: ParsingPattern](ABC):
    __slots__ = ("_tokens", "parent")

    # Subclasses
    ParserPattern: Type[T] | list[Type[ParsingPattern]]

    # instance variables
    parent: Self

    def __init__(self, tokens: T):
        self._tokens = tokens
        self._tokens.set_parents(self)

    def set_parent(self, parent: Self):
        self.parent = parent

    def walk[S](self, func: Callable[[Self], S]) -> list[S]:
        """Walk the syntax tree and run a function"""
        return [
            func(self),
            *(
                item
                for token in self._tokens
                if isinstance(token.value, AbstractAstNode)
                for item in token.value.walk(func)
                if item is not None
            ),
        ]

    def collect[S](self, typ: Type[S]) -> list[S]:
        '''Walk the syntax tree and collect all instances of "typ"'''
        output = [self] if isinstance(self, typ) else []
        return output + [
            item
            for token in self._tokens
            if isinstance(token.value, AbstractAstNode)
            for item in token.value.collect(typ)
        ]

    @property
    def position(self):
        return sum((token for token in self._tokens))


def abstractcompilationstep(order: int):
    """An abstract version of @compilation step"""

    def decorator(func):
        @wraps
        @abstractmethod
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


def compilationstep[T](func: T) -> T:
    func.__is_compilationstep__ = True
    return func


# How the user defines stuff (Example)


class Token[T](TokenEnum[T]):
    """Part of our own Stuff"""

    Comma: TokenType[str] = TokenType(pattern=r"\,")
    Keyword: TokenType[str] = TokenType(pattern=r"\d+")
    Number: TokenType[str] = TokenType(pattern=r"\w+")

    Expression: TokenType["ExpressionNode"] = TokenType()
    Statement: TokenType["AstNode"] = TokenType()


class AstNode(AbstractAstNode):
    """Basic Ast Node"""

    __slots__ = ()

    @abstractcompilationstep(0)
    def analyze_types(self, ctx):
        pass

    @abstractcompilationstep(1)
    def compile(self, ctx) -> Any:
        pass


class ExpressionNode(AstNode):
    """Basic Ast Node"""

    __slots__ = "return_type"

    # instance variables
    return_type: None  # Your own type class


class NumberLiteral(ExpressionNode):
    """Basic Ast Node"""

    __slots__ = "value"

    class ParserPattern(ParsingPattern):
        value = TokenHasType(Token.Number)

    # instance variables
    value: int

    def __init__(self, tokens: ParserPattern):
        super().__init__(tokens)
        self.value = int(tokens.value.value)

    @compilationstep
    def analyze_types(self, ctx):
        self.return_type = int

    @compilationstep
    def compile(self, ctx):
        return self.value


class SumNode(ExpressionNode):
    """Basic Ast Node"""

    __slots__ = ("lhs", "rhs")

    class ParserPattern(ParsingPattern, precedence=1):
        lhs = TokenHasType(Token.Expression)
        operation = TokenHasType(Token.Plus)
        # Parses, then checks for the specified case, errors if the value of the token is unparsed
        rhs = ParseThenCheck(TokenHasType(Token.Expression))

    # instance variables
    lhs: ExpressionNode
    rhs: ExpressionNode

    def __init__(self, tokens: ParserPattern):
        super().__init__(tokens)
        self.rhs = tokens.lhs.value
        self.lhs = tokens.lhs.value

    @compilationstep
    def analyze_types(self, ctx):
        self.lhs.analyze_types(ctx)
        self.rhs.analyze_types(ctx)
        self.return_type = int

    @compilationstep
    def compile(self, ctx):
        return self.lhs.compile(ctx) + self.rhs.compile(ctx)
