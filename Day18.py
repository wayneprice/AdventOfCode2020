import re



def process_expression(expression, rules) :

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

    def get_precedence(token, rules) :
        return [idx for idx, data in enumerate(rules) if token in data][0]

    output = []
    operators = []
    while tokens :
        token = tokens.pop(0)
        if token.isdigit() :
            output.append(int(token))
        elif token in ['+', '*', '('] :
            this_precedence = get_precedence(token, rules)
            while operators and operators[-1] != '(' :
                stack_precedence = get_precedence(operators[-1], rules)
                if this_precedence > stack_precedence :
                    break
                calculate(output, operators.pop())
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
        sum_no_precedence += process_expression(expression, [['+', '*'], ['(', ')']])
        sum_add_has_precedence += process_expression(expression, [['*'], ['+'], ['(', ')']])

    print(sum_no_precedence)
    print(sum_add_has_precedence)

