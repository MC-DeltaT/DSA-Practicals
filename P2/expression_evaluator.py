#from dsa_circular_queue import DSACircularQueue
from dsa_queue import DSAQueue
from dsa_shuffling_queue import DSAShufflingQueue
from dsa_stack import DSAStack

from operator import add, mul, sub, truediv
import re
import sys
from typing import Callable, List, Sequence, Union


queue_type = DSAShufflingQueue


class Number:
    def __init__(self, value: Union[int, float] = 0) -> None:
        self.value = value

    def __repr__(self) -> str:
        return repr(self.value)


class Token:
    # source: the string the token came from.
    # start_pos: the index in source of the first character in this token.
    # end_pos: the index in source of the last character in this token, + 1.
    def __init__(self, source: str, start_pos: int, end_pos: int) -> None:
        if start_pos < 0:
            raise ValueError("start_pos must be >= 0.")
        if end_pos < start_pos:
            raise ValueError("start_pos must be <= end_pos.")
        self.source = source
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.string = source[start_pos:end_pos]

    def __repr__(self) -> str:
        return self.string


class StartOfTokens(Token):
    description = "start of string"


class EndOfTokens(Token):
    description = "end of string"


class NumericLiteral(Token, Number):
    description = "number"


class IntegerLiteral(NumericLiteral):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.value = int(self.string)


class FloatLiteral(NumericLiteral):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.value = float(self.string)


class Operator(Token):
    description = "operator"


class OpenParenthesis(Token):
    description = "opening parenthesis"


class CloseParenthesis(Token):
    description = "closing parenthesis"


class OperatorInfo:
    def __init__(self, precedence: int,
            function: Callable[[Number, Number], Number]) -> None:
        self.precedence = precedence
        self.function = function


class InvalidExpression(Exception):
    def __init__(self, pos: int, message: str):
        self.pos = pos
        self.message = message

    def __str__(self):
        return "At position {}: {}".format(self.pos, self.message)


# A list of regexes defining the allowed tokens, and their associated classes.
token_regexes = [
    # Opening parenthesis.
    (r"\(", OpenParenthesis),

    # Closing parenthesis.
    (r"\)", CloseParenthesis),

    # Floating point literal. Matches an integer (as below) followed by ".",
    # followed by 1 or more digits.
    # Must be tried before the integer regex, otherwise that will always match
    # first.
    (r"(?:(?:\-?(?:[1-9]\d+|\d))\.\d+)", FloatLiteral),

    # Integer literal. Matches an optional minus sign, followed by a single
    # digit or non-zero digit, followed by 1 or more digit.
    (r"(?:\-?(?:[1-9]\d+|\d))", IntegerLiteral),

    # Binary operator. Matches any of "+", "-", "*", "/".
    # Must be tried after numeric literal regex, otherwise the minus sign will
    # always match as an operator.
    (r"(?:[\+\-\*/])", Operator)
]


# A sequence of 2 consecutive tokens must be one of these to be valid.
valid_sequences = [
    (StartOfTokens, EndOfTokens),
    (StartOfTokens, NumericLiteral),
    (StartOfTokens, OpenParenthesis),
    (NumericLiteral, Operator),
    (NumericLiteral, CloseParenthesis),
    (NumericLiteral, EndOfTokens),
    (Operator, NumericLiteral),
    (Operator, OpenParenthesis),
    (OpenParenthesis, OpenParenthesis),
    (OpenParenthesis, NumericLiteral),
    (CloseParenthesis, Operator),
    (CloseParenthesis, CloseParenthesis),
    (CloseParenthesis, EndOfTokens),
]


# Maps operator strings to their precedence and function.
operator_info = {
    "*": OperatorInfo(1, mul),
    "/": OperatorInfo(1, truediv),
    "+": OperatorInfo(0, add),
    "-": OperatorInfo(0, sub)
}


def evaluate(expression: str) -> Union[int, float]:
    tokens = _parse_tokens(expression)
    _check_syntax(tokens)
    postfix = _infix_to_postfix(tokens)
    #print(postfix)
    result = _evaluate_postfix(postfix)
    return result.value


