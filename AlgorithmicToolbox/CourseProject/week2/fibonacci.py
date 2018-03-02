#!/usr/bin/python
# -*- coding: utf-8 -*-


import time
result_list = [0, 1]


def fibonacci(n):
    global result_list
    if n <= 1:
        return result_list[n]
    else:
        for i in range(2, n + 1):
            result_list.append(result_list[i - 1] + result_list[i - 2])
    return result_list[n]


if __name__ == "__main__":
    fibonacci_index = int(input("Enter your fibonacci index:"))
    t1 = time.time()
    print("At the %d, the fibonacci number is " % fibonacci_index)
    print(fibonacci(fibonacci_index))
    print("The cost time is %f" % (t1 - time.time()))
