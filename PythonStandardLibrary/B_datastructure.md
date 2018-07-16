**目录**

[TOC]

`Python` 的数据结构包括多种类型，其中比较常用的是内置类型列表、元素、字典以及集合；另外在标准库（例如 `collections` 模块）中也存在一些数据结构：

* 双端队列 `Deque`
* 可以响应默认值的 `defaultdict` 字典
* 可以记住增加元素的序列的 `OrderDict`
* 扩展一般元组的 `namedtuple`
* 比列表在存储上更高效的 `array`，它采用了更紧凑的内存表示。同时列表的某些方法也能用于 `array`
* 有序列表或数组，剋通过 `bisect` 创建
* `Queue` 可以完成线程间的实序通信（因为列表中内置的 `insert` 和 `pop` 方法不是一个线程安全方式。此外在 `multiprocessing` 中包含一个 `Queue` 版本， 它会处理**进程间的通信**，从而能更容易将一个都**线程**程序转换为**进程**的方式
* `struct` 对于**解码**另一个应用的数据（可能是一个二进制文件或者数据流）非常有用
* 另外就是图和树，它们需哟啊使用 `weakref` 维护引用

## 1. `collections` 容器数据类型

作为容器数据模块，包括了内置类型以外的其他容器数据类型。其中包括的类和方法：

```python
"AsyncGenerator", "AsyncIterable", "AsyncIterator", "Awaitable", "ByteString", "Callable", "ChainMap", "Collection", "Container", "Coroutine", "Counter", "Generator", "Hashable", "ItemsView", "Iterable", "Iterator", "KeysView", "Mapping", "MappingView", "MutableMapping", "MutableSequence", "MutableSet", "OrderedDict", "Reversible", "Sequence", "Set", "Sized", "UserDict", "UserList", "UserString", "ValuesView", "_Link", "_OrderedDictItemsView", "_OrderedDictKeysView", "_OrderedDictValuesView", "__all__", "__builtins__", "__cached__", "__doc__", "__file__", "__loader__", "__name__", "__package__", "__path__", "__spec__", "_chain", "_class_template", "_collections_abc", "_count_elements", "_eq", "_field_template", "_heapq", "_iskeyword", "_itemgetter", "_proxy", "_recursive_repr", "_repeat", "_repr_template", "_starmap", "_sys", "abc", "defaultdict", "deque", "namedtuple"
```



### 1.1 `Counter`

 `Counter` 的作用是作为容器，跟踪相同的值频数，结果是生成对应的数据的类似字典数据。其中可以使用 `update` 方法进行更新填充。⚠️当查询元素的频数时，对于未知的 `key`， `Counter` 不会产生一个 `KeyError` 而是返回一个值 $0$。另外一点对于字典和其他序列的统计方式不同，字典的 `value` 会被作为计数频数。

```python
import collections

print(collections.Counter(['a', 'b', 'c', 'a', 'b', 'b']))
print(collections.Counter({'a': 2, 'b': 3, 'c': 1}))	# 使用 字典
print(collections.Counter(a=2, b=3, c=1))	# 使用 kwargs 方式

# output
Counter({'b': 3, 'a': 2, 'c': 1})
Counter({'b': 3, 'a': 2, 'c': 1})
Counter({'b': 3, 'a': 2, 'c': 1})

# 如果没有传入参数值，那么将做为初始化对象，但是可以通过 update 属性进行填充
c = collections.Counter()
c.update('abcdaab')
print('Sequence:', c)

# output
Sequence: Counter({'a': 3, 'b': 2, 'c': 1, 'd': 1})

c.update({'a': 1, 'd': 5})
print('Dict    :', c)
# output
Dict    : Counter({'d': 6, 'a': 4, 'b': 2, 'c': 1})
    
# 对于探查 Counter 内部的值，如果没有相应的 key 将会返回 0
for letter in 'abcde':
    print('{} : {}'.format(letter, c[letter]))
    
# output
a : 3
b : 2
c : 1
d : 1
e : 0
    
# 对于需要探查 Counter 对象的 “key” 值，可以通过 element 属性。注意通过该方法得到的是一个 itertools.chain，所以需要传给 list 以得到一个列表
print(list(c.elements()))

# output
['a', 'a', 'a', 'b', 'b', 'c', 'd']

# 如果需要了解值最大的 k 个数，可以通过 most_common 的属性——most_common(k) 得到一个有 k 个序列
print('Most common:')
for letter, count in c.most_common(3):
    print('{}: {:>7}'.format(letter, count))
    
# output
Most common:
a:       3
b:       2
c:       1
```

另外对于 `Counter` 可以直接进行算数计算，集合计算，以及原位计算（`+=`, `-=`, `&=`, and `|=`）。需要注意，当技术时负数或者为 0 时，数据会被删除

```python
c1 = collections.Counter(['a', 'b', 'c', 'a', 'b', 'b'])
c2 = collections.Counter('alphabet')

print('C1:', c1)
print('C2:', c2)

print('\nCombined counts:')
print(c1 + c2)

print('\nSubtraction:')
print(c1 - c2)

print('\nIntersection (taking positive minimums):')
print(c1 & c2)

print('\nUnion (taking maximums):')
print(c1 | c2)

# output

C1: Counter({'b': 3, 'a': 2, 'c': 1})
C2: Counter({'a': 2, 'l': 1, 'p': 1, 'h': 1, 'b': 1, 'e': 1, 't': 1})

Combined counts:
Counter({'a': 4, 'b': 4, 'c': 1, 'l': 1, 'p': 1, 'h': 1, 'e': 1, 't': 1})

Subtraction:
Counter({'b': 2, 'c': 1})

Intersection (taking positive minimums):
Counter({'a': 2, 'b': 1})

Union (taking maximums):
Counter({'b': 3, 'a': 2, 'c': 1, 'l': 1, 'p': 1, 'h': 1, 'e': 1, 't': 1})
```



### 1.2 `ChainMap`

`ChainMap` 管理字典的序列，并且可以通过给定的键值对的特定顺序来搜索到相应的值。它具有良好的上下文（**Context**）容器，因为它可以利用对处理数据的方式。

