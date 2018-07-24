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

## 2. `Random` ——伪随机数生成器

`random` 模块是基于`Mersenne Twister` 算法提供的一个快速为随机数生成器——它的目的是向蒙特卡洛模拟生成输入，它是一个大周期的近均匀分布的数，以适用于各种类型的应用。

### 2.1 保存状态——`Saving State`

`random` 使用的伪随机算法的内部状态可以保存，并用于控制后续各轮生成的随机数，继续生成随机数之前回复前一个状态，这会减少由之前输入得到的重复的值或值序列的可能性。`getstate` 方法会返回一些数据，以后可以使用 `setstate` 方法利用这些数据重新初始化伪随机数生成器。下面的例子中 `getstate` 方法返回的数据是一个实现细节，所以这个例子用 `pickle` 将数据保存到一个文件中，不过可以把它当作一个黑盒。如果程序开始时这个文件存在，则加载原来的状态并继续。而且每次运行时都会在保存状态之前以及之后生成一些数，以展示恢复状态会导致生成器再次生成同样的值。

```python
import random
import os
import pickle

if os.path.exists('state.dat'):
    # Restore the previously saved state
    print('Found state.dat, initializing random module')
    with open('state.dat', 'rb') as f:
        state = pickle.load(f)
    random.setstate(state)
else:
    # Use a well-known start state
    print('No state.dat, seeding')
    random.seed(1)

# Produce random values
for i in range(3):
    print('{:04.3f}'.format(random.random()), end=' ')
print()

# Save state for next time
with open('state.dat', 'wb') as f:
    pickle.dump(random.getstate(), f)

# Produce more random values
print('\nAfter saving state:')
for i in range(3):
    print('{:04.3f}'.format(random.random()), end=' ')
print()

# output
No state.dat, seeding
0.134 0.847 0.764

After saving state:
0.255 0.495 0.449

# 这是第二次运行的结果
Found state.dat, initializing random module
0.255 0.495 0.449

After saving state:
0.652 0.789 0.094
```

### 2.2 多个并发生成器

除了模块级函数，`random` 还包括一个 `Random` 类管理多个随机数生成器的内部状态。其他函数都可以作为 `Random` 实例的方法得到，并且各个实例可以单独初始化和使用，而不会与其他示例返回的值相互干扰。如果系统设置了很好的内置随机值种子，不同实例会有唯一的初始状态。如果没有一个好的平台随机值生成器，不同的 实例会使用当前时间作为种子，这样就会生成相同的值。

```python
import random
import time

print('Default initializiation:\n')

r1 = random.Random()
r2 = random.Random()

for i in range(3):
    print('{:04.3f}  {:04.3f}'.format(r1.random(), r2.random()))

print('\nSame seed:\n')

seed = time.time()
r1 = random.Random(seed)
r2 = random.Random(seed)

for i in range(3):
    print('{:04.3f}  {:04.3f}'.format(r1.random(), r2.random()))
    
# output
0.862  0.390
0.833  0.624
0.252  0.080

Same seed:

0.466  0.466
0.682  0.682
0.407  0.407

# 另外可以使用系统随机数生成器，需要使用 os.urandom 方法来生成值。下面的方式使用 random 库中 SystemRandom 方法来调用系统随机数生成器。需要注意的是 SystemRandom 产生的序列是不可再生的，因为其随机性来自系统，而非软件状态，所以 seed 和 setstate 方法将不起作用
print('Default initializiation:\n')

r1 = random.SystemRandom()
r2 = random.SystemRandom()

for i in range(3):
    print('{:04.3f}  {:04.3f}'.format(r1.random(), r2.random()))

print('\nSame seed:\n')

seed = time.time()
r1 = random.SystemRandom(seed)
r2 = random.SystemRandom(seed)

for i in range(3):
    print('{:04.3f}  {:04.3f}'.format(r1.random(), r2.random()))
```

### 2.3 其他分布的随机模拟

`random` 方法生成的值是**均匀分布的**，但是对于特定的情况需要不同的建模。

