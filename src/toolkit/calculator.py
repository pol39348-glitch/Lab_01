from .errors import (
    EmptyExpressionError, InvalidCharacterError, MissingOperandError,
    DivisionByZeroError, InvalidNumericValueError
)


def tokenize(expr: str) -> list:
    expr = expr.replace(' ', '')
    if not expr:
        raise EmptyExpressionError()

    tokens = []
    i = 0
    n = len(expr)

    while i < n:
        char = expr[i]
        if char.isdigit() or char == '.':
            start = i
            has_dot = (char == '.')
            i += 1
            while i < n and (expr[i].isdigit() or expr[i] == '.'):
                if expr[i] == '.':
                    if has_dot:
                        raise InvalidCharacterError("Несколько точек в числе")
                    has_dot = True
                i += 1
            tokens.append(('NUM', expr[start:i]))
        elif char in '+-*/()':
            if char in '+-':
                is_unary = (not tokens or tokens[-1][0] == 'OP' or tokens[-1][1] == '(')
                if is_unary:
                    i += 1
                    if i >= n or not (expr[i].isdigit() or expr[i] == '.'):
                        raise MissingOperandError("Пропущен операнд после унарного оператора")
                    start = i
                    has_dot = (expr[i] == '.')
                    i += 1
                    while i < n and (expr[i].isdigit() or expr[i] == '.'):
                        if expr[i] == '.':
                            if has_dot:
                                raise InvalidCharacterError("Несколько точек в числе")
                            has_dot = True
                        i += 1
                    tokens.append(('NUM', char + expr[start:i]))
                    continue
            tokens.append(('OP', char))
            i += 1
        else:
            raise InvalidCharacterError(f"Недопустимый символ: {char}")

    return tokens


def validate(tokens: list) -> None:
    if not tokens:
        raise EmptyExpressionError()

    for i in range(len(tokens)):
        type_, val = tokens[i]

        if i == 0 and type_ == 'OP' and val != '(':
            raise MissingOperandError("Пропущен операнд в начале выражения")

        if i == len(tokens) - 1 and type_ == 'OP' and val != ')':
            raise MissingOperandError("Пропущен операнд в конце выражения")

        if i < len(tokens) - 1:
            next_type, next_val = tokens[i + 1]
            if type_ == 'OP' and next_type == 'OP':
                if val == '(' or next_val == ')':
                    continue
                raise MissingOperandError("Два бинарных оператора подряд")


def calculate(expr: str) -> float:
    tokens = tokenize(expr)
    validate(tokens)

    output = []
    operators = []
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    for type_, val in tokens:
        if type_ == 'NUM':
            try:
                output.append(float(val))
            except ValueError:
                raise InvalidNumericValueError(f"Неверное числовое значение: {val}")
        elif val == '(':
            operators.append(val)
        elif val == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if not operators:
                raise MissingOperandError("Несовпадение скобок")
            operators.pop()
        elif type_ == 'OP':
            while (operators and operators[-1] != '(' and
                   operators[-1] in precedence and
                   precedence[operators[-1]] >= precedence[val]):
                output.append(operators.pop())
            operators.append(val)

    while operators:
        op = operators.pop()
        if op in '()':
            raise MissingOperandError("Несовпадение скобок")
        output.append(op)

    stack = []
    for token in output:
        if isinstance(token, float):
            stack.append(token)
        else:
            if len(stack) < 2:
                raise MissingOperandError("Недостаточно операндов")
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise DivisionByZeroError("Деление на ноль")
                stack.append(a / b)

    if len(stack) != 1:
        raise MissingOperandError("Некорректное выражение")

    return stack[0]