def calculation(a,b,operator):
    operators = {'+': lambda x, y: x + y, 
                '-': lambda x, y: x - y,
                '*': lambda x, y: x * y,
                '/': lambda x, y: x / y}

    result = operators[operator](a,b)
    return result