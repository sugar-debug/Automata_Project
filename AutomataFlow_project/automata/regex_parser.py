"""Regex tokenizer, explicit concatenation insertion, and postfix conversion."""

EPSILON = "ε"
CONCAT = "·"
OPERATORS = {"|", CONCAT, "*", "+" , "?"}
PRECEDENCE = {"|": 1, CONCAT: 2}

def tokenize(regex: str):
    """Tokenize supported regex: symbols, (), |, *, +, ?, and escapes."""
    if not isinstance(regex, str) or not regex.strip():
        raise ValueError("Please enter a regular expression.")
    tokens = []
    i = 0
    while i < len(regex):
        ch = regex[i]
        if ch.isspace():
            i += 1
            continue
        if ch == "\\":
            i += 1
            if i >= len(regex):
                raise ValueError("A backslash must escape a following character.")
            tokens.append(("LITERAL", regex[i]))
        elif ch in "()|*+?":
            tokens.append((ch, ch))
        elif ch == "ε":
            tokens.append(("EPSILON", ch))
        else:
            tokens.append(("LITERAL", ch))
        i += 1
    return tokens


def add_concatenation(tokens):
    """Insert explicit concatenation dots between adjacent expression units."""
    result = []
    can_end = {"LITERAL", "EPSILON", ")", "*", "+", "?"}
    can_start = {"LITERAL", "EPSILON", "("}
    for idx, token in enumerate(tokens):
        if idx:
            prev = tokens[idx - 1]
            if prev[0] in can_end and token[0] in can_start:
                result.append((CONCAT, CONCAT))
        result.append(token)
    return result


def to_postfix(regex: str):
    """Convert regex to postfix (Reverse Polish) notation via shunting-yard."""
    tokens = add_concatenation(tokenize(regex))
    output = []
    stack = []
    for kind, value in tokens:
        if kind in {"LITERAL", "EPSILON"}:
            output.append(value)
        elif kind == "(":
            stack.append(kind)
        elif kind == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise ValueError("Mismatched parentheses: missing '('")
            stack.pop()
        elif kind in OPERATORS:
            if kind in {"*", "+", "?"}:
                # Postfix unary operators are emitted directly.
                output.append(kind)
            else:
                while stack and stack[-1] != "(" and PRECEDENCE.get(stack[-1], 0) >= PRECEDENCE[kind]:
                    output.append(stack.pop())
                stack.append(kind)
        else:
            raise ValueError(f"Unsupported token: {value}")
    while stack:
        op = stack.pop()
        if op == "(":
            raise ValueError("Mismatched parentheses: missing ')'")
        output.append(op)

    # Basic expression-shape validation is performed by the NFA builder too.
    if not output:
        raise ValueError("Regular expression is empty.")
    return output
