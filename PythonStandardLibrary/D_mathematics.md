**目录**

[TOC]

在 `Python` 中涉及的数学模块，除了默认的内置类型，还有 `fractions`, `random`, `math`, `decimal` 以及 `statistics`。需要注意⚠️ `Python` 的浮点数是 `double` 形式的。

## 1. `Decimal`——定长和浮点数运算

它提供了大众熟悉的运算模式，而非 `IEEE` 运算模式——特别是在浮点数方面。

```python
"BasicContext", "Clamped", "Context", "ConversionSyntax", "Decimal", "DecimalException", "DecimalTuple", "DefaultContext", "DivisionByZero", "DivisionImpossible", "DivisionUndefined", "ExtendedContext", "FloatOperation", "HAVE_THREADS", "Inexact", "InvalidContext", "InvalidOperation", "MAX_EMAX", "MAX_PREC", "MIN_EMIN", "MIN_ETINY", "Overflow", "ROUND_05UP", "ROUND_CEILING", "ROUND_DOWN", "ROUND_FLOOR", "ROUND_HALF_DOWN", "ROUND_HALF_EVEN", "ROUND_HALF_UP", "ROUND_UP", "Rounded", "Subnormal", "Underflow", "__builtins__", "__cached__", "__doc__", "__file__", "__libmpdec_version__", "__loader__", "__name__", "__package__", "__spec__", "__version__", "getcontext", "localcontext", "setcontext"
```

### 1.1 `Decimal` 创建浮点数和数学运算

可以通过 `Decimal` 类创建浮点数，传入的是一个元组——第一个是符号标识（0 表示正，1 表示负），数字元组，指数幂次整数值（其实是一个 10 的指数）。使用这种方式的重要作用是导出小数值不会损失精度，另外数据值使用元组的形式保存方便网络传输，最重要的是在不支持小数值的数据库中存储数据以便后续被转换为浮点数

```python
import decimal

# Tuple
t = (1, (1, 1), -3)
print('Input  :', t)
print('Decimal:', decimal.Decimal(t))

# output
Decimal('-0.011')

# 除了可以使用元组形式穿件，还可以传入字符串数值进行创建
decimal.Decimal('3.2')
# output
Decimal('3.2')
```

在数学运算方面，需要注意⚠️ `Decimal` 类型数据可以和整数进行直接运算，但是浮点数不能直接运算。

```python
a = decimal.Decimal('3.14')
c = 4
d = 3.14

print(a + c)
try:
    print(a + d)
except TypeError as e:
    print(e)
    
# output
7.14
unsupported operand type(s) for +: 'decimal.Decimal' and 'float'
```

### 1.2 上下文——`Context`

`decimal` 模块中，精度、取整以及错误处理等行为可以被修改的。这需要使用上下文覆盖设置，可以通过 `getcontext` 方法来得到当前的全局上下文

```python
import decimal

context = decimal.getcontext()

print('Emax     =', context.Emax)
print('Emin     =', context.Emin)
print('capitals =', context.capitals)
print('prec     =', context.prec)
print('rounding =', context.rounding)
print('flags    =')
for f, v in context.flags.items():
    print('  {}: {}'.format(f, v))
print('traps    =')
for t, v in context.traps.items():
    print('  {}: {}'.format(t, v))
    
# output
Emax     = 999999
Emin     = -999999
capitals = 1
prec     = 28
rounding = ROUND_HALF_EVEN
flags    =
  <class 'decimal.InvalidOperation'>: False
  <class 'decimal.FloatOperation'>: False
  <class 'decimal.DivisionByZero'>: False
  <class 'decimal.Overflow'>: False
  <class 'decimal.Underflow'>: False
  <class 'decimal.Subnormal'>: False
  <class 'decimal.Inexact'>: False
  <class 'decimal.Rounded'>: False
  <class 'decimal.Clamped'>: False
traps    =
  <class 'decimal.InvalidOperation'>: True
  <class 'decimal.FloatOperation'>: False
  <class 'decimal.DivisionByZero'>: True
  <class 'decimal.Overflow'>: True
  <class 'decimal.Underflow'>: False
  <class 'decimal.Subnormal'>: False
  <class 'decimal.Inexact'>: False
  <class 'decimal.Rounded'>: False
  <class 'decimal.Clamped'>: False
```

#### 1.2.1 精度调整

对 `prec` 进行调整，可以控制精度，字面量值（**Literal Values**）将按照该属性值表示。

```python
import decimal

d = decimal.Decimal('0.123456')

for i in range(1, 5):
    decimal.getcontext().prec = i		# 这里更改了精度属性
    print(i, ':', d, d * 1)
    
# output
1 : 0.123456 0.1
2 : 0.123456 0.12
3 : 0.123456 0.123
4 : 0.123456 0.1235
```

#### 1.2.2 取整

可以使用多种方法进行取整，以保证值在所需的精度范围内。

