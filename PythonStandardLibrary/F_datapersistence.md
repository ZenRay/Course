**目录**

[TOC]

数据的持久存储和交换，包括内存中对象和持久保存格式之间的来回转换，以及处理转换后数据的存储。主要由两个模块可以将对象转换为一种可以传输和存储的格式——这个转换的过程是序列化（**Serializing**）。其中 `pickle` 多用于存储，这是因为它可以集成到其他可以存储序列化数据的标准库中（例如 `shelve`）。`JSON` 是另一个常用于基于 web 的应用（**web-based application**），这是因为它和现有的 web 服务存储工具整合良好。

一旦内存对象被转换为可以被存储的格式，下一步就是需要确认怎么存储数据。如果数据不需要以某种方式索引，那么依序先后写入序列化对象的简单平面文件（**flat-file**，这类文件主要是文件格式，且文件之间是独立的。例如 `CSV` 文件）就很适用。`Python` 中有一组模块可以在一个简单的数据库中存储键值对，需要索引查找时会使用某种变种的 `DBM` 格式。

在使用 `DBM` 格式方式中，最直接的的方式是使用 `shelve`，访问一个打开的 `shelve` 文件可以通过类似字典 `API` 来进行访问。而且保存到数据库的对象会自动 `pickle` 并保存，而无须调用其他方法。但是也存在一个缺点，使用默认接口时没有办法预测将要使用哪一个 `DBM` 格式，所以在涉及到移植性时需要将用模块中特定的类来确保选用特定的格式。

对于已经使用 `JSON` 数据的 web 应用，`json` 和 `dbm` 提供了另一种持久化机制。直接使用 `dbm` 比 `shelve` 需要多一点工作，因为 `DBM` 数据库中键和值必须是字符串，并且值在访问时不会自动重新创建。



## 1. `pickle` 对象序列化

一旦数据被序列化，你就可以把它写入到文件、socket、管道等等中。之后可以读取这个文件，反序列化这些数据来构造具有相同值的新对象。

```python
"ADDITEMS", "APPEND", "APPENDS", "BINBYTES", "BINBYTES8", "BINFLOAT", "BINGET", "BININT", "BININT1", "BININT2", "BINPERSID", "BINPUT", "BINSTRING", "BINUNICODE", "BINUNICODE8", "BUILD", "DEFAULT_PROTOCOL", "DICT", "DUP", "EMPTY_DICT", "EMPTY_LIST", "EMPTY_SET", "EMPTY_TUPLE", "EXT1", "EXT2", "EXT4", "FALSE", "FLOAT", "FRAME", "FROZENSET", "FunctionType", "GET", "GLOBAL", "HIGHEST_PROTOCOL", "INST", "INT", "LIST", "LONG", "LONG1", "LONG4", "LONG_BINGET", "LONG_BINPUT", "MARK", "MEMOIZE", "NEWFALSE", "NEWOBJ", "NEWOBJ_EX", "NEWTRUE", "NONE", "OBJ", "PERSID", "POP", "POP_MARK", "PROTO", "PUT", "PickleError", "Pickler", "PicklingError", "PyStringMap", "REDUCE", "SETITEM", "SETITEMS", "SHORT_BINBYTES", "SHORT_BINSTRING", "SHORT_BINUNICODE", "STACK_GLOBAL", "STOP", "STRING", "TRUE", "TUPLE", "TUPLE1", "TUPLE2", "TUPLE3", "UNICODE", "Unpickler", "UnpicklingError", "_Framer", "_Pickler", "_Stop", "_Unframer", "_Unpickler", "__all__", "__builtins__", "__cached__", "__doc__", "__file__", "__loader__", "__name__", "__package__", "__spec__", "_compat_pickle", "_dump", "_dumps", "_extension_cache", "_extension_registry", "_getattribute", "_inverted_registry", "_load", "_loads", "_test", "_tuplesize2code", "bytes_types", "codecs", "compatible_formats", "decode_long", "dispatch_table", "dump", "dumps", "encode_long", "format_version", "io", "islice", "load", "loads", "maxsize", "pack", "partial", "re", "sys", "unpack", "whichmodule"
```

