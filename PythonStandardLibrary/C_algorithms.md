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

* 比较序（**Collation Order**）

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

* 缓存（**Caching**）

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

* `Reducing a data set`

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

* 通用函数（**Generic Function**）

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