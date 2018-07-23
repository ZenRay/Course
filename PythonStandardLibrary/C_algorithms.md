**目录**

[TOC]

编程中存在三种主要的方式，过程式编程、面向对象编程和函数式编程。而在实际应用层面，可能是三种方式混用。

## 1. `functools` 管理函数的工具

作用是处理其他函数的函数。用于创建函数修饰符、允许面向侧面的编程（**aspect oriented programming**）以及传统面向对象方法所不能支持的代码重用。另外还提供了一种快捷方式，修饰符类来实现富有比较的 `APIs`（原句：` It also provides a class decorator for implementing all of the rich comparison APIs using a short-cut`）。另外提供了 `partial` 对象来创建函数及其参数的引用。

### 1.1 修饰符

`functools` 模块提供的主要工具是 `partial` 类，它可以用来 “包装” （`wrap`）一个有默认参数的可回调对象。得到对象本身是可回调的，可以看作是原来的函数，同时与原函数的参数完全相同——这样就避免了使用 `lambda` 方式。

```python
import functools

def myfunc(a, b=2):
    "Docstring for myfunc()."
    print('  called myfunc with:', (a, b))

def show_details(name, f, is_partial=False):
    "Show details of a callable object."
    print('{}:'.format(name))
    print('  object:', f)
    if not is_partial:
        print('  __name__:', f.__name__)
    if is_partial:
        print('  func:', f.func)	# 下面的三个都是 partial 类的方法
        print('  args:', f.args)
        print('  keywords:', f.keywords)
    return

show_details('myfunc', myfunc)
myfunc('a', 3)
print()

# Set a different default value for 'b', but require
# the caller to provide 'a'.
p1 = functools.partial(myfunc, b=4)
show_details('partial with named default', p1, True)
p1('passing a')
p1('override b', b=5)
print()

# Set default values for both 'a' and 'b'.
p2 = functools.partial(myfunc, 'default a', b=99)
show_details('partial with defaults', p2, True)
p2()
p2(b='override b')	# 这里就是使用 partial 实例，且更改参数
print()

print('Insufficient arguments:')
p1()

# output
myfunc:
  object: <function myfunc at 0x1007a6a60>
  __name__: myfunc
  called myfunc with: ('a', 3)

partial with named default:
  object: functools.partial(<function myfunc at 0x1007a6a60>,
b=4)
  func: <function myfunc at 0x1007a6a60>
  args: ()
  keywords: {'b': 4}
  called myfunc with: ('passing a', 4)
  called myfunc with: ('override b', 5)

partial with defaults:
  object: functools.partial(<function myfunc at 0x1007a6a60>,
'default a', b=99)
  func: <function myfunc at 0x1007a6a60>
  args: ('default a',)
  keywords: {'b': 99}
  called myfunc with: ('default a', 99)
  called myfunc with: ('default a', 'override b')

Insufficient arguments:
Traceback (most recent call last):
  File "functools_partial.py", line 51, in <module>
    p1()
TypeError: myfunc() missing 1 required positional argument: 'a'
```

* 获取函数属性

  默认情况下，`partial` 对象是没有 `__name__` 或者 `__doc__` 属性——⚠️实际上是有这`__doc__` 属性的，但是是没有进行格式化而已。但是没有这些属性，修饰的函数将更难调试。因此使用 `update_wrapper` 方法可以从原函数将属性复制或者添加到 `partial` 对象。

  ```python
  import functools
  
  
  def myfunc(a, b=2):
      "Docstring for myfunc()."
      print('  called myfunc with:', (a, b))
  
  def show_details(name, f):
      "Show details of a callable object."
      print('{}:'.format(name))
      print('  object:', f)
      print('  __name__:', end=' ')
      try:
          print(f.__name__)
      except AttributeError:
          print('(no __name__)')
      print('  __doc__', repr(f.__doc__))
      print()
  
  show_details('myfunc', myfunc)
  
  p1 = functools.partial(myfunc, b=4)
  show_details('raw wrapper', p1)
  
  print('Updating wrapper:')
  print('  assign:', functools.WRAPPER_ASSIGNMENTS)
  print('  update:', functools.WRAPPER_UPDATES)
  print()
  
  functools.update_wrapper(p1, myfunc)
  show_details('updated wrapper', p1)
  
  # output
  myfunc:
    object: <function myfunc at 0x1018a6a60>
    __name__: myfunc
    __doc__ 'Docstring for myfunc().'
  
  raw wrapper:
    object: functools.partial(<function myfunc at 0x1018a6a60>,
  b=4)
    __name__: (no __name__)
    __doc__ 'partial(func, *args, **keywords) - new function with
  partial application\n    of the given arguments and keywords.\n'
  
  Updating wrapper:
    assign: ('__module__', '__name__', '__qualname__', '__doc__',
  '__annotations__')
    update: ('__dict__',)
  
  updated wrapper:
    object: functools.partial(<function myfunc at 0x1018a6a60>,
  b=4)
    __name__: myfunc
    __doc__ 'Docstring for myfunc().'
  ```

* 其他可调用对象（**Other Callables**）

  `partial` 可以作用于任何可调用的对象，而不仅仅针对单独的函数

  ```python
  import functools
  
  
  class MyClass:
      "Demonstration class for functools"
  
      def __call__(self, e, f=6):
          "Docstring for MyClass.__call__"
          print('  called object with:', (self, e, f))
  
  
  def show_details(name, f):
      "Show details of a callable object."
      print('{}:'.format(name))
      print('  object:', f)
      print('  __name__:', end=' ')
      try:
          print(f.__name__)
      except AttributeError:
          print('(no __name__)')
      print('  __doc__', repr(f.__doc__))
      return
  
  
  o = MyClass()
  
  show_details('instance', o)
  o('e goes here')
  print()
  
  p = functools.partial(o, e='default for e', f=8)
  functools.update_wrapper(p, o)
  show_details('instance wrapper', p)
  p()
  
  # output
  instance:
    object: <__main__.MyClass object at 0x1011b1cf8>
    __name__: (no __name__)
    __doc__ 'Demonstration class for functools'
    called object with: (<__main__.MyClass object at 0x1011b1cf8>, 'e goes here', 6)
  
  instance wrapper:
    object: functools.partial(<__main__.MyClass object at
  0x1011b1cf8>, f=8, e='default for e')
    __name__: (no __name__)
    __doc__ 'Demonstration class for functools'
    called object with: (<__main__.MyClass object at 0x1011b1cf8>,'default for e', 8)
  ```

* 方法和函数（**Methods And Functions**）

  `partial` 方法返回一个可以直接被调用的对象，而 `partialmethod` 方法返回一个可被调用的对象且可以调用尚未绑定对象的方法。

  ```python
  import functools
  
  def standalone(self, a=1, b=2):
      "Standalone function"
      print('  called standalone with:', (self, a, b))
      if self is not None:
          print('  self.attr =', self.attr)
  
  
  class MyClass:
      "Demonstration class for functools"
  
      def __init__(self):
          self.attr = 'instance attribute'
  
      method1 = functools.partialmethod(standalone)	# 使用 partialmethod 方式
      method2 = functools.partial(standalone)			# 使用 partial 方式
  
  
  o = MyClass()
  
  print('standalone')
  standalone(None)
  print()
  
  print('method1 as partialmethod')
  o.method1()
  print()
  
  print('method2 as partial')
  try:
      o.method2()
  except TypeError as err:
      print('ERROR: {}'.format(err))
      
  # output
  standalone
    called standalone with: (None, 1, 2)
  
  method1 as partialmethod
    called standalone with: (<__main__.MyClass object at 0x114827550>, 1, 2)
    self.attr = instance attribute
  
  method2 as partial
  ERROR: standalone() missing 1 required positional argument: 'self'
  ```

* 为装饰器获取函数属性（**Acquiring Function Properties for Decorators**）

  在装饰器中，更新包装的可调用对象的属性非常有用，因为转换后的函数会得到原“裸”函数的属性。

  ```python
  import functools
  
  
  def show_details(name, f):
      "Show details of a callable object."
      print('{}:'.format(name))
      print('  object:', f)
      print('  __name__:', end=' ')
      try:
          print(f.__name__)
      except AttributeError:
          print('(no __name__)')
      print('  __doc__', repr(f.__doc__))
      print()
  
  
  def simple_decorator(f):
      @functools.wraps(f)		# 装饰器 wraps 方法会对所装饰的函数使用 update_wrapper 方法
      def decorated(a='decorated defaults', b=1):
          print('  decorated:', (a, b))
          print('  ', end=' ')
          return f(a, b=b)
      return decorated
  
  
  def myfunc(a, b=2):
      "myfunc() is not complicated"
      print('  myfunc:', (a, b))
      return
  
  
  # The raw function
  show_details('myfunc', myfunc)
  myfunc('unwrapped, default b')
  myfunc('unwrapped, passing b', 3)
  print()
  
  # Wrap explicitly
  wrapped_myfunc = simple_decorator(myfunc)
  show_details('wrapped_myfunc', wrapped_myfunc)
  wrapped_myfunc()
  wrapped_myfunc('args to wrapped', 4)
  print()
  
  
  # Wrap with decorator syntax
  @simple_decorator
  def decorated_myfunc(a, b):
      myfunc(a, b)
      return
  
  show_details('decorated_myfunc', decorated_myfunc)
  decorated_myfunc()
  decorated_myfunc('args to decorated', 4)
  
  # output
  myfunc:
    object: <function myfunc at 0x101241b70>
    __name__: myfunc
    __doc__ 'myfunc() is not complicated'
  
    myfunc: ('unwrapped, default b', 2)
    myfunc: ('unwrapped, passing b', 3)
  
  wrapped_myfunc:
    object: <function myfunc at 0x1012e62f0>
    __name__: myfunc
    __doc__ 'myfunc() is not complicated'
  
    decorated: ('decorated defaults', 1)
       myfunc: ('decorated defaults', 1)
    decorated: ('args to wrapped', 4)
       myfunc: ('args to wrapped', 4)
  
  decorated_myfunc:
    object: <function decorated_myfunc at 0x1012e6400>
    __name__: decorated_myfunc
    __doc__ None
  
    decorated: ('decorated defaults', 1)
       myfunc: ('decorated defaults', 1)
    decorated: ('args to decorated', 4)
       myfunc: ('args to decorated', 4)
  ```