这里可以使用 `dumps` 和 `loads` 方法，它们两者是直接将对象进行序列化和反序列化。需要注意⚠️反序列化后的数据与源数据相等，但是并不是之前的对象。

```python
import pickle
import pprint

data1 = [{'a': 'A', 'b': 2, 'c': 3.0}]
# 这里是直接打印出了序列化对象和原始对象
print('DATA:', end=' ')
pprint.pprint(data)

data_string = pickle.dumps(data)
print('PICKLE: {!r}'.format(data_string)

# output
DATA: [{'a': 'A', 'b': 2, 'c': 3.0}]
PICKLE: b'\x80\x03]q\x00}q\x01(X\x01\x00\x00\x00cq\x02G@\x08\x00
\x00\x00\x00\x00\x00X\x01\x00\x00\x00bq\x03K\x02X\x01\x00\x00\x0
0aq\x04X\x01\x00\x00\x00Aq\x05ua.'

# 下面主要是为了说明序列化和反序列化后数据的差异
print('BEFORE: ', end=' ')
pprint.pprint(data1)

data1_string = pickle.dumps(data1)

data2 = pickle.loads(data1_string)
print('AFTER : ', end=' ')
pprint.pprint(data2)

print('SAME? :', (data1 is data2))
print('EQUAL?:', (data1 == data2))

# output
BEFORE:  [{'a': 'A', 'b': 2, 'c': 3.0}]
AFTER :  [{'a': 'A', 'b': 2, 'c': 3.0}]
SAME? : False
EQUAL?: True
```

⚠️：`pickle` 的文档清晰的表明它不提供安全保证。实际上，反序列化后可以执行任意代码，所以慎用 `pickle`来作为内部进程通信或者数据存储，也不要相信那些你不能验证安全性的数据。请参阅 `hmac`模块，它提供了一个以安全方式验证序列化数据源的示例。

### 1.1 流序列化处理

`pickle`  除了提供  `dumps` 和  `loads` ，还提供了非常方便的函数用于操作文件流。支持同时写多个对象到同一个流中，然后在不知道有多少个对象或不知道它们有多大时，能够从这个流中读取到这些对象。需要注意另外的两个方法 `dump` 和 `load` ，它们是将序列化对象保存到文件或者从文件中读取内容。

下面的例子中使用两个 `BytesIO` 缓冲区来模拟流。一个接收序列化对象，另一个通过 `load` 方法读取第一个的值。一个简单的数据库格式也可以使用序列化来存储对象。 `shelve` 模块就是按照这个方式来处理数据。

```python
import io
import pickle
import pprint


class SimpleObject:

    def __init__(self, name):
        self.name = name
        self.name_backwards = name[::-1]
        return


data = []
data.append(SimpleObject('pickle'))
data.append(SimpleObject('preserve'))
data.append(SimpleObject('last'))

# Simulate a file.
out_s = io.BytesIO()

# Write to the stream
for o in data:
    print('WRITING : {} ({})'.format(o.name, o.name_backwards))
    pickle.dump(o, out_s)
    out_s.flush()

# Set up a read-able stream
in_s = io.BytesIO(out_s.getvalue())

# Read the data
while True:
    try:
        o = pickle.load(in_s)
    except EOFError:
        break
    else:
        print('READ    : {} ({})'.format(
            o.name, o.name_backwards))
        
# output
WRITING : pickle (elkcip)
WRITING : preserve (evreserp)
WRITING : last (tsal)
READ    : pickle (elkcip)
READ    : preserve (evreserp)
READ    : last (tsal)
```

除了用于存储数据，序列化在用于内部进程通信时也是非常灵活的。比如，使用  `os.fork()` 和 `os.pipe()` ，可以建立一些工作进程，它们从一个管道中读取任务说明并把结果输出到另一个管道。操作这些工作池、发送任务和接受返回的核心代码可以复用，因为任务和返回对象不是一个特殊的类。如果使用管道或者套接字，就不要忘记在序列化每个对象后刷新它们，并通过它们之间的连接将数据推送到另外一端。查看`multiprocessing` 模块构建一个可复用的任务池管理器

### 1.2 对象重构问题

当一个自定义类的对象被保存后，如果没有将类引入加载方法的所在进程的命名空间中，将出现报错。所以为了解决这个问题需要将需要的类、方法等 `import` 到相应的文件中