```python
# ChianMap 也满足一般字典的方法
import collections

a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(a, b)

print('Individual Values')
print('a = {}'.format(m['a']))
print('b = {}'.format(m['b']))
print('c = {}'.format(m['c']))
print()

print('Keys = {}'.format(list(m.keys())))
print('Values = {}'.format(list(m.values())))
print()

print('Items:')
for k, v in m.items():
    print('{} = {}'.format(k, v))
print()

print('"d" in m: {}'.format(('d' in m)))

# output
Individual Values
a = A
b = B
c = C

Keys = ['c', 'b', 'a']
Values = ['C', 'B', 'A']

Items:
c = C
b = B
a = A

"d" in m: False
```

因为在子映射的搜索方式中，是按照构造器中传入的参数顺序搜索的。所以上面的 `c` 键对应的值为 `C`。但是可以通过合适的方式进行调整，主要是因为 `ChainMap` 的属性 `maps` 可以得到映射对象的列表对象，并且是保存了搜索顺序的。因为是一个列表对象，所以可以更改顺序已经更新数据值。

```python
print(m.maps)
print('c = {}\n'.format(m['c']))

# reverse 列表，并且传回给原 maps
m.maps = list(reversed(m.maps))

print(m.maps)
print('c = {}'.format(m['c']))

# output
[{'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'}]
c = C

[{'b': 'B', 'c': 'D'}, {'a': 'A', 'c': 'C'}]
c = D

# 下面是通过直接更改值的方式来更新 ChainMap 的数据
print('Before:', m)
# 更新值
m['c'] = 'E'
print('After :', m)
print('a:', a)
# output
Before: ChainMap({'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
After : ChainMap({'a': 'A', 'c': 'E'}, {'b': 'B', 'c': 'D'})
a: {'a': 'A', 'c': 'E'}
```

此外，可以使用 `new_child` 属性方法创建一个在头部额外带有一个映射的新实例，并且是深度复制的。这个方式，还可以

```python
a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}

m1 = collections.ChainMap(a, b)
m2 = m1.new_child()

print('m1 before:', m1)
print('m2 before:', m2)

# 添加数据到头部，没有更新之前更新的 c 键值
m2['c'] = 'E'

print('m1 after:', m1)
print('m2 after:', m2)

# output
m1 before: ChainMap({'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
m2 before: ChainMap({}, {'a': 'A', 'c': 'C'}, {'b': 'B', 'c':'D'})
m1 after: ChainMap({'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
m2 after: ChainMap({'c': 'E'}, {'a': 'A', 'c': 'C'}, {'b': 'B','c': 'D'})
    
# 上面的方法中可以使用另外的方式，达到同样的解决方案
a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}
c = {'c': 'E'}

m1 = collections.ChainMap(a, b)
# 这里的两个赋值给 m2 都是相同的
m2 = m1.new_child(c)
m2 = collections.ChainMap(c, *m1.maps)

print('m1["c"] = {}'.format(m1['c']))
print('m2["c"] = {}'.format(m2['c']))

# output
m1["c"] = C
m2["c"] = E
```



### 1.3 `defaultdict` 

在内置的字典数据类型中，可以通过 `setdefault` 方法来得到键值，但键不存在时则设置相应的值（类似的 `get` 属性是键不存在则返回设置的相应的值， `D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D`）

```python
import collections


def default_factory():
    return 'default value'

d = collections.defaultdict(default_factory, foo='bar')
print('d:', d)
print('foo =>', d['foo'])
print('bar =>', d['bar'])
# output
d: defaultdict(<function default_factory at 0x1074429d8>, {'foo': 'bar'})
foo => bar
bar => default value

# 在上面的例子中传入的默认值是一个函数，实际中常用的是传入列表、集合或者 int。因为这样可以根据键来更新数据
s = 'mississippi'
d = defaultdict(int)
for k in s:
    d[k] += 1

sorted(d.items())
# output
[('i', 4), ('m', 1), ('p', 2), ('s', 4)]

# 下面是实际应用举例，方式不同但结果相同
# 方法一
dict_set = {}

if key not in dict_set:
    dict_set[key] = set()
dict_set[key].add(item)
# 方法二
dict_set = {}

dict_set.setdefault(key, set()).add(item)
# 方法三

dict_set = defaultdict(set)

dict_set[key].add(item)
```



### 1.4 `Deque`

双端队列，即`Double-Ended Queue`，它支持从两头添加和删除元素。它是堆和队列的复合形式，因此需要限定从哪一头更新数据。

```python
# 列表具有的方法，它也可以使用
import collections

d = collections.deque('abcdefg')
print('Deque:', d)
print('Length:', len(d))
print('Left end:', d[0])
print('Right end:', d[-1])

d.remove('c')
print('remove(c):', d)

# output
Deque: deque(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
Length: 7
Left end: a
Right end: g
remove(c): deque(['a', 'b', 'd', 'e', 'f', 'g'])
```

对于填充数据的时候，需要指定 `leftside` 还是 `rightside`，但是进行右端更新的时候不需要指明。包括 `pop` `append` `extend`进行右端更新的时候不需要指明，但是在进行左端更新的时候需要用 `left` 标识指明

```python
# 添加数据
d1 = collections.deque()
d1.extend('abcdefg')
print('extend    :', d1)
d1.append('h')
print('append    :', d1)

# 使用 left 标识符来指明进行左端更新
d2 = collections.deque()
d2.extendleft(range(6))
print('extendleft:', d2)
d2.appendleft(6)
print('appendleft:', d2)

# output
extend    : deque(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
append    : deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
extendleft: deque([5, 4, 3, 2, 1, 0])
appendleft: deque([6, 5, 4, 3, 2, 1, 0])
```

由于双端队列时候线程安全的，所以可以在不同线程中同时从两端列用队列的内容。下面为示例：