### 1.2 比较

在 `Python 2.x` 中，类可以定义一个 `__cmp__` 方法，后者会根据这个对象大于、等于以及小于所比较的元素返回一个值 1、0 以及 -1。之后引入了富比较（**Rich Comparison**）的 `API` 方法，例如 `__lt__`, `__le__`, `__eq__`, `__ne__`, `__gt__` , `__ge__` 等方法完成比较操作。`Python 3.x` 之后取代了 `__cmp__` 方法。

* 富比较

  它是为了支持复杂比较的类，从而以最高效的方式实现各个测试。对于简单比较没有比较使用创建各个富比较方法。`total_ordering` 装饰符提供了部分方法的类，并且添加其余的方法

  ```python
  import functools
  import inspect		# 检查存活的对象——包括模块、方法、函数等
  # provides several useful functions to help get information about live objects such as modules, classes, methods, functions, tracebacks, frame objects, and code objects
  from pprint import pprint
  
  
  @functools.total_ordering
  class MyObject:
  
      def __init__(self, val):
          self.val = val
  
      def __eq__(self, other):
          print('  testing __eq__({}, {})'.format(
              self.val, other.val))
          return self.val == other.val
  
      def __gt__(self, other):
          print('  testing __gt__({}, {})'.format(
              self.val, other.val))
          return self.val > other.val
  
  
  print('Methods:\n')
  pprint(inspect.getmembers(MyObject, inspect.isfunction))
  
  a = MyObject(1)
  b = MyObject(2)
  
  print('\nComparisons:')
  for expr in ['a < b', 'a <= b', 'a == b', 'a >= b', 'a > b']:
      print('\n{:<6}:'.format(expr))
      result = eval(expr)
      print('  result of {}: {}'.format(expr, result))
      
  # 这个类必须提供 __eq__ 和另一富比较方法的实现，装饰符会增加其余方法的实现，它们利用类提供的比较来完成工作
  # output
  
  Methods:
  
  [('__eq__', <function MyObject.__eq__ at 0x10139a488>),
   ('__ge__', <function _ge_from_gt at 0x1012e2510>),
   ('__gt__', <function MyObject.__gt__ at 0x10139a510>),
   ('__init__', <function MyObject.__init__ at 0x10139a400>),
   ('__le__', <function _le_from_gt at 0x1012e2598>),
   ('__lt__', <function _lt_from_gt at 0x1012e2488>)]
  
  Comparisons:
  
  a < b :
    testing __gt__(1, 2)
    testing __eq__(1, 2)
    result of a < b: True
  
  a <= b:
    testing __gt__(1, 2)
    result of a <= b: True
  
  a == b:
    testing __eq__(1, 2)
    result of a == b: False
  
  a >= b:
    testing __gt__(1, 2)
    testing __eq__(1, 2)
    result of a >= b: False
  
  a > b :
    testing __gt__(1, 2)
    result of a > b: False
  ```

### 1.3 比较序（**Collation Order**）

由于 `Python 3.x` 废弃了老式比较函数，因此在 `sort` 等函数中也不再支持 `cmp` 参数。`cmp_to_key` 方法可以将它们转换为一个返回比对键（`collation key` ）的函数，这个键可用于确认元素的最终序列中的位置。

```python
import functools


class MyObject:

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return 'MyObject({})'.format(self.val)


def compare_obj(a, b):
    """Old-style comparison function.
    """
    print('comparing {} and {}'.format(a, b))
    if a.val < b.val:
        return -1
    elif a.val > b.val:
        return 1
    return 0


# Make a key function using cmp_to_key()
get_key = functools.cmp_to_key(compare_obj)

def get_key_wrapper(o):
    "Wrapper function for get_key to allow for print statements."
    new_key = get_key(o)
    print('key_wrapper({}) -> {!r}'.format(o, new_key))
    return new_key


objs = [MyObject(x) for x in range(5, 0, -1)]

for o in sorted(objs, key=get_key_wrapper):
    print(o)
    
# 在正常情况下，可以直接使用 cmp_to_key，但这的例子引入了一个额外的装饰器函数，从而在调用 key 函数时可以输入更多信息。而且这个类使用传入的老式比较函数来实现富比较 API

# output
key_wrapper(MyObject(5)) -> <functools.KeyWrapper object at
0x1011c5530>
key_wrapper(MyObject(4)) -> <functools.KeyWrapper object at
0x1011c5510>
key_wrapper(MyObject(3)) -> <functools.KeyWrapper object at
0x1011c54f0>
key_wrapper(MyObject(2)) -> <functools.KeyWrapper object at
0x1011c5390>
key_wrapper(MyObject(1)) -> <functools.KeyWrapper object at
0x1011c5710>
comparing MyObject(4) and MyObject(5)
comparing MyObject(3) and MyObject(4)
comparing MyObject(2) and MyObject(3)
comparing MyObject(1) and MyObject(2)
MyObject(1)
MyObject(2)
MyObject(3)
MyObject(4)
MyObject(5)
```
### 1.4 缓存（**Caching**）

`lru_cache` 装饰器将函数包装并放入最近常用的缓存。函数的参数被用于创建一个 `hash key`，且映射到结果。子序列调用相同的值时，会直接从缓存中抓取值而非调用函数。`cache_info` 方法可以获取缓存的状态， `cache_clear` 方法可以清除缓存

```python
import functools


@functools.lru_cache()
def expensive(a, b):
    print('expensive({}, {})'.format(a, b))
    return a * b


MAX = 2

print('First set of calls:')
for i in range(MAX):
    for j in range(MAX):
        expensive(i, j)
print(expensive.cache_info())

print('\nSecond set of calls:')
for i in range(MAX + 1):
    for j in range(MAX + 1):
        expensive(i, j)
print(expensive.cache_info())

print('\nClearing cache:')
expensive.cache_clear()
print(expensive.cache_info())

print('\nThird set of calls:')
for i in range(MAX):
    for j in range(MAX):
        expensive(i, j)
print(expensive.cache_info())
# 这个例子多次调用 expensive 在嵌套循环中，当被清除缓存后需要重新计算
# output
First set of calls:
expensive(0, 0)
expensive(0, 1)
expensive(1, 0)
expensive(1, 1)
CacheInfo(hits=0, misses=4, maxsize=128, currsize=4)

Second set of calls:
expensive(0, 2)
expensive(1, 2)
expensive(2, 0)
expensive(2, 1)
expensive(2, 2)
CacheInfo(hits=4, misses=9, maxsize=128, currsize=9)

Clearing cache:
CacheInfo(hits=0, misses=0, maxsize=128, currsize=0)

Third set of calls:
expensive(0, 0)
expensive(0, 1)
expensive(1, 0)
expensive(1, 1)
CacheInfo(hits=0, misses=4, maxsize=128, currsize=4)

# ⚠️在长时间运行进程中，为了避免 cache 无节制增长限制的最大的缓存数目。但是可以通过 maxsize 参数来调整大小

@functools.lru_cache(maxsize=2)		# 这里调整了数目
def expensive(a, b):
    print('called expensive({}, {})'.format(a, b))
    return a * b


def make_call(a, b):
    print('({}, {})'.format(a, b), end=' ')
    pre_hits = expensive.cache_info().hits
    expensive(a, b)
    post_hits = expensive.cache_info().hits
    if post_hits > pre_hits:
        print('cache hit')


print('Establish the cache')
make_call(1, 2)
make_call(2, 3)

print('\nUse cached items')
make_call(1, 2)
make_call(2, 3)

print('\nCompute a new value, triggering cache expiration')
make_call(3, 4)

print('\nCache still contains one old item')
make_call(2, 3)

print('\nOldest item needs to be recomputed')
make_call(1, 2)


# output
Establish the cache
(1, 2) called expensive(1, 2)
(2, 3) called expensive(2, 3)

Use cached items
(1, 2) cache hit
(2, 3) cache hit

Compute a new value, triggering cache expiration
(3, 4) called expensive(3, 4)

Cache still contains one old item
(2, 3) cache hit

Oldest item needs to be recomputed
(1, 2) called expensive(1, 2)
```

另外所有的函数需要都能被 hash，否则将有异常 `TypeError`

```python
import functools

@functools.lru_cache(maxsize=2)
def expensive(a, b):
    print('called expensive({}, {})'.format(a, b))
    return a * b


def make_call(a, b):
    print('({}, {})'.format(a, b), end=' ')
    pre_hits = expensive.cache_info().hits
    expensive(a, b)
    post_hits = expensive.cache_info().hits
    if post_hits > pre_hits:
        print('cache hit')


make_call(1, 2)

try:
    make_call([1], 2)	# 列表不可以 hash
except TypeError as err:
    print('ERROR: {}'.format(err))

try:
    make_call(1, {'2': 'two'})
except TypeError as err:
    print('ERROR: {}'.format(err))
    
# output
(1, 2) called expensive(1, 2)
([1], 2) ERROR: unhashable type: 'list'
(1, {'2': 'two'}) ERROR: unhashable type: 'dict'
```

