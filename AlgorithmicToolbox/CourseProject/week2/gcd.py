#!/usr/bin/python
# -*-coding: utf-8 -*-

import sys


def gcd(a, b):
    print(a, b)
    if b == 0:
        return a
    elif a > b:
        x = b
        y = a % b
    else:
        x = a
        y = b % a

    return gcd(x, y)


if __name__ == "__main__":
    # input_data = sys.stdin.read()
    input_data = input("Enter the numbers splited by ',':")
    a, b = map(int, input_data.split(","))
    print(gcd(a, b))
