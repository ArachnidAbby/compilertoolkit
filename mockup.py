from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable, Generator, Self, Type



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