### 1.5 `Reducing a data set`

`reduce` 函数可以接受一个可调用对象和序列数据作为输入，并且以之前的可调用对象，对序列数据进行计算输出一个单一的值

```python
import functools


def do_reduce(a, b):
    print('do_reduce({}, {})'.format(a, b))
    return a + b


data = range(1, 5)
print(data)
result = functools.reduce(do_reduce, data)
print('result: {}'.format(result))

# output
range(1, 5)
do_reduce(1, 2)
do_reduce(3, 3)
do_reduce(6, 4)
result: 10
    
# 如果使用了其他 initialize 参数，是用于替换已有参数的第一参数
data = range(1, 5)
print(data)
result = functools.reduce(do_reduce, data, 99)		# 这里的 99 将替换掉序列中的第一个数据 1，所以序列变为了 [99, 2, 3, 4]
print('result: {}'.format(result))

# output
range(1, 5)
do_reduce(99, 1)
do_reduce(100, 2)
do_reduce(102, 3)
do_reduce(105, 4)
result: 109
    
# 但是当序列中是单个值时，initialize 参数将被用于直接计算；如果没有值的序列，那么将直接被替换
print('Single item in sequence:',
      functools.reduce(do_reduce, [1]))

print('Single item in sequence with initializer:',
      functools.reduce(do_reduce, [1], 99))		# 此时将被用于直接相加，而不会发生替换

print('Empty sequence with initializer:',
      functools.reduce(do_reduce, [], 99))		# 此时数据将直接作为参数计算，返回结果，这里也不会报错

try:
    print('Empty sequence:', functools.reduce(do_reduce, []))		# 空序列将报错
except TypeError as err:
    print('ERROR: {}'.format(err))
    
# output
Single item in sequence: 1
do_reduce(99, 1)
Single item in sequence with initializer: 100
Empty sequence with initializer: 99
ERROR: reduce() of empty sequence with no initial value
```

### 1.6 通用函数（**Generic Function**）

在动态类型语言中，会因为数据类型不同而导致运算符有不同作用。为了避免因为这类行为差异，而使用 `singledispatch` 装饰符来隔绝到不同的函数中（⚠️，实际是使用 `register` 方法的特性来作为替换不同数据类型的函数运行）

```python
import functools

@functools.singledispatch		# 这里需要使用 singledispatch 来将 “原函数”包装起来，作为非强调数据类型的函数运行
def myfunc(arg):
    print('default myfunc({!r})'.format(arg))

@myfunc.register(int)		# 这里使用 register 方法作为强调函数不同数据类型运行方式，注意这里使用的类
def myfunc_int(arg):
    print('myfunc_int({})'.format(arg))


@myfunc.register(list)		# 这里使用 register 方法作为强调函数不同数据类型运行方式
def myfunc_list(arg):
    print('myfunc_list()')
    for item in arg:
        print('  {}'.format(item))


myfunc('string argument')
myfunc(1)
myfunc(2.3)		# 这里的 float 数据将直接被被原函数调用
myfunc(['a', 'b', 'c'])

# output
default myfunc('string argument')
myfunc_int(1)
default myfunc(2.3)
myfunc_list()
  a
  b
  c
    
# 如果存在类的继承的话，将使用最接近的匹配继承顺序——这里包括参数顺序，来使用对应的类
class A:
    pass

class B(A):		# 继承 A
    pass


class C(A):		# 继承 A
    pass


class D(B):		# 继承 B
    pass


class E(C, D):
    pass

@functools.singledispatch
def myfunc(arg):
    print('default myfunc({})'.format(arg.__class__.__name__))


@myfunc.register(A)
def myfunc_A(arg):
    print('myfunc_A({})'.format(arg.__class__.__name__))


@myfunc.register(B)
def myfunc_B(arg):
    print('myfunc_B({})'.format(arg.__class__.__name__))


@myfunc.register(C)
def myfunc_C(arg):
    print('myfunc_C({})'.format(arg.__class__.__name__))


myfunc(A())
myfunc(B())
myfunc(C())
myfunc(D())		# 因为最近的继承来自于 B，所以会优先调用 myfunc_B
myfunc(E())		# 在顺序上来说，C 在前优先判断 C 的继承

# output
myfunc_A(A)
myfunc_B(B)
myfunc_C(C)
myfunc_B(D)
myfunc_C(E)
```

## 2. `Itertools` 迭代器函数

