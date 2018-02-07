#!/usr/bin/python

if False:
    """
     problem: optimise the running time
     reason: it takes too much time, because using the for nested loop
     method: find the largest and the second largest elements, we need only two
        scans of the sequence. During the first scan, we find the largest element.
        During the second scan, we find the largest element among the remaining
        ones by skipping the element found at the previ- ous scan. So use the two
        for loop seperatly
     variables: n=>the length of the list
                a=>the splited list
    """
    n = int(input())
    a = [int(x) for x in input().split()]
    assert(len(a) == n)

    result = 0

    index_1 = 0

    for i in range(1, n):
        if a[index_1] < a[i]:
            index_1 = i

    # avoid that the index_1 at the first index is the largest number, which in the
    # second scan the index_2 is index 0 and the index_2 can`t update
    if index_1 == 0:
        index_2 = 1
    else:
        index_2 = 0

    for i in range(1, n):
        if (i != index_1) & (a[i] > a[index_2]):
            index_2 = i

    print(a[index_1] * a[index_2])

if True:
    """
     problem: optimise the running time
     reason: it takes too much time, because using the for nested loop
     method: use the buildin method about list sorted in the python
     variables: n=>the length of the list
                a=>the splited list
    """
    n = int(input())
    a = [int(x) for x in input().split()]
    assert(len(a) == n)

    sorted_a = sorted(a)

    print(sorted_a[n - 1] * sorted_a[n - 2])