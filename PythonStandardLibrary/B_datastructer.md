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