```python
import collections
import threading
import time

candle = collections.deque(range(5))


def burn(direction, nextSource):
    while True:
        try:
            next = nextSource()
        except IndexError:
            break
        else:
            print('{:>8}: {}'.format(direction, next))
            time.sleep(0.1)
    print('{:>8} done'.format(direction))
    return


left = threading.Thread(target=burn,
                        args=('Left', candle.popleft))
right = threading.Thread(target=burn,
                         args=('Right', candle.pop))

left.start()
right.start()

left.join()
right.join()

# output

 Left: 0
Right: 4
Right: 3
 Left: 1
Right: 2
 Left done
Right done
```

在双端队列中还有一个比较有趣的功能，旋转。它的功能是从一段去除元素，直接移动到另一端——正值为向右旋转（顺时针），即从右端取出数据移动到左端；负值则是相反方向。

```python
d = collections.deque(range(10))
print('Normal        :', d)

d = collections.deque(range(10))
d.rotate(2)
print('Right rotation:', d)

d = collections.deque(range(10))
d.rotate(-2)
print('Left rotation :', d)

# output
Normal        : deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Right rotation: deque([8, 9, 0, 1, 2, 3, 4, 5, 6, 7])
Left rotation : deque([2, 3, 4, 5, 6, 7, 8, 9, 0, 1])
```

注意⚠️，`Deque` 的大小可以被限制，这样当队列达到最大长度后，已经队列将沿着更新数据的方向将整个队列向该方向推——这样丢弃前方的值以添加新值。

```python
import random
import collections
random.seed(1)

d1 = collections.deque(maxlen=3)
d2 = collections.deque(maxlen=3)

for i in range(5):
    n = random.randint(0, 100)
    print('n =', n)
    d1.append(n)
    d2.appendleft(n)
    print('D1:', d1)
    print('D2:', d2)
    
# output
n = 17
D1: deque([17], maxlen=3)
D2: deque([17], maxlen=3)
n = 72
D1: deque([17, 72], maxlen=3)
D2: deque([72, 17], maxlen=3)
n = 97
D1: deque([17, 72, 97], maxlen=3)
D2: deque([97, 72, 17], maxlen=3)
n = 8
D1: deque([72, 97, 8], maxlen=3)
D2: deque([8, 97, 72], maxlen=3)
n = 32
D1: deque([97, 8, 32], maxlen=3)
D2: deque([32, 8, 97], maxlen=3)
```



### 1.5 `OrderedDict`

它是字典的子类，可以记住更新的顺序（常规的字典不能跟踪插入顺序）。另外这类数据类型，在进行比较相等关系的时候，需要考虑元素添加的顺序。

```python
print('Regular dictionary:')
d = {}
d['a'] = 'A'
d['b'] = 'B'
d['c'] = 'C'

for k, v in d.items():
    print(k, v)

print('\nOrderedDict:')
d = collections.OrderedDict()
d['a'] = 'A'
d['b'] = 'B'
d['c'] = 'C'

for k, v in d.items():
    print(k, v)
    
# output 这里的结果因版本存在差异，但是实际上内置的字典不会追踪添加顺序
Regular dictionary:
c C
b B
a A

OrderedDict:
a A
b B
c C
```

重排，具有可以将值移动到前端还是后端，这里需要通过 `move_to_end` 方法来实现，另外传入 `last` 来确定是传入前端还是后端：

```python
import collections

d = collections.OrderedDict(
    [('a', 'A'), ('b', 'B'), ('c', 'C')]
)

print('Before:')
for k, v in d.items():
    print(k, v)

d.move_to_end('b')

print('\nmove_to_end():')
for k, v in d.items():
    print(k, v)

d.move_to_end('b', last=False)

print('\nmove_to_end(last=False):')
for k, v in d.items():
    print(k, v)
    
# output
Before:
a A
b B
c C

move_to_end():
a A
c C
b B

move_to_end(last=False):
b B
a A
c C
```



### 1.6 `Array` 固定类型数据序列

作用是可以高效管理**固定类型数值数据**的序列，即要求所有成员都必须是相同的基本类型。需要注意 `array` 是一个独立的 `module`。

```python
"ArrayType", "__doc__", "__file__", "__loader__", "__name__", "__package__", "__spec__", "_array_reconstructor", "array", "typecodes"
```

对于 `array` 支持的数据类型，在下表中有说明：

| Type Code |         Type         | Minimum size (bytes) |
| :-------: | :------------------: | :------------------- |
|    `b`    |        `int`         | 1                    |
|    `B`    |        `int`         | 1                    |
|    `h`    |   ` signed short`    | 2                    |
|    `H`    |  ` unsigned short`   | 2                    |
|    `i`    |    `  signed int`    | 2                    |
|    `I`    |    `unsigned int`    | 2                    |
|    `l`    |   `  signed long`    | 4                    |
|    `L`    |   `unsigned long`    | 4                    |
|    `q`    | `  signed long long` | 8                    |
|    `Q`    | `unsigned long long` | 8                    |
|    `f`    |       `float`        | 4                    |
|    `D`    |    `double float`    | 8                    |

初始化 `array` 初始化的方式，是需要实例化对象，其中需要两个参数——分别是指示数据类型和数据（其中数据参数可选，因为可以只实例化对象），详情如下：

```python
import array
import binascii

s = b'This is the array.'
a = array.array('b', s)

print('As byte string:', s)
print('As array      :', a)
print('As hex        :', binascii.hexlify(a))

# output
As byte string: b'This is the array.'
As array      : array('b', [84, 104, 105, 115, 32, 105, 115, 32,
 116, 104, 101, 32, 97, 114, 114, 97, 121, 46])
As hex        : b'54686973206973207468652061727261792e'
```

`array` 的操作上和其他序列方式类似，例如`slice`, `iteration`, `append`，实际例子如下：

```python
a = array.array('i', range(3))
print('Initial :', a)

a.extend(range(3))
print('Extended:', a)

print('Slice   :', a[2:5])

print('Iterator:')
print(list(enumerate(a)))

# output
Initial : array('i', [0, 1, 2])
Extended: array('i', [0, 1, 2, 0, 1, 2])
Slice   : array('i', [2, 0, 1])
Iterator:
[(0, 0), (1, 1), (2, 2), (3, 0), (4, 1), (5, 2)]
```

