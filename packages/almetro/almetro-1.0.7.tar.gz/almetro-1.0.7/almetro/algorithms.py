import math


def loop_n(instance=[]):
    n = len(instance)
    j = 0
    for _ in range(n):
        j += 1
    return j


def loop_n_quadratic(instance=[]):
    n = len(instance)
    j = 0
    for _ in range(n):
        for _ in range(n):
            j += 1
    return j


def loop_n_cubic(instance=[]):
    n = len(instance)
    j = 0
    for _ in range(n):
        for _ in range(n):
            for _ in range(n):
                j += 1
    return j


def loop_n_log(instance=[]):
    n = len(instance)
    log_n = math.ceil(math.log2(n))
    j = 0
    for _ in range(log_n):
        j += 1
    return j


def loop_n_log_n(instance=[]):
    n = len(instance)
    log_n = math.ceil(math.log2(n))
    j = 0
    for _ in range(n * log_n):
        j += 1
    return j
