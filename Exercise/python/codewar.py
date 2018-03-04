def divisors(integer):
    ret = [x for x in range(2, integer // 2 + 1) if not integer % x]
    if not ret:
        return "{} is prime".format(integer)
    return ret, list(range(2, integer // 2 + 1))


# print(divisors(12))


"""
 problem:
    In this kata you are required to, given a string, replace every letter with
    its position in the alphabet. If anything in the text isn't a letter,
    ignore it and don't return it.
 example:
    a being 1, b being 2, etc.
 blueprint:
    use the built-in function( chr and ord ) in python. The ord can get the
    character`s order value, then minus the base value (96 and 64); the chr can
    check whether the charater is in the range of the order value.
"""


def alphabet_position(text: str):
    result = []

    for i in text:
        if ord(i) in range(97, 123):
            result.append(str(ord(i) - 96))
        elif ord(i) in range(65, 91):
            result.append(str(ord(i) - 64))
    return " ".join(result)

# the better code example


def alphabet_position_better(text: str):
    # firstly lowercase the text, add the order value
    result = [str(ord(i - 96)) for i in text.lower() if i.isalpha()]

    return " ".join(result)

# print(alphabet_position("z"))


"""
 problem:
    Write a function toWeirdCase (weirdcase in Ruby) that accepts a string, and
    returns the same string with all even indexed characters in each word upper
    cased, and all odd indexed characters in each word lower cased. The
    indexing just explained is zero based, so the zero-ith index is even,
    therefore that character should be upper cased.
 example:
    to_weird_case('String'); # => returns 'StRiNg'
    to_weird_case('Weird string case') # => returns 'WeIrD StRiNg CaSe'
 blueprint:
    use the built-in function upper, lower, enumarate( get the index), join

"""


def to_weird_case(string: str) -> str:
    result = []

    for word in string.split(" "):
        tem_word = []   # store the word character in every loop
        for index, _ in enumerate(word):
            if index % 2 == 0:
                tem_word.append(word[index].upper())
            else:
                tem_word.append(word[index].lower())
        result.append("".join(tem_word))

    return " ".join(result)


# print(to_weird_case("cda afajk llkj"))


"""
 problem:
    Build Tower by the following given argument:
    number of floors (integer and always greater than 0).
    Tower block is represented as *
 blueprint:
    use the format string syntax. The url:
    https://docs.python.org/3.4/library/string.html
"""


def tower_builder(n_floors):
    result = []
    length = n_floors * 2 - 1

    for i in range(0, n_floors):
        result.append('{0:{fill}{align}{length}}'.format(
            "*" * (2 * i - 1), fill=" ", align="^", length=length))

    return result


"""
 problem:
    "56 65 74 100 99 68 86 180 90" ordered by numbers weights becomes:
    "100 180 90 56 65 74 68 86 99" When two numbers have the same "weight",
    let us class them as if they were strings and not numbers: 100 is before
    180 because its "weight" (1) is less than the one of 180 (9) and 180 is
    before 90 since, having the same "weight" (9) it comes before as a string.
    All numbers in the list are positive numbers and the list can be empty
 blueprint:
    use the insertion method to scan the sorted list and update the list

"""


def check(string, value):
    # check whether the strings are inserted
    for char1, char2 in zip(string, value):
        if int(char1) > int(char2):
            return True
        elif int(char1) < int(char2):
            return False

    if len(string) >= len(value):
        return True
    else:
        return False


def insertion(array, value):
    # parameter: the value need to be updated; the array is sorted list
    for i in range(0, len(array)):
        if sum([int(x) for x in array[i]]) == sum([int(x) for x in value]):
            if check(array[i], value):
                array.insert(i, value)
                return
    array.append(value)


def order_weight(s: str):
    # parameter: s is a string with list seperated by space
    weight = s.split(" ")

    weight.sort(key=lambda x: sum([int(i) for i in x]))

    result = []
    result.append(weight[0])

    for i in range(1, len(weight)):
        insertion(result, weight[i])

    return " ".join(result)


print(order_weight("71899703 200 6 91 425 4 67407 7 96488 6 4 2 7 31064 9 7920 \
    1 34608557 27 72 18 81"))
