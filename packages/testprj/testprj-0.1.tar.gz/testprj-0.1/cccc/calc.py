
def add(x, y):
    """
    Add two integers.
    :param x: first integer
    :param y: second integer
    :return: result of the addition
    """
    return x + y


def sub(x, y):
    """
    Substract two integers
    :param x: first integer
    :param y: second interger
    :return: result of the operation
    """
    return x - y


def mult(x, y):
    """
    Multiply two intergers together
    :param x: first interger
    :param y: second integer
    :return: the result of the arithmetic operation
    """
    return x * y


def div(x, y):
    if y != 0:
        return x / y

    else:
        return None


if __name__ == '__main__':
    a = 7
    b = 13
    res = mult(a, b)
    print(res)