注意⚠️，`array` 的内容可以写入文件以及从文件读取。对于数据处理不仅可以直接从二进制文件读取原始数据，并将字节转换为适当的类型。在应用中可以使用 `tobytes` 方法替换 `tofile` 来格式化数据，以及使用 `frombytes` 来替换 `fromfile` 将数据转换为 `array` 实例。

```python
import array
import binascii
import tempfile		# 这个 module 可以跨平台的进行上下文管理，并且提供了自动清理的高级接口

a = array.array('i', range(5))
print('A1:', a)

# Write the array of numbers to a temporary file
output = tempfile.NamedTemporaryFile()
a.tofile(output.file)  # must pass an *actual* file，这里可以使用 as_bytes = a.tobytes() 格式数据——实际就是 16 进制数据——并且无需写入文件
output.flush()

# Read the raw data
with open(output.name, 'rb') as file:
    raw_data = file.read()
    print('Raw Contents:', binascii.hexlify(raw_data))	# 这里使用 hexlify 属性将数据转换为了原来的数据内容

    # Read the data into an array
    file.seek(0)
    a2 = array.array('i')
    a2.fromfile(file, len(a))
    print('A2:', a2)
    
# output
A1: array('i', [0, 1, 2, 3, 4])
Raw Contents: b'0000000001000000020000000300000004000000'
A2: array('i', [0, 1, 2, 3, 4])

```

候选字节排序（**Alternative Byte Ordering**），因为 `array` 存储方式存在差异（大端和小端，例如 `C` 和 `Fortran` 存储方式差异），所以在不同字节熟悉的系统或者网络上时，需要转换顺序。这里可以使用 `byteswap` 方法进行转换。

### 1.7 `heapq` 堆排序算法

它的作用是实现了一个用于 `Python` 列表的最小堆排序算法。`heap` 是一个树形数据结构，子节点和父节点是一种有序关系。最大堆（**Max-heap**）特点是父节点大于或等于其子节点，最小堆（**Min-heap**）特点是父及诶单小于或等于子节点。而 `Python` 模块实现了一个最小堆。

```python
# 这里是模拟输出堆的图示
import heapq
import math
from io import StringIO		# 文本输入输出的内存流，使用 close 方法时丢弃文件


def show_tree(tree, total_width=36, fill=' '):
    """Pretty-print a tree."""
    output = StringIO()
    last_row = -1
    for i, n in enumerate(tree):
        if i:
            row = int(math.floor(math.log(i + 1, 2)))
        else:
            row = 0
        if row != last_row:
            output.write('\n')
        columns = 2 ** row
        col_width = int(math.floor(total_width / columns))
        output.write(str(n).center(col_width, fill))
        last_row = row
    print(output.getvalue())
    print('-' * total_width)
    print()

data = [19, 9, 4, 10, 11]

# 在 heapq 中有两种方式创建 heap，heappush() 方法的作用是更新已经创建的堆，可以用于更新堆
heap = []
print('random :', data)
print()

for n in data:
    print('add {:>3}:'.format(n))
    heapq.heappush(heap, n)
    show_tree(heap)
    
# 而使用 heapify() 方法的作用是直接对数据进行创建堆，从代码简洁度上来说，它要更简洁很多
print('random    :', data)
heapq.heapify(data)
print('heapified :')
show_tree(data)

# output
random    : [19, 9, 4, 10, 11]
heapified :

                 4
        9                 19
    10       11
------------------------------------
```

在数据更新上，堆可以使用 `heappop` 方法删除已经创建好的堆中的最小值，并且更新堆的结构。

```python
print('random    :', data)
heapq.heapify(data)
print('heapified :')
show_tree(data)
print()

for i in range(2):
    smallest = heapq.heappop(data)
    print('pop    {:>3}:'.format(smallest))
    show_tree(data)
    
# output
random    : [19, 9, 4, 10, 11]
heapified :

                 4
        9                 19
    10       11
------------------------------------


pop      4:

                 9
        10                19
    11
------------------------------------

pop      9:

                 10
        11                19
------------------------------------
```

对于数据替换方式，需要使用 `heapreplace` 方法——工作流程是**删除最小值**，同时插入新数据——这样保留了堆的大小

```python
heapq.heapify(data)
print('start:')
show_tree(data)

for n in [0, 13, 14]:
    smallest = heapq.heapreplace(data, n)
    print('replace {:>2} with {:>2}:'.format(smallest, n))
    show_tree(data)
    
# output
start:

                 4
        9                 19
    10       11
------------------------------------

replace  4 with  0:

                 0
        9                 19
    10       11
------------------------------------

replace  0 with 13:

                 9
        10                19
    13       11
------------------------------------

replace  9 with 14:

                 10
        11                19
    13       14
------------------------------------
```

堆数据选择最大的几个值，需要使用 `nlargest`  来筛选；而反之，需要使用 `nsmallest`。实际上结果和相当于对序列排序后使用切片方式得到的结果

```python
print('all       :', data)
print('3 largest :', heapq.nlargest(3, data))	# 需要两个参数，第一个参数是选择值
print('from sort :', list(reversed(sorted(data)[-3:])))
print('3 smallest:', heapq.nsmallest(3, data))	# 同样需要两个参数
print('from sort :', sorted(data)[:3])

# output
all       : [19, 9, 4, 10, 11]
3 largest : [19, 11, 10]
from sort : [19, 11, 10]
3 smallest: [4, 9, 10]
from sort : [4, 9, 10]
```

高效插入已排序序列，使用堆的方法可以更高效——它是融合了几个数据的处理的方法， `list(sorted(itertools.chain(*data)))`。但是对于大数据集时，使用前面的方法就显得很吃力，因为堆的插入方式可以节约空间开销。使用堆的 `merge` 方法每次更新元素都产生新的序列，那么在下一次更新元素的时候就决定了固定总量的内存