* 正太分布

  用于非均匀的连续值建模，例如梯度、高度、重量等。`random` 中包括两个函数的可以生成正太分布，分别是  `normalvariate` 和 `gauss` 方法

* 近似分布

  三角分布（**Triangular Distribution**）常被用于 **小样本** 的近似分布（**Approximation distribution**）。三角分布的“曲线”中，低点在已知的最小和最大值，在模式值处有一个高点——主要根据“最接近”的结果来估计，需要由 `triangular` 方法的模式参数来反应。关于三角分布见[Triangular distribution - Wikipedia](https://en.wikipedia.org/wiki/Triangular_distribution) 

* 指数分布

  `expovariate` 方法可以生成一个指数分布，这对于模拟到达或间隔时间值中的泊松过程会非常有用，实际的例子如放射衰变速度或到达 `Web` 服务器的请求。

  其他的观察实例如帕累托分布和幂律分布，在“长尾效应”中很普遍。使用 `paretovariate` 方法模拟资源分配（例如财富分配，音乐家的需求，对博客的关注）

* 角分布

  角分布（**Angular Distribution**），即米塞斯（`von Mises`）分布或圆正太分布用于计算周期值的概率，例如角度、日历日期和时间。可以使用 `vonmisesvariate` 方法生成。

* 大小分布（**Size Distribution**）

  `betavariate` 方法生成 $\beta$ 分布的值，常用于贝叶斯统计和应用，如任务持续时间建模。`gammavariate` 方法生成 $\gamma$ 分布，用于对事物的大小建模，例如等待时间、雨量和计算错误。`weibullvariate` 方法可以生成韦伯分布用于鼓掌分析、工业工程和天气预报。可以描述例子或其他离散对象的大小分布。

## 参考

1. [Floating Point Arithmetic: Issues and Limitations](https://docs.python.org/tutorial/floatingpoint.html) Article from the Python tutorial describing floating point math representation issues.

2. [Wikipedia: Floating Point](https://en.wikipedia.org/wiki/Floating_point) Article on floating point representations and arithmetic.

3. [Standard library documentation for fractions](https://docs.python.org/3.6/library/fractions.html) `fractions` 模块是 `decimal` 模块的另一种方法，在对分数处理的方面可以进行单独的分子和分母进行表示。另外其实例化创建对象时，可以使用字符串

   ```python
   import fractions
   
   for n, d in [(1, 2), (2, 4), (3, 6)]:
       f = fractions.Fraction(n, d)	# 这是使用分子和分母的表示方法，来表示无理数
       print('{}/{} = {}'.format(n, d, f))
       
   # output
   1/2 = 1/2
   2/4 = 1/2
   3/6 = 1/2
   
   # 通过字符串的形式来实例化对象
   for s in ['1/2', '2/4', '3/6']:
       f = fractions.Fraction(s)
       print('{} = {}'.format(s, f))
       
   # output
   1/2 = 1/2
   2/4 = 1/2
   3/6 = 1/2
   
   # 下面是使用小数进行分子分母拆分处理
   for s in ['0.5', '1.5', '2.0', '5e-1']:
       f = fractions.Fraction(s)
       print('{0:>4} = {1}'.format(s, f))
       
   # output
    0.5 = 1/2
    1.5 = 3/2
    2.0 = 2
   5e-1 = 1/2
   
   # 通过浮点点数来进行实例化，而非字符串的话，可能会产生一定的问题——因为浮点数不能被准确表达
   for v in [0.1, 0.5, 1.5, 2.0]:
       print('{} = {}'.format(v, fractions.Fraction(v)))
       
   # output
   0.1 = 3602879701896397/36028797018963968	# 这个结果就说明了浮点数表达的问题
   0.5 = 1/2
   1.5 = 3/2
   2.0 = 2
   ```

4. [Wikipedia: Mersenne Twister](https://en.wikipedia.org/wiki/Mersenne_twister) Article about the pseudorandom generator algorithm used by Python