作用，`itertools` 模块提供了一组函数用于处理序列数据集。它是模仿了函数式编程语言例如 [Clojure](https://clojure.org/) ，[Haskell](https://www.haskell.org/) 等的特点。它们处理序列块而且使用内存高效，而且可以联结为在一起用于表达更复杂的迭代算法。另外重要特点是基于迭代器的算法可以提供更好的内存使用特性，而迭代器是用于管理数据的方式，不需要将所有数据都同时存储在内存中，从而减少内存使用，减少数据交换以及其他副作用。

```python
"__doc__", "__loader__", "__name__", "__package__", "__spec__", "_grouper", "_tee", "_tee_dataobject", "accumulate", "chain", "combinations", "combinations_with_replacement", "compress", "count", "cycle", "dropwhile", "filterfalse", "groupby", "islice", "permutations", "product", "repeat", "starmap", "takewhile", "tee", "zip_longest"
```



### 2.1 合并和分解迭代器——Merging And Spliting Iterator

`chain` 函数使用多个迭代器作为参数，并且返回一个迭代器，这个迭代器包含了多个所有迭代器的内容。

```python
from itertools import *

for i in chain([1, 2, 3], ['a', 'b', 'c']):
    print(i, end=' ')
print()
# output
1 2 3 a b c
```

如果已经未知的多个迭代器提前被组合，或者需要逐步被检查。这就需要使用`chain.from_iterable` 方法来创建一个 `chain`

```python
def make_iterables_to_chain():
    yield [1, 2, 3]
    yield ['a', 'b', 'c']


for i in chain.from_iterable(make_iterables_to_chain()):
    print(i, end=' ')
print()

# output
1 2 3 a b c
```

⚠️内置的 `zip` 方法其实也是有元组作为元素的迭代器。但是当遇到第一个迭代器被消耗完，`zip` 将终止。为了避免该种情况发生，可以使用 `zip_longest` 方法来完成——被提前消耗完的迭代器将使用 `None ` 来代替元素

```python
from itertools import *
r1 = range(3)
r2 = range(2)

print('zip stops early:')
print(list(zip(r1, r2)))

r1 = range(3)
r2 = range(2)

print('\nzip_longest processes all of the values:')
print(list(zip_longest(r1, r2)))

# output
zip stops early:
[(0, 0), (1, 1)]

zip_longest processes all of the values:
[(0, 0), (1, 1), (2, None)]
```

`islice` 方法，可以作为切片的迭代器，后续参数是作为索引值。其同样具有三个参数，`start`, `end`, `step`，而其中 `start`, `step` 是作为可选参数

```python
from itertools import *

print('Stop at 5:')
for i in islice(range(100), 5):
    print(i, end=' ')
print('\n')

print('Start at 5, Stop at 10:')
for i in islice(range(100), 5, 10):
    print(i, end=' ')
print('\n')

print('By tens to 100:')
for i in islice(range(100), 0, 100, 10):
    print(i, end=' ')
print('\n')

# output
Stop at 5:
0 1 2 3 4

Start at 5, Stop at 10:
5 6 7 8 9

By tens to 100:
0 10 20 30 40 50 60 70 80 90
```

`tee` 方法默认是产生两个相同元素的独立迭代器，在语义上和 `Unix` 的 `tee` 命令具有形同性。可以利用这种特点进行多种算法的并行处理。另外需要注意⚠️，`tee` 需要迭代器作为输入，如果原始迭代器发生了使用，数据会发生变更

```python
from itertools import *

r = islice(count(), 5)
i1, i2 = tee(r)

print('r:', end=' ')
for i in r:		# 这里对迭代器发生进行了调用
    print(i, end=' ')
    if i > 1:
        break
print()

print('i1:', list(i1))
print('i2:', list(i2))

# output
r: 0 1 2
i1: [3, 4]
i2: [3, 4]
```

### 2.2 转换输入——`Converting Map`

内置的 `map` 函数可以调用一个函数对输出的迭代器（**Iterator**）进行处理，返回值。当迭代器耗尽时，终止运行。`startmap` 方法具有相似功能，但是它会将结果中的元素分隔开给独立的迭代器。

```python
from itertools import *

values = [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]

for i in starmap(lambda x, y: (x, y, x * y), values):
    print('{} * {} = {}'.format(*i))		# 这里使用了解包的方式打开元素
    
# output
0 * 5 = 0
1 * 6 = 6
2 * 7 = 14
3 * 8 = 24
4 * 9 = 36

starmap(lambda x, y: (x, y, x * y), values)
# output
<itertools.starmap at 0x10fd5a390>

[i for i in starmap(lambda x, y: (x, y, x * y), values)]
# output
[(0, 5, 0), (1, 6, 6), (2, 7, 14), (3, 8, 24), (4, 9, 36)]		# 这两步验证了结果得到的结果是一个迭代器
```

### 2.3 产生新值——`Producing New values`

`count` 方法可以对迭代数据产生一个，累加的计数。默认值是 `0`，每次迭代可以在数值上进行累加。另外可以传入两个参数，将两个值每步累加

```python
import fractions
from itertools import *

for i in zip(count(1), ['a', 'b', 'c']):
    print(i)
    
# output
(1, 'a')
(2, 'b')
(3, 'c')

# 使用两个参数作为累加计数参数
start = fractions.Fraction(1, 3)
step = fractions.Fraction(1, 3)

for i in zip(count(start, step), ['a', 'b', 'c']):
    print('{}: {}'.format(*i))
    
# output
1/3: a
2/3: b
1: c
```

`cycle` 函数会将迭代器内容循环，默认上无线循环的——这样会导致内存消耗。下面是使用 `zip` 来控制循环

```python
for i in zip(range(7), cycle(['a', 'b', 'c'])):
    print(i)
    
# output
(0, 'a')
(1, 'b')
(2, 'c')
(3, 'a')
(4, 'b')
(5, 'c')
(6, 'a')

# 另外还有一个可以控制产生重复值的方法 repeat，它需要第二个参数来限制循环次数
for i in repeat('over-and-over', 5):
    print(i)
    
# output
over-and-over
over-and-over
over-and-over
over-and-over
over-and-over

# 下面是综合使用 map repeat 等方式来进行数据计算
for i in map(lambda x, y: (x, y, x * y), repeat(2), range(5)):
    print('{:d} * {:d} = {:d}'.format(*i))
    
# output
2 * 0 = 0
2 * 1 = 2
2 * 2 = 4
2 * 3 = 6
2 * 4 = 8
```

### 2.4 过滤——`Filtering`

`dropwhile` 方法返回一个迭代器，它会生成输入迭代器中条件第一次为 `False` 之后的元素——即遇见第一个不满足条件之后的元素被作为新的迭代器。

```python
def should_drop(x):
    print('Testing:', x)
    return x < 1


for i in dropwhile(should_drop, [-1, 0, 1, 2, -2]):
    print('Yielding:', i)
    
# output
Testing: -1
Testing: 0
Testing: 1		# 1 是第一个不满足条件的迭代器，但是还是会运行 Test。但包括其在内的其他元素都被作为新的迭代器
Yielding: 1
Yielding: 2
Yielding: -2
```

`takewhile` 存在差异的，它是对整体进行扫描，如果为 `True` 则作为新迭代器中的元素，到不满足时之后的所有元素都被抛弃

```python
def should_take(x):
    print('Testing:', x)
    return x < 2


for i in takewhile(should_take, [-1, 0, 1, 2, -2]):
    print('Yielding:', i)
    
# output
Testing: -1
Yielding: -1
Testing: 0
Yielding: 0
Testing: 1
Yielding: 1
Testing: 2		# 不满足条件而把之后的所有元素都抛弃
```

`filter` 可以筛选出每一个满足条件的元素，而使用 `filterfalse` 会筛选出每个不满足条件的元素。

```python
def check_item(x):
    print('Testing:', x)
    return x < 1


for i in filter(check_item, [-1, 0, 1, 2, -2]):
    print('Yielding:', i)
    
# output
Testing: -1
Yielding: -1
Testing: 0
Yielding: 0
Testing: 1
Testing: 2
Testing: -2
Yielding: -2

# 使用 filterfalse 用于筛选不满足条件的元素
for i in filterfalse(check_item, [-1, 0, 1, 2, -2]):
    print('Yielding:', i)
    
# output
Testing: -1
Testing: 0
Testing: 1
Yielding: 1
Testing: 2
Yielding: 2
Testing: -2
```

`compress` 方法可以使用另一种方法用于筛选迭代器的内容，它可以使用另一个迭代器的值——一般是布尔值，用于判断和筛选值

```python
every_third = cycle([False, False, True])	# 这里构建了一个条件
data = range(1, 10)

for i in compress(data, every_third):
    print(i, end=' ')
print()
# output
3 6 9

# 下面是模拟 compress，但是没有完全使用布尔值来筛选数据——实际还是利用数据来模拟布尔值
def compress(data, selectors):
    # compress('ABCDEF', [1,0,1,0,1,1]) --> A C E F
    return (d for d, s in zip(data, selectors) if s)
```

### 2.5 数据分组——`grouping data`

`groupby` 函数依据一个公共的键来组织数据集。

```python
import functools
from itertools import *
import operator		# 可以用于输出一个 python 的操作符，但是以一个高效函数的方式来做
import pprint


@functools.total_ordering
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __gt__(self, other):
        return (self.x, self.y) > (other.x, other.y)


# Create a dataset of Point instances
data = list(map(Point,
                cycle(islice(count(), 3)),
                islice(count(), 7)))
print('Data:')
pprint.pprint(data, width=35)
print()

# Try to group the unsorted data based on X values
print('Grouped, unsorted:')
for k, g in groupby(data, operator.attrgetter('x')):
    print(k, list(g))
print()

# Sort the data
data.sort()
print('Sorted:')
pprint.pprint(data, width=35)
print()

# Group the sorted data based on X values
print('Grouped, sorted:')
for k, g in groupby(data, operator.attrgetter('x')):	# 这里使用了类属性来进行排序，得到了一个迭代器
    print(k, list(g))
print()

# output
Data:
[(0, 0),
 (1, 1),
 (2, 2),
 (0, 3),
 (1, 4),
 (2, 5),
 (0, 6)]

Grouped, unsorted:
0 [(0, 0)]
1 [(1, 1)]
2 [(2, 2)]
0 [(0, 3)]
1 [(1, 4)]
2 [(2, 5)]
0 [(0, 6)]

Sorted:
[(0, 0),
 (0, 3),
 (0, 6),
 (1, 1),
 (1, 4),
 (2, 2),
 (2, 5)]

Grouped, sorted:
0 [(0, 0), (0, 3), (0, 6)]
1 [(1, 1), (1, 4)]
2 [(2, 2), (2, 5)]
```

### 2.6 合并输入——`Combining Input`

`accumulate` 方法传入迭代器中第 `n` 和 `n+1` 两个数据到函数中，并且返回值以生成新的迭代器而不是原输入作为迭代器。

```python
print(list(accumulate(range(5))))	# [0, 1, 2, 3, 4] 是输入，将每步值进行累加
print(list(accumulate('abcde')))

# output
[0, 1, 3, 6, 10]
['a', 'ab', 'abc', 'abcd', 'abcde']

# 该方法不仅可以进行累加，还可以传入其他函数作为新的累加函数
def f(a, b):
    print(a, b)		# 每一步都更新和输出相应的值
    return b + a + b


print(list(accumulate('abcde', f)))

# output
a b
bab c
cbabc d
dcbabcd e
['a', 'bab', 'cbabc', 'dcbabcd', 'edcbabcde']
```

对于迭代对象的数据替换，除了使用 `for` 循环还可以使用 `product` 方法，它会将输入作为笛卡尔积的方式生成新的迭代器。需要注意⚠️，产生的结果是是一个元组构成的迭代器

```python
FACE_CARDS = ('J', 'Q', 'K', 'A')
SUITS = ('H', 'D', 'C', 'S')

DECK = list(
    product(
        chain(range(2, 11), FACE_CARDS),
        SUITS,
    )
)	# 这里每个列表内的元素是一个元组

for card in DECK:
    print('{:>2}{}'.format(*card), end=' ')
    if card[1] == SUITS[-1]:
        print()
    
# output
 2H  2D  2C  2S
 3H  3D  3C  3S
 4H  4D  4C  4S
 5H  5D  5C  5S
 6H  6D  6C  6S
 7H  7D  7C  7S
 8H  8D  8C  8S
 9H  9D  9C  9S
10H 10D 10C 10S
 JH  JD  JC  JS
 QH  QD  QC  QS
 KH  KD  KC  KS
 AH  AD  AC  AS

# 调整 product 的参数顺序会产生不同的结果
FACE_CARDS = ('J', 'Q', 'K', 'A')
SUITS = ('H', 'D', 'C', 'S')

DECK = list(
    product(
        SUITS,
        chain(range(2, 11), FACE_CARDS),
    )
)

for card in DECK:
    print('{:>2}{}'.format(card[1], card[0]), end=' ')		# 注意这里调整了 card 的元素顺序
    if card[1] == FACE_CARDS[-1]:
        print()
        
# output
 2H  3H  4H  5H  6H  7H  8H  9H 10H  JH  QH  KH  AH
 2D  3D  4D  5D  6D  7D  8D  9D 10D  JD  QD  KD  AD
 2C  3C  4C  5C  6C  7C  8C  9C 10C  JC  QC  KC  AC
 2S  3S  4S  5S  6S  7S  8S  9S 10S  JS  QS  KS  AS

# 另外 product 可以传入 repeat 参数这样可以进行自乘得到，重复形式的笛卡尔积
def show(iterable):
    for i, item in enumerate(iterable, 1):
        print(item, end=' ')
        if (i % 3) == 0:
            print()
    print()


print('Repeat 2:\n')
show(list(product(range(3), repeat=2)))

print('Repeat 3:\n')
show(list(product(range(3), repeat=3)))

# output
Repeat 2:

(0, 0) (0, 1) (0, 2)
(1, 0) (1, 1) (1, 2)
(2, 0) (2, 1) (2, 2)

Repeat 3:

(0, 0, 0) (0, 0, 1) (0, 0, 2)
(0, 1, 0) (0, 1, 1) (0, 1, 2)
(0, 2, 0) (0, 2, 1) (0, 2, 2)
(1, 0, 0) (1, 0, 1) (1, 0, 2)
(1, 1, 0) (1, 1, 1) (1, 1, 2)
(1, 2, 0) (1, 2, 1) (1, 2, 2)
(2, 0, 0) (2, 0, 1) (2, 0, 2)
(2, 1, 0) (2, 1, 1) (2, 1, 2)
(2, 2, 0) (2, 2, 1) (2, 2, 2)
```

`permutations` 会产生一个组合。

```python
def show(iterable):
    first = None
    for i, item in enumerate(iterable, 1):
        if first != item[0]:
            if first is not None:
                print()
            first = item[0]
        print(''.join(item), end=' ')
    print()


print('All permutations:\n')
show(permutations('abcd'))

print('\nPairs:\n')
show(permutations('abcd', r=2))		# r 可以控制元素

# output
All permutations:

abcd abdc acbd acdb adbc adcb
bacd badc bcad bcda bdac bdca
cabd cadb cbad cbda cdab cdba
dabc dacb dbac dbca dcab dcba

Pairs:

ab ac ad
ba bc bd
ca cb cd
da db dc
```

另外还有一种是 `combinations` 方式，将输入成员进行组合——这些元素是包括了不重复的元素。另外还有一种方案可以对筛选出重复的元素，这里需要使用 `combinations_with_replacement` 方法

```python
def show(iterable):
    first = None
    for i, item in enumerate(iterable, 1):
        if first != item[0]:
            if first is not None:
                print()
            first = item[0]
        print(''.join(item), end=' ')
    print()


print('Unique pairs:\n')
show(combinations('abcd', r=2))

# output
Unique pairs:

ab ac ad
bc bd
cd

print('Unique pairs:\n')
show(combinations_with_replacement('abcd', r=2))

# output
Unique pairs:

aa ab ac ad
bb bc bd
cc cd
dd
```

## 3. `operator` —— 内置操作符的函数接口

作用是作为内置操作符的函数接口。因为在使用迭代器编程时，有时需要简单的表达式创建小函数，`operator` 模块定义了一些对应算数和内置比较操作，以达到不使用 `lambda` 等新函数的方式来完成的操作。

```python
"__abs__", "__add__", "__all__", "__and__", "__builtins__", "__cached__", "__concat__", "__contains__", "__delitem__", "__doc__", "__eq__", "__file__", "__floordiv__", "__ge__", "__getitem__", "__gt__", "__iadd__", "__iand__", "__iconcat__", "__ifloordiv__", "__ilshift__", "__imatmul__", "__imod__", "__imul__", "__index__", "__inv__", "__invert__", "__ior__", "__ipow__", "__irshift__", "__isub__", "__itruediv__", "__ixor__", "__le__", "__loader__", "__lshift__", "__lt__", "__matmul__", "__mod__", "__mul__", "__name__", "__ne__", "__neg__", "__not__", "__or__", "__package__", "__pos__", "__pow__", "__rshift__", "__setitem__", "__spec__", "__sub__", "__truediv__", "__xor__", "_abs", "abs", "add", "and_", "attrgetter", "concat", "contains", "countOf", "delitem", "eq", "floordiv", "ge", "getitem", "gt", "iadd", "iand", "iconcat", "ifloordiv", "ilshift", "imatmul", "imod", "imul", "index", "indexOf", "inv", "invert", "ior", "ipow", "irshift", "is_", "is_not", "isub", "itemgetter", "itruediv", "ixor", "le", "length_hint", "lshift", "lt", "matmul", "methodcaller", "mod", "mul", "ne", "neg", "not_", "or_", "pos", "pow", "rshift", "setitem", "sub", "truediv", "truth", "xor"
```

### 3.1 逻辑操作——`Logical Operations`

有些函数可以使用来确定一个值的对应 `boolean` 值。

```python
from operator import *

a = -1
b = 5

print('a =', a)
print('b =', b)
print()

print('not_(a)     :', not_(a))		# 相当于使用 not a
print('truth(a)    :', truth(a))	# 如果 a 为 True，那么返回真
print('is_(a, b)   :', is_(a, b))	# 相当于 a is b
print('is_not(a, b):', is_not(a, b))

# output
a = -1
b = 5

not_(a)     : False
truth(a)    : True
is_(a, b)   : False
is_not(a, b): True
```

### 3.2 比较操作符——`Comparison Operators`

支持所有富比较操作符

```python
from operator import *

a = 1
b = 5.0

print('a =', a)
print('b =', b)
for func in (lt, le, eq, ne, ge, gt):		# 相当于<, <=, ==, >=, 和 >
    print('{}(a, b): {}'.format(func.__name__, func(a, b)))
    
# output
a = 1
b = 5.0
lt(a, b): True
le(a, b): True
eq(a, b): False
ne(a, b): True
ge(a, b): False
gt(a, b): False
```

### 3.3 算数操作符——`Arithmetic Operators`

支持处理数字值的算数操作符

```python
from operator import *

a = -1
b = 5.0
c = 2
d = 6

print('a =', a)
print('b =', b)
print('c =', c)
print('d =', d)

print('\nPositive/Negative:')
print('abs(a):', abs(a))
print('neg(a):', neg(a))
print('neg(b):', neg(b))
print('pos(a):', pos(a))
print('pos(b):', pos(b))

print('\nArithmetic:')
print('add(a, b)     :', add(a, b))
print('floordiv(a, b):', floordiv(a, b))	# 整数除法，没有小数点，向下取整
print('floordiv(d, c):', floordiv(d, c))
print('mod(a, b)     :', mod(a, b))
print('mul(a, b)     :', mul(a, b))
print('pow(c, d)     :', pow(c, d))
print('sub(b, a)     :', sub(b, a))
print('truediv(a, b) :', truediv(a, b))	# 浮点数除法
print('truediv(d, c) :', truediv(d, c))

print('\nBitwise:')
print('and_(c, d)  :', and_(c, d))
print('invert(c)   :', invert(c))
print('lshift(c, d):', lshift(c, d))
print('or_(c, d)   :', or_(c, d))
print('rshift(d, c):', rshift(d, c))
print('xor(c, d)   :', xor(c, d))

# output
a = -1
b = 5.0
c = 2
d = 6

Positive/Negative:
abs(a): 1
neg(a): 1
neg(b): -5.0
pos(a): -1
pos(b): 5.0

Arithmetic:
add(a, b)     : 4.0
floordiv(a, b): -1.0
floordiv(d, c): 3
mod(a, b)     : 4.0
mul(a, b)     : -5.0
pow(c, d)     : 64
sub(b, a)     : 6.0
truediv(a, b) : -0.2
truediv(d, c) : 3.0

Bitwise:
and_(c, d)  : 2
invert(c)   : -3
lshift(c, d): 128
or_(c, d)   : 6
rshift(d, c): 1
xor(c, d)   : 4
```

### 3.3 序列操作符——`Sequence Operators`

对序列的操作来说主要包括，建立序列，搜素元素，访问内容，从序列删除元素

```python
from operator import *

a = [1, 2, 3]
b = ['a', 'b', 'c']

print('a =', a)
print('b =', b)

print('\nConstructive:')
print('  concat(a, b):', concat(a, b))		# 拼接序列

print('\nSearching:')
print('  contains(a, 1)  :', contains(a, 1))	# 搜索判断是否存在
print('  contains(b, "d"):', contains(b, "d"))
print('  countOf(a, 1)   :', countOf(a, 1))		# 搜索存在的数量
print('  countOf(b, "d") :', countOf(b, "d"))
print('  indexOf(a, 5)   :', indexOf(a, 1))		# 返回存在的第一个索引值

print('\nAccess Items:')
print('  getitem(b, 1)                  :',
      getitem(b, 1))
print('  getitem(b, slice(1, 3))        :',
      getitem(b, slice(1, 3)))
print('  setitem(b, 1, "d")             :', end=' ')
setitem(b, 1, "d")
print(b)
print('  setitem(a, slice(1, 3), [4, 5]):', end=' ')	# 这需要注意 setitem 和 delitem 会原地修改序列，而不会返回任何值
setitem(a, slice(1, 3), [4, 5])
print(a)

print('\nDestructive:')
print('  delitem(b, 1)          :', end=' ')
delitem(b, 1)
print(b)
print('  delitem(a, slice(1, 3)):', end=' ')
delitem(a, slice(1, 3))
print(a)
# output
a = [1, 2, 3]
b = ['a', 'b', 'c']

Constructive:
  concat(a, b): [1, 2, 3, 'a', 'b', 'c']

Searching:
  contains(a, 1)  : True
  contains(b, "d"): False
  countOf(a, 1)   : 1
  countOf(b, "d") : 0
  indexOf(a, 5)   : 0

Access Items:
  getitem(b, 1)                  : b
  getitem(b, slice(1, 3))        : ['b', 'c']
  setitem(b, 1, "d")             : ['a', 'd', 'c']
  setitem(a, slice(1, 3), [4, 5]): [1, 4, 5]

Destructive:
  delitem(b, 1)          : ['a', 'c']
  delitem(a, slice(1, 3)): [1]
```

### 3.4 原位操作符——`In-place Operator`

原位操作符类似 `+=` 等方式，更多信息可以**参考官方文档**

```
a = -1
b = 5.0
c = [1, 2, 3]
d = ['a', 'b', 'c']
print('a =', a)
print('b =', b)
print('c =', c)
print('d =', d)
print()

a = iadd(a, b)
print('a = iadd(a, b) =>', a)
print()

c = iconcat(c, d)
print('c = iconcat(c, d) =>', c)

# output
a = -1
b = 5.0
c = [1, 2, 3]
d = ['a', 'b', 'c']

a = iadd(a, b) => 4.0

c = iconcat(c, d) => [1, 2, 3, 'a', 'b', 'c']
```

### 3.5 属性和元素获取——`Attribute and Item “Getters”`

`getter` 方法是 `operator` 中使用最广泛地特征。它是运行时（**Runtime**）构建的某些可回调对象，用来获取对象的属性或序列的内容，在处理迭代器或生成器序列是特别有用——它可以降低开销，比 `lambda` 及其他函数开销小很多。 使用方法是 `attrgetter(x, n)` 其中 `n` 是属性名称，使用方式类似于 `lambda x, n: getattr(x, n)`。而对于取元素来说，`itemgetter(x, n)` 其中 `n` 是对应的可用键或者索引，类似于 `lambda x, n: x[n]`。

```python
from operator import *


class MyObj:
    """example class for attrgetter"""

    def __init__(self, arg):
        super().__init__()
        self.arg = arg

    def __repr__(self):
        return 'MyObj({})'.format(self.arg)


l = [MyObj(i) for i in range(5)]
print('objects   :', l)

# Extract the 'arg' value from each object
g = attrgetter('arg')
vals = [g(i) for i in l]
print('arg values:', vals)

# Sort using arg
l.reverse()
print('reversed  :', l)
print('sorted    :', sorted(l, key=g))

# output
objects   : [MyObj(0), MyObj(1), MyObj(2), MyObj(3), MyObj(4)]
arg values: [0, 1, 2, 3, 4]
reversed  : [MyObj(4), MyObj(3), MyObj(2), MyObj(1), MyObj(0)]
sorted    : [MyObj(0), MyObj(1), MyObj(2), MyObj(3), MyObj(4)]

# 取元素
l = [dict(val=-1 * i) for i in range(4)]
print('Dictionaries:')
print(' original:', l)
g = itemgetter('val')
vals = [g(i) for i in l]
print('   values:', vals)
print('   sorted:', sorted(l, key=g))

print()
l = [(i, i * -2) for i in range(4)]
print('\nTuples:')
print(' original:', l)
g = itemgetter(1)
vals = [g(i) for i in l]
print('   values:', vals)
print('   sorted:', sorted(l, key=g))

# outpu
Dictionaries:
 original: [{'val': 0}, {'val': -1}, {'val': -2}, {'val': -3}]
   values: [0, -1, -2, -3]
   sorted: [{'val': -3}, {'val': -2}, {'val': -1}, {'val': 0}]


Tuples:
 original: [(0, 0), (1, -2), (2, -4), (3, -6)]
   values: [0, -2, -4, -6]
   sorted: [(3, -6), (2, -4), (1, -2), (0, 0)]
```

### 3.6 操作符和定制类的结合——`Combining Operators and Custom Classes`

`operator` 中的函数通过对应的操作的标准 `Python` 接口完成工作，所以它不仅适用于内置类型，还可用于定制类，详情参考文档。从下面的示例爱看，更像是使用运算符重载。

```python
from operator import *


class MyObj:
    """Example for operator overloading"""

    def __init__(self, val):
        super(MyObj, self).__init__()
        self.val = val

    def __str__(self):
        return 'MyObj({})'.format(self.val)

    def __lt__(self, other):
        """compare for less-than"""
        print('Testing {} < {}'.format(self, other))
        return self.val < other.val

    def __add__(self, other):
        """add values"""
        print('Adding {} + {}'.format(self, other))
        return MyObj(self.val + other.val)


a = MyObj(1)
b = MyObj(2)

print('Comparison:')
print(lt(a, b))

print('\nArithmetic:')
print(add(a, b))

# output
Comparison:
Testing MyObj(1) < MyObj(2)
True

Arithmetic:
Adding MyObj(1) + MyObj(2)
MyObj(3)
```

## 4. `contextlib`——上下文管理器工具

作用创建和处理上下文管理器的工具，`contextlib` 模块包含了用于处理上下文管理器的工具以及 `with` 语句

```python
"AbstractContextManager", "ContextDecorator", "ExitStack", "_GeneratorContextManager", "_RedirectStream", "__all__", "__builtins__", "__cached__", "__doc__", "__file__", "__loader__", "__name__", "__package__", "__spec__", "_collections_abc", "abc", "closing", "contextmanager", "deque", "redirect_stderr", "redirect_stdout", "suppress", "sys", "wraps"
```

### 4.1 上下文管理器 `API`

上下文管理器要负责一个代码块中的资源，在进入代码块时创建资源，然后在退出代码块时清理资源——这样可以很方便的确保文件在读写完成后关闭文件，下面的示例是使用 `with` 来进行上下文管理

```python
with open("filename.txt", "wt") as f:
	f.write("contents go here")
# 这里的文件会在写入完成后自动关闭
```

在上下文管理器中，`API` 包括两种方法，主要是 `__enter__` 方法用于返回一个对象，以便上下文被使用。在执行离开时，调用 `__exit__` 方法用于清理所使用的资源。下面的方式是模拟上下文的管理方式

```python
class Context:

    def __init__(self):
        print('__init__()')

    def __enter__(self):
        print('__enter__()')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__()')

with Context():
    print('Doing work in the context')
    
# output
__init__()
__enter__()
Doing work in the context
__exit__()
```

在进行上下文管理中使用了 `as` 进行别名管理，可以在 `__enter__` 方法中返回与这个名称相关联的任何对象。下面的示例中，使用 `do_something` 方法

```python
class WithinContext:

    def __init__(self, context):
        print('WithinContext.__init__({})'.format(context))

    def do_something(self):
        print('WithinContext.do_something()')

    def __del__(self):
        print('WithinContext.__del__')


class Context:

    def __init__(self):
        print('Context.__init__()')

    def __enter__(self):
        print('Context.__enter__()')
        return WithinContext(self)		# 这里演示了使用 __enter__ 将上下文内容传达给其他可以处理的对象，例如函数，这里是类

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Context.__exit__()')


with Context() as c:		# 这里使用了 as 进行变量名管理，c 会得到 __enter__ 方法的上下文，并调用了其中的 WithinContext 类
    c.do_something()
    
# output
Context.__init__()
Context.__enter__()
WithinContext.__init__(<__main__.Context object at 0x101e9c080>)
WithinContext.do_something()
Context.__exit__()
WithinContext.__del__
```

在 `__exit__` 中，可以接收某些参数，其中包括 `with` 模块中产生的异常的信息。实际运行过程中，如果上下文可以处理这个异常，`__exit__` 方法应当返回一个 `True` 值来只是不需要传播 `with` 块中的异常，否则的话 `__exit__` 会在运行完成后重新跑出这个异常

```python
class Context:

    def __init__(self, handle_error):
        print('__init__({})'.format(handle_error))
        self.handle_error = handle_error

    def __enter__(self):
        print('__enter__()')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__()')
        print('  exc_type =', exc_type)
        print('  exc_val  =', exc_val)
        print('  exc_tb   =', exc_tb)
        return self.handle_error		# 这里的 False 和 True 在这里被返回，表示了最终处理的结果


with Context(True):		# 这里就是传入了一个 True 表示下面的异常可以杯处理，不需要传播异常
    raise RuntimeError('error message handled')

print()

with Context(False):	# 这里传入的是一个 False 表示异常不被传播，并且将在最后又被抛出
    raise RuntimeError('error message propagated')
    
# output
__init__(True)
__enter__()
__exit__()
  exc_type = <class 'RuntimeError'>
  exc_val  = error message handled
  exc_tb   = <traceback object at 0x1044ea648>

__init__(False)
__enter__()
__exit__()
  exc_type = <class 'RuntimeError'>
  exc_val  = error message propagated
  exc_tb   = <traceback object at 0x1044ea648>
Traceback (most recent call last):
  File "contextlib_api_error.py", line 34, in <module>
    raise RuntimeError('error message propagated')
RuntimeError: error message propagated
```

### 4.2 作为函数装饰器的上下文管理器

在 `4.1` 中主要是使用了示例来解释上下文管理器的处理文件的方式。 `ContextDecorator` 类提供了常规上下文管理器的类，以达到使用函数装饰器的方法做到上下文的管理器的目的。

```python
import contextlib

class Context(contextlib.ContextDecorator):		# 这里传入了一个 contextlib 中的 ContextDecorator 类

    def __init__(self, how_used):
        self.how_used = how_used
        print('__init__({})'.format(how_used))

    def __enter__(self):
        print('__enter__({})'.format(self.how_used))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__({})'.format(self.how_used))


@Context('as decorator')
def func(message):
    print(message)


# 下面两个演示了直接调用上下文管理器和以上下文管理器装饰器函数的使用是那个的差异。被装饰器包裹的函数，不能像 with 与 as 语句一样调用 __enter__ 返回的值；另外作为装饰器的的管理器中传入的参数，可以被用于全局中
print()
with Context('as context manager'):
    print('Doing work in the context')

print()
func('Doing work in the wrapped function')

# output
__init__(as decorator)		# 这个结果是在做装饰器中的时候 初始化的输出——即 17 行到 19 行的输出

__init__(as context manager)
__enter__(as context manager)
Doing work in the context
__exit__(as context manager)

__enter__(as decorator)
Doing work in the wrapped function
__exit__(as decorator)
```

### 4.3 从生成器到上下文管理器

传统的创建上下文管理器的方法是创建一个 `__enter__` 和 `__exit__` 方法的类。但是在编写代码的时候过多的使用这种方式，会增加代码负担。为了解决这种问题，可以使用 `contextmanager()` 作为装饰器将一个生成器函数转换为上下文管理器

```python
import contextlib


@contextlib.contextmanager
def make_context():
    print('  entering')
    try:
        yield {}
    except RuntimeError as err:
        print('  ERROR:', err)
    finally:
        print('  exiting')

# 这里生成器要初始化，用 yield 生成一次值，生成的值会被绑定到 with 语句中的 as 子句中的变量，完成后清理上下文，同样的如果 with 语句代码块处理过程出现异常会根据上下文处理异常的方式处理
print('Normal:')
with make_context() as value:
    print('  inside with statement:', value)

print('\nHandled error:')
with make_context() as value:
    raise RuntimeError('showing example of handling an error')

print('\nUnhandled error:')
with make_context() as value:
    raise ValueError('this exception is not handled')
    
# output
Normal:
  entering
  inside with statement: {}
  exiting

Handled error:
  entering
  ERROR: showing example of handling an error
  exiting

Unhandled error:
  entering
  exiting
Traceback (most recent call last):
  File "contextlib_contextmanager.py", line 33, in <module>
    raise ValueError('this exception is not handled')
ValueError: this exception is not handled
```

其中 `contextmanager` 返回的上下文管理器是来源于 `ContextDecorator` ，所以它也可以被用于函数装饰器

```python
import contextlib

@contextlib.contextmanager
def make_context():
    print('  entering')
    try:
        # Yield control, but not a value, because any value
        # yielded is not available when the context manager
        # is used as a decorator.
        yield
    except RuntimeError as err:
        print('  ERROR:', err)
    finally:
        print('  exiting')


@make_context()
def normal():
    print('  inside with statement')


@make_context()
def throw_error(err):
    raise err


print('Normal:')
normal()

print('\nHandled error:')
throw_error(RuntimeError('showing example of handling an error'))

print('\nUnhandled error:')
throw_error(ValueError('this exception is not handled'))

# 在这里的例子中，同样存在上下文管理器做装饰器和直接使用上下文管理器的差异。此外被装饰的函数，得到的参数是可以被使用的，见 throw_error 得到的参数

# output
Normal:
  entering
  inside with statement
  exiting

Handled error:
  entering
  ERROR: showing example of handling an error
  exiting

Unhandled error:
  entering
  exiting
Traceback (most recent call last):
  File "contextlib_contextmanager_decorator.py", line 43, in
<module>
    throw_error(ValueError('this exception is not handled'))
  File ".../lib/python3.6/contextlib.py", line 52, in inner
    return func(*args, **kwds)
  File "contextlib_contextmanager_decorator.py", line 33, in
throw_error
    raise err
ValueError: this exception is not handled

```

### 4.3 关闭打开的句柄——`Closing Open Handles`

`file` 类可以直接支持上下文管理器的 `API`，但是某些打开句柄不一定支持这个 `API`。下面演示了使用具有 `close` 方法的类，但是不支持上下文管理器 `API` ，这里可以使用 `closing` 方法来创建一个上下文管理器，来保障句柄最终被关闭：

```python
import contextlib


class Door:

    def __init__(self):
        print('  __init__()')
        self.status = 'open'

    def close(self):
        print('  close()')
        self.status = 'closed'


print('Normal Example:')
with contextlib.closing(Door()) as door:
    print('  inside with statement: {}'.format(door.status))
print('  outside with statement: {}'.format(door.status))

print('\nError handling example:')
try:
    with contextlib.closing(Door()) as door:
        print('  raising from inside with statement')
        raise RuntimeError('error message')
except Exception as err:
    print('  Had an error:', err)
    
# output
Normal Example:
  __init__()
  inside with statement: open
  close()
  outside with statement: closed

Error handling example:
  __init__()
  raising from inside with statement
  close()
  Had an error: error message
```

### 4.4 忽略异常——`Ignoring Exception`

忽略其他 `library` 产生的异常通常是非常有用的，因为这个异常值说明了得到的设计期望，或者结果是可以被或略的异常。常见的是使用 `try/except` 语句的方式，通过在 `except` 中运行 `pass` 来避免。而在 `contextlib` 中可以使用 `suppress` 方法来显性处理 `with` 语句中的异常

```python
import contextlib


class NonFatalError(Exception):
    pass


def non_idempotent_operation():
    raise NonFatalError(
        'The operation failed because of existing state'
    )

# 方式一，使用 suppress 方法来显性控制
with contextlib.suppress(NonFatalError):
    print('trying non-idempotent operation')
    non_idempotent_operation()
    print('succeeded!')

print('done')

# 方法二，使用 try/except 来控制
try:
    print('trying non-idempotent operation')
    non_idempotent_operation()
    print('succeeded!')
except NonFatalError:
    pass
    
# output
trying non-idempotent operation
done
```

### 4.5 重定向输出流——`Redirecting Ouput Streams`

在输出结果中，可以使用不同的参数来配置结果的输出目标，`redicect_stdout` 和 `redirect_stderr` 两个上下文管理器方法，可以用于捕获结果——捕获可以用于没有提供接收新的输出参数的函数的输出。

```python
from contextlib import redirect_stdout, redirect_stderr
import io
import sys


def misbehaving_function(a):
    sys.stdout.write('(stdout) A: {!r}\n'.format(a))
    sys.stderr.write('(stderr) A: {!r}\n'.format(a))


capture = io.StringIO()
with redirect_stdout(capture), redirect_stderr(capture):
    misbehaving_function(5)

print(capture.getvalue())

# misbehaving_function() 同时写了 stdout 和 stderr ，不过后面两个上下文管理器都使用了同一个 io.StringIO 实例将其捕获用于之后的使用

# output
(stdout) A: 5
(stderr) A: 5
```

### 4.6 动态上下文管理器栈——`Dynamic Context Manager Stacks`

多数上下文管理只能每次处理一个对象，例如单个文件或者数据库句柄。这些情况中对象都是提前知道的，使用上下文管理器也都可以围绕这个对象展开。不过在另一些情况中，可能需要创建一个未知数量的上下文，同时希望控制流退出上下文时这些上下文管理器也全部执行清理功能。 `ExitStack` 就是用来处理这些动态情况的。

`ExitStack` 实例维护一个包含清理回调的栈。这些回调都会被放在上下文中，任何被注册的回调都会在控制流退出上下文时以倒序方式被调用。这有点像嵌套了多层的 `with` 语句，除了它们是被动态创建的。

#### 4.6.1 栈上下文管理器

`ExitStack` 可以使用多种方法来对栈进行填充，例如 `enter_content` 方法，可以将上下文管理器添加到栈中。它首先会在整个上下文中调用 `__enter__` 方法，之后寄存器（`register` ）中使用 `__exit__` 方法来回调执行栈的后续工作（例如出栈）

```python
import contextlib


@contextlib.contextmanager
def make_context(i):
    print('{} entering'.format(i))
    yield {}
    print('{} exiting'.format(i))


def variable_stack(n, msg):
    with contextlib.ExitStack() as stack:
        for i in range(n):
            stack.enter_context(make_context(i))
        print(msg)


variable_stack(2, 'inside context')

# output
0 entering
1 entering
inside context
1 exiting
0 exiting
```

注意⚠️，在 `python 3.x` 中取消了 `nest` 的嵌套方法，但是可以使用 `ExitStack` 来模拟嵌套。任何发生在上下文中的错误都会交给上下文管理器的正常错误处理系统去处理，下面的示例揭示了上下文管理器类传递错误的方式

```python
import contextlib


class Tracker:
    "Base class for noisy context managers."

    def __init__(self, i):
        self.i = i

    def msg(self, s):
        print('  {}({}): {}'.format(
            self.__class__.__name__, self.i, s))

    def __enter__(self):
        self.msg('entering')


class HandleError(Tracker):
    "If an exception is received, treat it as handled."

    def __exit__(self, *exc_details):
        received_exc = exc_details[1] is not None
        if received_exc:
            self.msg('handling exception {!r}'.format(
                exc_details[1]))
        self.msg('exiting {}'.format(received_exc))
        # Return Boolean value indicating whether the exception
        # was handled.
        return received_exc


class PassError(Tracker):
    "If an exception is received, propagate it."

    def __exit__(self, *exc_details):
        received_exc = exc_details[1] is not None
        if received_exc:
            self.msg('passing exception {!r}'.format(
                exc_details[1]))
        self.msg('exiting')
        # Return False, indicating any exception was not handled.
        return False


class ErrorOnExit(Tracker):
    "Cause an exception."

    def __exit__(self, *exc_details):
        self.msg('throwing error')
        raise RuntimeError('from {}'.format(self.i))


class ErrorOnEnter(Tracker):
    "Cause an exception."

    def __enter__(self):
        self.msg('throwing error on enter')
        raise RuntimeError('from {}'.format(self.i))

    def __exit__(self, *exc_info):
        self.msg('exiting')
        
# 例子中的类会被包含在 variable_stack() 中使用（见上面的代码），variable_stack() 把上下文管理器放到 ExitStack 中使用，逐一建立起上下文。下面的例子我们将传递不同的上下文管理器来测试错误处理结果。首先我们测试无异常的常规情况。

print('No errors:')
variable_stack([
    HandleError(1),
    PassError(2),
])

# 接下来创建了在栈末的处理异常的例子，这样的话所有已经打开的上下文管理器会随着栈的释放而关闭
print('\nError at the end of the context stack:')
variable_stack([
    HandleError(1),
    HandleError(2),
    ErrorOnExit(3),
])

# 之后，做一个在栈中间处理异常的例子，某些时候直到上下文被关闭，错误才会发生。这样错误对上下文是没有影响的
print('\nError in the middle of the context stack:')
variable_stack([
    HandleError(1),
    PassError(2),
    ErrorOnExit(3),
    HandleError(4),
])

# 最后创建了一个例子，用于解释未处理的异常以及在被代码调用传播的异常。这里需要注意⚠️，栈中的上下文管理器可以接收一个异常值，同时返回一个 True 值，这样可以避免异常值被传播到其他上下文管理器中
try:
    print('\nError ignored:')
    variable_stack([
        PassError(1),
        ErrorOnExit(2),
    ])
except RuntimeError:
    print('error handled outside of context')
    
# output
No errors:
  HandleError(1): entering
  PassError(2): entering
  PassError(2): exiting
  HandleError(1): exiting False
  outside of stack, any errors were handled

Error at the end of the context stack:
  HandleError(1): entering
  HandleError(2): entering
  ErrorOnExit(3): entering
  ErrorOnExit(3): throwing error
  HandleError(2): handling exception RuntimeError('from 3',)
  HandleError(2): exiting True
  HandleError(1): exiting False
  outside of stack, any errors were handled

Error in the middle of the context stack:
  HandleError(1): entering
  PassError(2): entering
  ErrorOnExit(3): entering
  HandleError(4): entering
  HandleError(4): exiting False
  ErrorOnExit(3): throwing error
  PassError(2): passing exception RuntimeError('from 3',)
  PassError(2): exiting
  HandleError(1): handling exception RuntimeError('from 3',)
  HandleError(1): exiting True
  outside of stack, any errors were handled

Error ignored:
  PassError(1): entering
  ErrorOnExit(2): entering
  ErrorOnExit(2): throwing error
  PassError(1): passing exception RuntimeError('from 2',)
  PassError(1): exiting
error handled outside of context
```

#### 4.6.2 任意上下文回调——`Arbitrary Context Callbacks`

`ExitStack` 也支持任意回调方式来关闭上下文，同样也是为了方便通过上下文的方式来关闭文件

```python
import contextlib


def callback(*args, **kwds):
    print('closing callback({}, {})'.format(args, kwds))

# 正如使用了上下文管理器的 __exit__ 方法，下面演示了调换顺序后在寄存器中的执行方式
with contextlib.ExitStack() as stack:
    stack.callback(callback, 'arg1', 'arg2')
    stack.callback(callback, arg3='val3')
    
# output
closing callback((), {'arg3': 'val3'})
closing callback(('arg1', 'arg2'), {})

# 不论错误是否发生以及给定的信息是否有错误发生，回调会被执行。返回值也会被忽略，因为上下文不会访问这些错误，回调不能监督异常会传播到余下的上下文管理器中
try:
    with contextlib.ExitStack() as stack:
        stack.callback(callback, 'arg1', 'arg2')
        stack.callback(callback, arg3='val3')
        raise RuntimeError('thrown error')
except RuntimeError as err:
    print('ERROR: {}'.format(err))
    
# output
closing callback((), {'arg3': 'val3'})
closing callback(('arg1', 'arg2'), {})
ERROR: thrown error

# 回调提供了一种便捷的方式定义清理逻辑而无需创建一个多余的新的上下文管理器类。为了提高可读性，具体逻辑也可以写在内联函数（inline function）中，callback() 也可以作为装饰器使用。把callback() 作为装饰器使用时无法给被注册的函数指定参数。不过，如果清理函数作为内联定义，作用域规则使其可以访问调用代码中被定义的变量

with contextlib.ExitStack() as stack:

    @stack.callback
    def inline_cleanup():
        print('inline_cleanup()')
        print('local_resource = {!r}'.format(local_resource))

    local_resource = 'resource created in context'
    print('within the context')
    
# output
within the context
inline_cleanup()
local_resource = 'resource created in context'
```

#### 4.6.3 局部栈——`Partial Stack`

如果上下文不能被完全构造出来，有时创建一个复杂的上下文后使用局部栈取消操作是非常有效的。同时为了延迟所有资源的清理，直到最终被一次性清理，这需要被正确设置。举个例子，如果在操作中需要多个长时间的网络连接，如果其中某一连接失效时，最好的方式是不进行这个操作。但如果所有被正确打开的连接需要单个上下文管理器在运行期间保持连接。 `ExitStack` 中的 `pop_all()` 则适用于这种情况。

`pop_all()` 会清理栈中所有的上下文管理器和回调，并返回一个包含与之前的栈相同内容的新栈。 原栈完成操作后，新栈的 `close()` 方法可以在之后执行以清理掉所有资源

```python
import contextlib

from contextlib_context_managers import *


def variable_stack(contexts):
    with contextlib.ExitStack() as stack:
        for c in contexts:
            stack.enter_context(c)
        # Return the close() method of a new stack as a clean-up
        # function.
        return stack.pop_all().close
    # Explicitly return None, indicating that the ExitStack could
    # not be initialized cleanly but that cleanup has already
    # occurred.
    return None


print('No errors:')
cleaner = variable_stack([
    HandleError(1),
    HandleError(2),
])
cleaner()

print('\nHandled error building context manager stack:')
try:
    cleaner = variable_stack([
        HandleError(1),
        ErrorOnEnter(2),
    ])
except RuntimeError as err:
    print('caught error {}'.format(err))
else:
    if cleaner is not None:
        cleaner()
    else:
        print('no cleaner returned')

print('\nUnhandled error building context manager stack:')
try:
    cleaner = variable_stack([
        PassError(1),
        ErrorOnEnter(2),
    ])
except RuntimeError as err:
    print('caught error {}'.format(err))
else:
    if cleaner is not None:
        cleaner()
    else:
        print('no cleaner returned')
        
# 这里的示例使用了之前定义好的上下文管理器类，差异在于用 ErrorOnEnter 处理 __enter__ 产生的错误，而非使用 __exit__ 方法来处理。在 variable_stack 内部，如果所有的上下文都被传递进去而且没有产生错误， 新的 ExitStack 中的 close 方法将被返回。如果错误被处理了，variable_stack 将返回一个 None，来指明清理工作已完成。如果是错误未被处理，局部栈将被清理，并且错误将被传播

# output

No errors:
  HandleError(1): entering
  HandleError(2): entering
  HandleError(2): exiting False
  HandleError(1): exiting False

Handled error building context manager stack:
  HandleError(1): entering
  ErrorOnEnter(2): throwing error on enter
  HandleError(1): handling exception RuntimeError('from 2',)
  HandleError(1): exiting True
no cleaner returned

Unhandled error building context manager stack:
  PassError(1): entering
  ErrorOnEnter(2): throwing error on enter
  PassError(1): passing exception RuntimeError('from 2',)
  PassError(1): exiting
caught error from 2
```





## 参考

1. [面向侧面的程序设计](https://zh.wikipedia.org/wiki/%E9%9D%A2%E5%90%91%E4%BE%A7%E9%9D%A2%E7%9A%84%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1) 

2. [Rich comparison methods](https://docs.python.org/reference/datamodel.html#object.__lt__) 描述了富比较方法的参考指导

3. [Isolated @memoize](http://nedbatchelder.com/blog/201601/isolated_memoize.html) 是针对单元测试（**Unit Tests**）的内存管理装饰符。

   因为函数调用是非常昂贵的，当面对处理同样的输入期望得到同样的结果的时候，可以采用 `meomize` 装饰符来处理这类问题。通常使用缓存来快速返回结果，如果之前已经进行过相同的运算。实际是模拟缓存方式

   ```python
   # 这里写了一个函数来进行模拟缓存，虽然解决了函数调用开销的问题，但是因为 cache 使用的是
   # 字典，它具有 ”global“ 变量的特点，具有潜在风险
   def memoize(func):
       cache = {}
   
       def memoizer(*args, **kwargs):
           key = str(args) + str(kwargs)
           if key not in cache:
               cache[key] = func(*args, **kwargs)
           return cache[key]
   
       return memoizer
   
   @memoize		# 这里是一个装饰器
   def expensive_fn(a, b):
       return a + b 
   
   # 下面使用了其他方案
   import functools
   
   # A list of all the memoized functions, so that
   # `clear_memoized_values` can clear them all.
   _memoized_functions = []
   
   def memoize(func):
       """Cache the value returned by a function call."""
       func = functools.lru_cache()(func)
       _memoized_functions.append(func)
       return func
   
   def clear_memoized_values():
       """Clear all the values saved by @memoize, to ensure isolated tests."""
       for func in _memoized_functions:
           func.cache_clear()
           
   # 上面的代码部分被作为 pytest.py 脚本保存
   # 这里使用了一个缓存清除机制
   @pytest.fixture(autouse=True)
   def reset_all_memoized_functions():
       """Clears the values cached by @memoize before each test."""
       clear_memoized_values()
   
   # For unittest:
   
   class MyTestCaseBase(unittest.TestCase):
       def setUp(self):
           super().setUp()
           clear_memoized_values()
   
   ```

4. [PEP 443](https://www.python.org/dev/peps/pep-0443) “Single-dispatch generic functions”

5. [The Standard ML Basis Library](http://www.standardml.org/Basis/) The library for SML.

6. [Standard ML - Wikipedia](https://en.wikipedia.org/wiki/Standard_ML) The library for SML.

7. [Standard library documentation for operator](https://docs.python.org/3.6/library/operator.html) 

8. [Inline function - Wikipedia](https://en.wikipedia.org/wiki/Inline_function) 内联函数

9. [PEP 343](https://www.python.org/dev/peps/pep-0343) 描述 `with` 语句

10. [Context Manager Types](https://docs.python.org/library/stdtypes.html#typecontextmanager) 上下文管理器 `API` 描述

11. [With Statement Context Managers](https://docs.python.org/reference/datamodel.html#context-managers) 

12. [Resource management in Python 3.3, or contextlib.ExitStack FTW!](http://www.wefearchange.org/2013/05/resource-management-in-python-33-or.html) Description of using `ExitStack` to deploy safe code from Barry Warsaw.