```python
import heapq
import random


random.seed(2016)

data = []
for i in range(4):
    new_data = list(random.sample(range(1, 101), 5))
    new_data.sort()
    data.append(new_data)

for i, d in enumerate(data):
    print('{}: {}'.format(i, d))

print('\nMerged:')
for i in heapq.merge(*data):
    print(i, end=' ')
print()

# output
0: [33, 58, 71, 88, 95]
1: [10, 11, 17, 38, 91]
2: [13, 18, 39, 61, 63]
3: [20, 27, 31, 42, 45]

Merged:
10 11 13 17 18 20 27 31 33 38 39 42 45 58 61 63 71 88 91 95
```

### 1.8 `bisect` 维护有序列表

使用 `bisect` 可以维护有序列表，而不用每次向列表增加一个元素时调用 `sort` 排序，此外最后的结果保持了列表的有序。特点是**高效**——相当于插入排序的算法，因为不用反复对列表进行显性排序，也不用先构建列表再排序。

```python
"__builtins__", "__cached__", "__doc__", "__file__", "__loader__", "__name__", "__package__", "__spec__", "bisect", "bisect_left", "bisect_right", "insort", "insort_left", "insort_right"
```

插入有序列表，需要使用 `insort` 方法，另外通过 `bisect` 可以得到更新数据的位置。

```python
import bisect

# A series of random numbers
values = [14, 85, 77, 26, 50, 45, 66, 79, 10, 3, 84, 77, 1]

print('New  Pos  Contents')
print('---  ---  --------')

l = []
for i in values:
    position = bisect.bisect(l, i)		# 使用 bisect 得到插入数据的位置
    bisect.insort(l, i)					# 插入数据
    print('{:3}  {:3}'.format(i, position), l)
    
# output
New  Pos  Contents
---  ---  --------
 14    0 [14]
 85    1 [14, 85]
 77    1 [14, 77, 85]
 26    1 [14, 26, 77, 85]
 50    2 [14, 26, 50, 77, 85]
 45    2 [14, 26, 45, 50, 77, 85]
 66    4 [14, 26, 45, 50, 66, 77, 85]
 79    6 [14, 26, 45, 50, 66, 77, 79, 85]
 10    0 [10, 14, 26, 45, 50, 66, 77, 79, 85]
  3    0 [3, 10, 14, 26, 45, 50, 66, 77, 79, 85]
 84    9 [3, 10, 14, 26, 45, 50, 66, 77, 79, 84, 85]
 77    8 [3, 10, 14, 26, 45, 50, 66, 77, 77, 79, 84, 85]
  1    0 [1, 3, 10, 14, 26, 45, 50, 66, 77, 77, 79, 84, 85]
    
# 另外需要注意的是，对于重复数据的处理。有两种方式，左端插入和右端插入。直接使用 insort 方法
# 就是使用了右端插入，如果需要左端插入那么需要 left 指示，即insort_left
# Use bisect_left and insort_left.
l = []
for i in values:
    position = bisect.bisect_left(l, i)
    bisect.insort_left(l, i)
    print('{:3}  {:3}'.format(i, position), l)

# output
New  Pos  Contents
---  ---  --------
 14    0 [14]
 85    1 [14, 85]
 77    1 [14, 77, 85]
 26    1 [14, 26, 77, 85]
 50    2 [14, 26, 50, 77, 85]
 45    2 [14, 26, 45, 50, 77, 85]
 66    4 [14, 26, 45, 50, 66, 77, 85]
 79    6 [14, 26, 45, 50, 66, 77, 79, 85]
 10    0 [10, 14, 26, 45, 50, 66, 77, 79, 85]
  3    0 [3, 10, 14, 26, 45, 50, 66, 77, 79, 85]
 84    9 [3, 10, 14, 26, 45, 50, 66, 77, 79, 84, 85]
 77    7 [3, 10, 14, 26, 45, 50, 66, 77, 77, 79, 84, 85]
  1    0 [1, 3, 10, 14, 26, 45, 50, 66, 77, 77, 79, 84, 85]
```

### 1.9 `queue` 线程安全的 `FIFO` 实现

作用提供了线程安全的 `FIFO`（**Fisrt-in, Fisrt-out**），可以用于多线程的 `FIFO` 数据结构——可以用于信息和数据产生与使用之间安全传递，这里是通过为调用者处理锁定。使用多个线程可以安全**处理同一个** `queue` 实例（注意⚠️这可能因为内存处理和使用，可能限制 `queue` 的大小）

```python
"Empty", "Full", "LifoQueue", "PriorityQueue", "Queue", "__all__", "__builtins__", "__cached__", "__doc__", "__file__", "__loader__", "__name__", "__package__", "__spec__", "deque", "heappop", "heappush", "threading", "time"
```

`queue` 的数据更新需要使用 `put` 方法将数据插入，`get` 方法可以将数据从另一端删除。下面的例子模拟了一个线程的方式，插入数据和删除数据：

```python
import queue

q = queue.Queue()

for i in range(5):
    q.put(i)

while not q.empty():
    print(q.get(), end=' ')
print()

# output
0 1 2 3 4

# 需要注意⚠️ queue 不仅可以控制数据为 FIFO，同时可以 LIFO——这里需要使用 LifoQueue 类


q = queue.LifoQueue()

for i in range(5):
    q.put(i)

while not q.empty():
    print(q.get(), end=' ')
print()
#output
4 3 2 1 0
```

**优先队列（priority queue）**，这类数据结构主要是针对队列中的元素处理顺序由元素特性决定。例如财务部的打印任务优先于开发人员打印代码清单。优先队列是用队列的内容的有序顺序决定获取元素的顺序。下面的例子是使用多线程进行处理作业，这里需要根据 `get` 队列中元素优先级来处理。运行调用线程时，增加到队列中的元素的处理顺序，取决于线程的上下文切换。

