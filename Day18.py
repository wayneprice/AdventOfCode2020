import re



def process_expression(expression, add_has_precedence) :

    # Split expression into tokens
    tokens = re.findall('([+*\(\)]|[0-9]+) *', expression)

    # Helper function - apply operator to top values on stack
    def calculate(output, operator) :
        if operator == '+' :
            output.append(output.pop() + output.pop())
        elif operator == '*':
            output.append(output.pop() * output.pop())
        else :
            raise RuntimeError('unexpected operator')

    output = []
    operators = []
    while tokens :
        token = tokens.pop(0)
        if token.isdigit() :
            output.append(int(token))
        elif token in ['+', '*'] :
            if operators and operators[-1] != '(' and (not add_has_precedence or not (token == '+' and operators[-1] == '*')) :
                calculate(output, operators.pop())
            operators.append(token)
        elif token == '(' :
            operators.append(token)
        elif token == ')' :
            while operators :
                operator = operators.pop()
                if operator == '(' :
                    break
                calculate(output, operator)

    while operators :
        calculate(output, operators.pop())

    return output.pop()



with open('data/input-day18.txt', 'r') as fp :
    sum_no_precedence = 0
    sum_add_has_precedence = 0
    for expression in fp :
        sum_no_precedence += process_expression(expression, False)
        sum_add_has_precedence += process_expression(expression, True)

    print(sum_no_precedence)
    print(sum_add_has_precedence)