| 类型              | 解释                                                         |
| ----------------- | ------------------------------------------------------------ |
| `ROUND_CEILING`   | 总是趋向无穷大向上取整                                       |
| `ROUND_DOWN`      | 总是趋向 0 取整                                              |
| `ROUND_FLOOR`     | 总是趋向负无穷大向下取整                                     |
| `ROUND_HALF_DOWN` | 如果最后一个有效数字大于或等于 5 则向 0 反向取整；否则向 0 取整 |
| `ROUND_HALF_EVEN` | 类似上一个，但是如果最后有效数字是 5 则检查前一位。偶数值向下取整，否则反之 |
| `ROUND_HALF_UP`   | 如果是 5 则向 0 反向取整                                     |
| `ROUND_UP`        | 向 0 的反向取整                                              |
| `ROUND_05UP`      | 最后一位是 5 或者 0，则向 0 的反向取整，否则反之             |

```python
import decimal

context = decimal.getcontext()

ROUNDING_MODES = [
    'ROUND_CEILING',
    'ROUND_DOWN',
    'ROUND_FLOOR',
    'ROUND_HALF_DOWN',
    'ROUND_HALF_EVEN',
    'ROUND_HALF_UP',
    'ROUND_UP',
    'ROUND_05UP',
]

header_fmt = '{:10} ' + ' '.join(['{:^8}'] * 6)

print(header_fmt.format(
    ' ',
    '1/8 (1)', '-1/8 (1)',
    '1/8 (2)', '-1/8 (2)',
    '1/8 (3)', '-1/8 (3)',
))
for rounding_mode in ROUNDING_MODES:
    print('{0:10}'.format(rounding_mode.partition('_')[-1]),
          end=' ')
    for precision in [1, 2, 3]:
        context.prec = precision
        context.rounding = getattr(decimal, rounding_mode)
        value = decimal.Decimal(1) / decimal.Decimal(8)
        print('{0:^8}'.format(value), end=' ')
        value = decimal.Decimal(-1) / decimal.Decimal(8)
        print('{0:^8}'.format(value), end=' ')
    print()
    
# output
           1/8 (1)  -1/8 (1) 1/8 (2)  -1/8 (2) 1/8 (3)  -1/8 (3)
CEILING      0.2      -0.1     0.13    -0.12    0.125    -0.125

DOWN         0.1      -0.1     0.12    -0.12    0.125    -0.125

FLOOR        0.1      -0.2     0.12    -0.13    0.125    -0.125

HALF_DOWN    0.1      -0.1     0.12    -0.12    0.125    -0.125

HALF_EVEN    0.1      -0.1     0.12    -0.12    0.125    -0.125

HALF_UP      0.1      -0.1     0.13    -0.13    0.125    -0.125

UP           0.2      -0.2     0.13    -0.13    0.125    -0.125

05UP         0.1      -0.1     0.12    -0.12    0.125    -0.125
```

#### 1.2.3 本地上下文——`Local Context`

这个是使用 `with` 语句的方式，进行代码块控制。需要使用 `context` 的上下文管理 `API` 

```python
with decimal.localcontext() as c:		# 使用 localcontext 来管理本地上下文
    c.prec = 2
    print('Local precision:', c.prec)
    print('3.14 / 3 =', (decimal.Decimal('3.14') / 3))

print()
print('Default precision:', decimal.getcontext().prec)
print('3.14 / 3 =', (decimal.Decimal('3.14') / 3))

# output
Local precision: 2
3.14 / 3 = 1.0

Default precision: 28
3.14 / 3 = 1.046666666666666666666666667
```

#### 1.2.4 各实例上下文——`Per-Instance Context`

上下文可以通过实例来创建，这样可以只修改对应的实例下的属性。

````python
import decimal

# Set up a context with limited precision
c = decimal.getcontext().copy()
c.prec = 3

# Create our constant
pi = c.create_decimal('3.1415')

# The constant value is rounded off
print('PI    :', pi)

# The result of using the constant uses the global context
print('RESULT:', decimal.Decimal('2.01') * pi)

# output
PI    : 3.14
RESULT: 6.3114
````

#### 1.2.5 线程——`Threads`

“全局”上下文实际是线程本地上下文，所以完全可以使用不同的值来分配给各个线程。下面的例子是使用指定的值创建新的上下文，之后运用到各个线程中。

```python
import decimal
import threading
from queue import PriorityQueue


class Multiplier(threading.Thread):
    def __init__(self, a, b, prec, q):
        self.a = a
        self.b = b
        self.prec = prec
        self.q = q
        threading.Thread.__init__(self)

    def run(self):
        c = decimal.getcontext().copy()
        c.prec = self.prec
        decimal.setcontext(c)
        self.q.put((self.prec, a * b))


a = decimal.Decimal('3.14')
b = decimal.Decimal('1.234')
# A PriorityQueue will return values sorted by precision,
# no matter what order the threads finish.
q = PriorityQueue()
threads = [Multiplier(a, b, i, q) for i in range(1, 6)]
for t in threads:
    t.start()

for t in threads:
    t.join()

for i in range(5):
    prec, value = q.get()
    print('{}  {}'.format(prec, value))

# output
1  4
2  3.9
3  3.87
4  3.875
5  3.8748
```



## 参考

1. [Floating Point Arithmetic: Issues and Limitations](https://docs.python.org/tutorial/floatingpoint.html) Article from the Python tutorial describing floating point math representation issues.
2. [Wikipedia: Floating Point](https://en.wikipedia.org/wiki/Floating_point) Article on floating point representations and arithmetic.