```python
import functools		# functools 是一个高阶函数（可以返回其他函数的函数）模块
import queue
import threading


@functools.total_ordering
class Job:

    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        print('New job:', description)
        return

    def __eq__(self, other):
        try:
            return self.priority == other.priority
        except AttributeError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return self.priority < other.priority
        except AttributeError:
            return NotImplemented


q = queue.PriorityQueue()

q.put(Job(3, 'Mid-level job'))
q.put(Job(10, 'Low-level job'))
q.put(Job(1, 'Important job'))


def process_job(q):
    while True:
        next_job = q.get()
        print('Processing job:', next_job.description)
        q.task_done()


workers = [
    threading.Thread(target=process_job, args=(q,)),
    threading.Thread(target=process_job, args=(q,)),
]
for w in workers:
    w.setDaemon(True)
    w.start()

q.join()

# output
New job: Mid-level job
New job: Low-level job
New job: Important job
Processing job: Important job
Processing job: Mid-level job
Processing job: Low-level job
```

下面的示例是创建多线程播客客户程序，通过读取一个或多个 `RSS` 源，从每一个订阅中显示新的 5 集以下载。这里需要并行使用线程来处理下载数据。其中参数——首选项，数据库等需要用户输入，这直接使用硬编码

```python
from queue import Queue
import threading
import time
import urllib
from urllib.parse import urlparse

import feedparser

# Set up some global variables
num_fetch_threads = 2		# 硬编码进程数
enclosure_queue = Queue()

# A real app wouldn't use hard-coded data...
feed_urls = [
    'http://talkpython.fm/episodes/rss',
]	# 硬编码订阅的 URL


def message(s):
    print('{}: {}'.format(threading.current_thread().name, s))
    
# 下面的 download_enclosures 在进程中运行，并且使用 urllib 来下载数据
def download_enclosures(q):
    """This is the worker thread function.
    It processes items in the queue one after
    another.  These daemon threads go into an
    infinite loop, and exit only when
    the main thread ends.
    """
    while True:
        message('looking for the next enclosure')
        url = q.get()
        filename = url.rpartition('/')[-1]
        message('downloading {}'.format(filename))
        response = urllib.request.urlopen(url)
        data = response.read()
        # Save the downloaded file to the current directory
        message('writing to {}'.format(filename))
        with open(filename, 'wb') as outfile:
            outfile.write(data)
        q.task_done()
        
# 定义了线程的目标函数，接下来就可以启动工作线程。在 download_enclosures 处理完 url=q.get() 的数据并返回结果之前，会阻塞并等待
# Set up some threads to fetch the enclosures
for i in range(num_fetch_threads):
    worker = threading.Thread(
        target=download_enclosures,
        args=(enclosure_queue,),
        name='worker-{}'.format(i),
    )
    worker.setDaemon(True)
    worker.start()
    
# 下一步是需要使用 feedparser 模块来提取订阅内容，并将专辑 URL 加入到 queue 中。当开始加入数据，就会有工作线程提取 URL 开始下载，直至全部完成
# Download the feed(s) and put the enclosure URLs into
# the queue.
for url in feed_urls:
    response = feedparser.parse(url, agent='fetch_podcasts.py')
    for entry in response['entries'][:5]:
        for enclosure in entry.get('enclosures', []):
            parsed_url = urlparse(enclosure['url'])
            message('queuing {}'.format(
                parsed_url.path.rpartition('/')[-1]))
            enclosure_queue.put(enclosure['url'])
            
# 最后需要使用 join 将再次等待队列腾空，这样就说明处理完了所有需下载资源
# Now wait for the queue to be empty, indicating that we have
# processed all of the downloads.
message('*** main thread waiting')
enclosure_queue.join()
message('*** done')

# output，可能的结果如下
worker-0: looking for the next enclosure
worker-1: looking for the next enclosure
MainThread: queuing turbogears-and-the-future-of-python-web-frameworks.mp3
MainThread: queuing continuum-scientific-python-and-the-business-of-open-source.mp3
MainThread: queuing openstack-cloud-computing-built-on-python.mp3
MainThread: queuing pypy.js-pypy-python-in-your-browser.mp3
MainThread: queuing machine-learning-with-python-and-scikit-learn.mp3
MainThread: *** main thread waiting
worker-0: downloading turbogears-and-the-future-of-python-web-frameworks.mp3
worker-1: downloading continuum-scientific-python-and-the-business-of-open-source.mp3
worker-0: looking for the next enclosure
worker-0: downloading openstack-cloud-computing-built-on-python.mp3
worker-1: looking for the next enclosure
worker-1: downloading pypy.js-pypy-python-in-your-browser.mp3
worker-0: looking for the next enclosure
worker-0: downloading machine-learning-with-python-and-scikit-learn.mp3
worker-1: looking for the next enclosure
worker-0: looking for the next enclosure
MainThread: *** done
```

### 1.10 `struct` 二进制数据结构

作用是在字符串和二进制数据之间转换，`struct` 包提供了字节串（`strings of bytes`）和内置的 `Python` 数据类型（例如：数字和字符串）之间的转换方法。

```python
"Struct", "__all__", "__builtins__", "__cached__", "__doc__", "__file__", "__loader__", "__name__", "__package__", "__spec__", "_clearcache", "calcsize", "error", "iter_unpack", "pack", "pack_into", "unpack", "unpack_from"
```

`struct` 提供了处理结构值的模块级函数，以及一个`Struct` 类。格式化指示符（**format specifiers**）是一种字符串格式被编译的呈现，这种方式和正则表达式的处理过程相似。因为过程会耗费资源，所以当创建一个 `Struct` 实例并在这个是上调用方法时——而非使用模块级函数，进行一次转换更会高效。

