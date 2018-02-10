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