```python
# pickle_dump_to_file_1.py
import pickle
import sys


class SimpleObject:

    def __init__(self, name):
        self.name = name
        l = list(name)
        l.reverse()
        self.name_backwards = ''.join(l)


if __name__ == '__main__':
    data = []
    data.append(SimpleObject('pickle'))
    data.append(SimpleObject('preserve'))
    data.append(SimpleObject('last'))

    filename = sys.argv[1]

    with open(filename, 'wb') as out_s:
        for o in data:
            print('WRITING: {} ({})'.format(
                o.name, o.name_backwards))
            pickle.dump(o, out_s)
            
# 运行脚本
$ python3 pickle_dump_to_file_1.py test.dat

WRITING: pickle (elkcip)
WRITING: preserve (evreserp)
WRITING: last (tsal)
```

上面是将文件保存 `dump` 到了 `test.dat`，下面的方法是直接进行 `load`

```python
# pickle_load_from_file_1.py
import pickle
import pprint
import sys

filename = sys.argv[1]

with open(filename, 'rb') as in_s:
    while True:
        try:
            o = pickle.load(in_s)
        except EOFError:
            break
        else:
            print('READ: {} ({})'.format(
                o.name, o.name_backwards))
                
# 运行脚本
$ python3 pickle_load_from_file_1.py test.dat

Traceback (most recent call last):
  File "pickle_load_from_file_1.py", line 15, in <module>
    o = pickle.load(in_s)
AttributeError: Can't get attribute 'SimpleObject' on <module '_
_main__' from 'pickle_load_from_file_1.py'>
```

上面的就是因为没有相应的类，而出现报错。修正这个问题需要在脚本中加入 `from pickle_dump_to_file_1 import SimpleObject` 即可

### 1.3 不可`pickle` 对象

不是所有对象都可以被序列化的，如套接字、文件句柄、数据库连接或其他运行时状态可能依赖于操作系统或其他进程的对象，则无法有效的存储下来。如果对象具有不可 `pickle` 属性，可以定义 `__getstate__` 和 `__setstate__` 方法来返回实例在被序列化时的状态。

这个 `__getstate__` 方法须返回对象，它包含该对象内部状态。一种便捷的方式是使用字典来表达状态，字典的值可以是任意可序列化的对象。当对象通过 `pickle` 加载时，状态会被存储，并且传递给 `__setstate__` 方法。下面是使用一个单独的 `State` 对象存储 `MyClass` 的内部状态。当 `MyClass` 的实例反序列化时，会给  `__setstate__` 传入一个 `State` 的实例去初始化新的对象。⚠️如果 `__getstate__()` 返回值是 false，则 `__setstate__()` 在对象反序列化时不会被调用。

```python
import pickle


class State:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'State({!r})'.format(self.__dict__)


class MyClass:

    def __init__(self, name):
        print('MyClass.__init__({})'.format(name))
        self._set_name(name)

    def _set_name(self, name):
        self.name = name
        self.computed = name[::-1]

    def __repr__(self):
        return 'MyClass({!r}) (computed={!r})'.format(
            self.name, self.computed)

    def __getstate__(self):
        state = State(self.name)
        print('__getstate__ -> {!r}'.format(state))
        return state

    def __setstate__(self, state):
        print('__setstate__({!r})'.format(state))
        self._set_name(state.name)


inst = MyClass('name here')
print('Before:', inst)

dumped = pickle.dumps(inst)

reloaded = pickle.loads(dumped)
print('After:', reloaded)

# output
MyClass.__init__(name here)
Before: MyClass('name here') (computed='ereh eman')
__getstate__ -> State({'name': 'name here'})
__setstate__(State({'name': 'name here'}))
After: MyClass('name here') (computed='ereh eman')
```



## 参考

1. 数据序列化

   将结构化数据转换成允许以共享或存储的格式，可恢复其原始结构的概念

2. [Pickle: An interesting stack language.](http://peadrop.com/blog/2007/06/18/pickle-an-interesting-stack-language/) – by Alexandre Vassalotti

3. [**PEP 3154**](https://www.python.org/dev/peps/pep-3154) – Pickle protocol version 4