* 打包和解包（**Packing And Unpacking**）

  `Struct` 提供了打包数据为字符串，以及使用由数据类型的字符以及可选的数量以及字节序（**Endianness**）组成的格式化指示符从字符串解包数据。

  在下面的例子中，格式指示符包括了一个整数，一个有两个字符的字符串以及一个浮点数，其中使用空格来分割类型指示符，在编译格式的过程中空格被忽略。

  ```python
  import struct
  import binascii
  
  values = (1, 'ab'.encode('utf-8'), 2.7)
  s = struct.Struct('I 2s f')		# 创建一个“编译”格式
  packed_data = s.pack(*values)	# 打包数据
  
  print('Original values:', values)
  print('Format string  :', s.format)
  print('Uses           :', s.size, 'bytes')
  print('Packed Value   :', binascii.hexlify(packed_data))
  
  # output
  Original values: (1, b'ab', 2.7)
  Format string  : b'I 2s f'
  Uses           : 12 bytes
  Packed Value   : b'0100000061620000cdcc2c40'
      
  # 从打包的对象中提取数据，需要使用 unpack 方法
  packed_data = binascii.unhexlify(b'0100000061620000cdcc2c40')	# 从十六进制数据中转换二进制
  
  s = struct.Struct('I 2s f')
  unpacked_data = s.unpack(packed_data)	# 需要二进制数据
  print('Unpacked Values:', unpacked_data)
  ```

*  字节序（**Endianness**）

  默认的情况下，值的编码是使用内置 `C` 库的字节序。在格式字符串中，可以通过提供的显性字节序命令，可以很方便的覆盖默认的选项。可以使用的字节顺序命令如下：

| Code |            Meaning            |
| :--: | :---------------------------: |
| `@`  |   内置顺序（`Native order`)   |
| `=`  | 内置标准（`Native standard`） |
| `<`  |    小端（`little endian`）    |
| `>`  |     大端（`big endian`）      |
| `!`  |  网络顺序（`Network Order`）  |



```python
import struct
import binascii

values = (1, 'ab'.encode('utf-8'), 2.7)
print('Original values:', values)

endianness = [
    ('@', 'native, native'),
    ('=', 'native, standard'),
    ('<', 'little-endian'),
    ('>', 'big-endian'),
    ('!', 'network'),
]

for code, name in endianness:
    s = struct.Struct(code + ' I 2s f')		# 使用不同的字节顺序来创建 struct
    packed_data = s.pack(*values)
    print()
    print('Format string  :', s.format, 'for', name)
    print('Uses           :', s.size, 'bytes')
    print('Packed Value   :', binascii.hexlify(packed_data))
    print('Unpacked Value :', s.unpack(packed_data))
    
# output
Original values: (1, b'ab', 2.7)

Format string  : b'@ I 2s f' for native, native
Uses           : 12 bytes
Packed Value   : b'0100000061620000cdcc2c40'
Unpacked Value : (1, b'ab', 2.700000047683716)

Format string  : b'= I 2s f' for native, standard
Uses           : 10 bytes
Packed Value   : b'010000006162cdcc2c40'
Unpacked Value : (1, b'ab', 2.700000047683716)

Format string  : b'< I 2s f' for little-endian
Uses           : 10 bytes
Packed Value   : b'010000006162cdcc2c40'
Unpacked Value : (1, b'ab', 2.700000047683716)

Format string  : b'> I 2s f' for big-endian
Uses           : 10 bytes
Packed Value   : b'000000016162402ccccd'
Unpacked Value : (1, b'ab', 2.700000047683716)

Format string  : b'! I 2s f' for network
Uses           : 10 bytes
Packed Value   : b'000000016162402ccccd'
Unpacked Value : (1, b'ab', 2.700000047683716)
```

* 缓冲（`Buffers`）

  二进制打包数据，通常用于存储对性能要求高和扩展模块间传入或传出数据的情况。通过避免为每个打包结构分配一个新的缓冲区，以此来优化之前的情况。这里需要使用 `pack_into` 和 `unpack_from` 的方法来直接写入预分配的缓冲区。

  ```python
  import array
  import binascii
  import ctypes	# 是 Python 的一个外部库，提供和 C 语言兼容的数据类型，可以很方便地调用 DLL 中的函数或者共享库。可以使用纯 Python 代码调用这些函数， 而不用编写额外的 C 代码或使用第三方扩展工具。
  import struct
  
  s = struct.Struct('I 2s f')
  values = (1, 'ab'.encode('utf-8'), 2.7)
  print('Original:', values)
  
  print()
  print('ctypes string buffer')
  
  b = ctypes.create_string_buffer(s.size)
  print('Before  :', binascii.hexlify(b.raw))
  s.pack_into(b, 0, *values)
  print('After   :', binascii.hexlify(b.raw))
  print('Unpacked:', s.unpack_from(b, 0))
  
  print()
  print('array')
  
  a = array.array('b', b'\0' * s.size)	# size 属性指出缓冲区需要多大
  print('Before  :', binascii.hexlify(a))
  s.pack_into(a, 0, *values)
  print('After   :', binascii.hexlify(a))
  print('Unpacked:', s.unpack_from(a, 0))
  
  # output
  Original: (1, b'ab', 2.7)
  
  ctypes string buffer
  Before  : b'000000000000000000000000'
  After   : b'0100000061620000cdcc2c40'
  Unpacked: (1, b'ab', 2.700000047683716)
  
  array
  Before  : b'000000000000000000000000'
  After   : b'0100000061620000cdcc2c40'
  Unpacked: (1, b'ab', 2.700000047683716)
  ```

  





## 2. `Enumeration` 数据类型

### 2.1  `Enum` 枚举类型

该模块定义了具有迭代和比较能力的 `Enumeration ` 类型，同时它兼具了定义值名称的值，而非使用字面上的正数和字符串。官方文档中的描述，很好解释了它的意义：

> `The properties of an enumeration are useful for defining an immutable, related set of constant values that have a defined sequence but no inherent semantic meaning. Classic examples are days of the week (Sunday through Saturday) and school assessment grades (‘A’ through ‘D’, and ‘F’). Other examples include error status values and states within a defined process.`



> `It is possible to simply define a sequence of values of some other basic type, such as ` `int` ` or ` `str` `, to represent discrete arbitrary values. However, an enumeration ensures that such values are distinct from any others, and that operations without meaning (“Wednesday times two”) are not defined for these values.`

在创建上该数据类型上，可以使用类语法。要求每一个 `enumeration` 都必须具有唯一值和有效的识别符用于限制它的名称，此外值不能重复。



