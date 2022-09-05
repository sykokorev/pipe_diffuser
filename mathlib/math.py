def factorial(n: int) -> int:
    if n == 0:
        return 1
    elif n < 0:
        return -1
    else:
        return n * factorial(n - 1)


def linspace(n1: float, n2: float, np: int) -> list:
    delta = (n2 - n1) / (np - 1)
    return [n1 + i * delta for i in range(np)]


def arange(start: float=0.0, stop: float=1.0, step: float=0.1):
    np = round((stop - start) / step)
    return [start + i * step for i in range(np)]


def span(p: float, lst: list) -> int:
    
    for i, elm in enumerate(lst[:-1]):
        if elm <= p <= lst[i+1]:
            return int(i)
    
    return int(-1)
