def division(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        raise ValueError("Parameter b darf nicht 0 sein") from None

x = division(7, 3)
y = division(5, 0)

print(x + y)