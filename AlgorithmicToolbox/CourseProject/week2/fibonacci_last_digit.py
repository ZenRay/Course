#!/usr/bin/python
# -*- coding: utf-8 -*-


def get_fibonacci_last_digit(n):
    # result_list = [0, 1, 1, 2, 3, 5, 8]
    if n <= 1:
        return n

    previous, current = 0, 1

    for i in range(2, n + 1):
        previous, current = current, (previous + current) % 10
    return current


if __name__ == "__main__":
    import time

    t1 = time.time()
    print(get_fibonacci_last_digit(331))
    print("The cost time is %f" % (time.time() - t1))