```python
# 假设对于需要定义整年月份的对象，可以定义常量名称对应月份，但是这个限定了值是 int。使用 Enum 可以解决该问题，定义值名称为 Month，值越各月份的简写
import enum
Month = enum.Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

print(type(Month))
# output
enum.EnumMeta

# 之后可以直接使用 Month 的属性方式来读取或者通过字典读取 key 的方式来获取值
print(Month.Apr)
print(Month["Apr"])
# output
Month.Apr

# 另外可以通过定制化类，来控制新的对象
class BugStatus(enum.Enum):
    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1


print('\nMember name: {}'.format(BugStatus.wont_fix.name))
print('Member value: {}'.format(BugStatus.wont_fix.value))

# output
Member name: wont_fix
Member value: 4
    
# 该对象可以进行迭代以及进行比较，下面将从这两个角度以实际例子的角度来演示示例
for status in BugStatus:
    print('{:15} = {}'.format(status.name, status.value))
    
# output
new             = 7
incomplete      = 6
invalid         = 5
wont_fix        = 4
in_progress     = 3
fix_committed   = 2
fix_released    = 1

# 需要注意的是该该对象仅能比较 identity 和相等，而不能进行大于和小于比较——将产生类型错误
actual_state = BugStatus.wont_fix
desired_state = BugStatus.fix_released

print('Equality:',
      actual_state == desired_state,
      actual_state == BugStatus.wont_fix)
print('Identity:',
      actual_state is desired_state,
      actual_state is BugStatus.wont_fix)
print('Ordered by value:')
try:
    print('\n'.join('  ' + s.name for s in sorted(BugStatus)))
except TypeError as err:
    print('  Cannot sort: {}'.format(err))
    
# output
Equality: False True
Identity: False True
Ordered by value:
  Cannot sort: '<' not supported between instances of 'BugStatus
' and 'BugStatus'
```

`Enum` 的成员值，并没有限制为 `integer`，但是实际上可以使用其他类型的数据作为成员值，例如使用元组。另外需要注意，这里的定制化类需要使用将成员传给 `__init__`下面的例子中将成员值，包括为数值型的 `ID` 和可以从当前状态进行转换的列表：

```python
class BugStatus(enum.Enum):

    new = (7, ['incomplete',
               'invalid',
               'wont_fix',
               'in_progress'])
    incomplete = (6, ['new', 'wont_fix'])
    invalid = (5, ['new'])
    wont_fix = (4, ['new'])
    in_progress = (3, ['new', 'fix_committed'])
    fix_committed = (2, ['in_progress', 'fix_released'])
    fix_released = (1, ['new'])

    def __init__(self, num, transitions):
        self.num = num
        self.transitions = transitions

    def can_transition(self, new_state):
        return new_state.name in self.transitions


print('Name:', BugStatus.in_progress)
print('Value:', BugStatus.in_progress.value)
print('Custom attribute:', BugStatus.in_progress.transitions)
print('Using attribute:',
      BugStatus.in_progress.can_transition(BugStatus.new))
      
# output
Name: BugStatus.in_progress
Value: (3, ['new', 'fix_committed'])
Custom attribute: ['new', 'fix_committed']
Using attribute: True
    
# 下面是对更复杂的类型，成员值变为了字典的。这里需要将值直接传给 __init__() 初始化，这点
# 和元组方式不同
class BugStatus(enum.Enum):

    new = {
        'num': 7,
        'transitions': [
            'incomplete',
            'invalid',
            'wont_fix',
            'in_progress',
        ],
    }
    incomplete = {
        'num': 6,
        'transitions': ['new', 'wont_fix'],
    }
    invalid = {
        'num': 5,
        'transitions': ['new'],
    }
    wont_fix = {
        'num': 4,
        'transitions': ['new'],
    }
    in_progress = {
        'num': 3,
        'transitions': ['new', 'fix_committed'],
    }
    fix_committed = {
        'num': 2,
        'transitions': ['in_progress', 'fix_released'],
    }
    fix_released = {
        'num': 1,
        'transitions': ['new'],
    }

    def __init__(self, vals):
        self.num = vals['num']
        self.transitions = vals['transitions']

    def can_transition(self, new_state):
        return new_state.name in self.transitions


print('Name:', BugStatus.in_progress)
print('Value:', BugStatus.in_progress.value)
print('Custom attribute:', BugStatus.in_progress.transitions)
print('Using attribute:',
      BugStatus.in_progress.can_transition(BugStatus.new))

# output
Name: BugStatus.in_progress
Value: {'num': 3, 'transitions': ['new', 'fix_committed']}
Custom attribute: ['new', 'fix_committed']
Using attribute: True
```





## 参考

1. [PEP 435](https://www.python.org/dev/peps/pep-0435) 官方文档关于 `enum` 的说明
2. [flufl.enum](http://pythonhosted.org/flufl.enum/) 对整个文档进行了解释，对于理解`enumeration` 非常有用
3. [collections.abc — Abstract Base Classes for Containers ](https://pymotw.com/3/collections/abc.html) `collection` 模块的抽象基类列表
4. [Command line and environment](https://docs.python.org/3.5/using/cmdline.html#) 对 `Python` 的 `CMD` 可选参数做了解释，同时解释了 `Python` 环境变量，随机种子的应用
5. [Numerical Python](http://www.scipy.org/) 数据处理类 `module` 官方网页，包括 `Numpy`, `Pandas`,`Matplotlib`, `Scipy`, `Sympy` 等
6. [理解字节序](http://www.ruanyifeng.com/blog/2016/11/byte-order.html) 解释了字节顺序，大小端的问题
7. [纸上谈兵: 堆 (heap)](http://www.cnblogs.com/vamei/archive/2013/03/20/2966612.html)  图示的解释了堆的结构以及数据更新
8. [feedparser module](https://pypi.python.org/pypi/feedparser) Mark Pilgrim 的 `feedparser` 模块，用于解析 RSS 和 Atom 订阅内容
9. [第十五章：C语言扩展 — python3-cookbook](http://python3-cookbook-personal.readthedocs.io/zh_CN/latest/chapters/p15_c_extensions.html)  `ctype` 模块说明