def _parse_tokens(expression: str) -> List[Token]:
    tokens = []
    tokens.append(StartOfTokens(expression, 0, 0))
    i = 0
    while i < len(expression):
        if expression[i].isspace():
            i += 1
        else:
            matched = False
            j = 0
            while not matched and j < len(token_regexes):
                regex, cls = token_regexes[j]
                match = re.match(regex, expression[i:])
                if match:
                    start_pos = i + match.start()
                    end_pos = i + match.end()
                    token = cls(expression, start_pos, end_pos)
                    tokens.append(token)
                    matched = True
                    i = end_pos
                j += 1
            if not matched:
                raise InvalidExpression(i, "Invalid token.")
    tokens.append(EndOfTokens(expression, len(expression), len(expression)))
    return tokens


def _check_syntax(tokens: Sequence[Token]) -> None:
    assert len(tokens) >= 2
    prev_token = tokens[0]
    for token in tokens[1:]:
        if not _is_token_allowed(prev_token, token):
            raise InvalidExpression(token.start_pos,
                "Unexpected {} after {}."
                    .format(token.description, prev_token.description))
        prev_token = token


def _infix_to_postfix(tokens: Sequence[Token]) -> DSAQueue:
    postfix = queue_type(len(tokens))
    operators = DSAStack(len(tokens))
    assert len(tokens) >= 2
    for token in tokens[1:-1]:
        if isinstance(token, OpenParenthesis):
            operators.push(token)

        elif isinstance(token, CloseParenthesis):
            try:
                while not isinstance(operators.top(), OpenParenthesis):
                    postfix.enqueue(operators.pop())
            except ValueError:
                raise InvalidExpression(
                    token.start_pos, "Unmatched closing parenthesis.")
            operators.pop()

        elif isinstance(token, Operator):
            while not operators.is_empty() \
                    and not isinstance(operators.top(), OpenParenthesis) \
                    and _operator_precedence(operators.top()) >= _operator_precedence(token):
                postfix.enqueue(operators.pop())
            operators.push(token)

        elif isinstance(token, NumericLiteral):
            postfix.enqueue(token)

        else:
            raise AssertionError(
                "Didn't expect type `{}`.".format(type(token)))

    while not operators.is_empty():
        token = operators.pop()
        if isinstance(token, OpenParenthesis):
            raise InvalidExpression(
                token.start_pos, "Unmatched opening parethesis.")
        postfix.enqueue(token)

    return postfix


# Checks if the occurence of token directly after prev_token is valid.
def _is_token_allowed(prev_token: Token, token: Token) -> bool:
    # Set of token types that are allowed to occur after the previous token.
    allowed = map(lambda t: t[1],
                filter(lambda t: isinstance(prev_token, t[0]),
                    valid_sequences))
    return any(map(lambda cls: isinstance(token, cls), allowed))


def _operator_precedence(token: Operator) -> int:
    assert token.string in operator_info
    return operator_info[token.string].precedence


def _evaluate_operator(op: Operator, lhs: Number, rhs: Number) -> Number:
    assert op.string in operator_info
    return Number(operator_info[op.string].function(lhs.value, rhs.value))


def _evaluate_postfix(postfix: DSAQueue) -> Number:
    operands = DSAStack(postfix.get_size())
    while not postfix.is_empty():
        token = postfix.dequeue()
        if isinstance(token, Operator):
            assert operands.get_size() >= 2
            rhs = operands.pop()
            lhs = operands.pop()
            result = _evaluate_operator(token, lhs, rhs)
            operands.push(result)
        elif isinstance(token, Number):
            operands.push(token)
        else:
            raise AssertionError(
                "Didn't expect type `{}`.".format(type(token)))
    assert operands.get_size() == 1
    assert isinstance(operands.top(), Number)
    return operands.pop()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python {} "expression"'.format(sys.argv[0]))
    else:
        expression = sys.argv[1]
        print("Evaluating {}".format(expression))
        try:
            result = evaluate(expression)
        except InvalidExpression as e:
            print("Error - invalid expression:")
            print(e)
        else:
            print(result)
