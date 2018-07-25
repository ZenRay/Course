**目录**

[TOC]

* 处理文件的第一步就是要确定待处理文件的名称。Python 将文件名称表现为一个简单的字符串，同时也提供了标准的，跨平台的组件 `os.path` 来构建他们。

  `pathlib` 模块提供了一个面向对象的API用于处理系统路径。比起 `os.path` 它更方便，因为它在更高的抽象级别上运行。

  使用来自模块 `os` 的` listdir()` 查看目录内容列表，或者使用 `glob` 查找匹配指定模式的文件。

  查找文件的模式可以通过 `glob` 以及 `fnmatch` 模块，因此可以在其他上下文中使用。

* 在文件的名称被确定之后，可以用 `os.stat() `或者 `stat` 常量检查文件的其他特性，例如权限和大小。

  当一个应用需要随机访问文件内容时， `linecache` 模块可以很容易地按照行号读取内容。但是由于该文件的内容被缓存在内存中，因此要格外小心内存的消耗。

  `tempfile` 模块对于创建临时文件来存储数据的情况是非常有用的。它提供了安全可靠的创建临时文件和目录的类。文件或者目录名称保证是唯一的，由于包含了随机组件因此它们不会被容易猜出。

* 经常有这种情况，程序需要将文件当做一个整体来处理，而不用处理文件的内容。 `shutil` 模块提供了一系列高级的文件操作，例如复制文件和目录，解压缩文件等。

   `filecmp` 模块通过查看它们包含的字节来比较文件或者目录，因此，它们的格式丝毫不影响比较结果。

* 内建的 `file` 类可以用于读写本机上的可见文件。当一个程序读写大文件时，它的性能会下降很多，因为这期间涉及到多次从磁盘到内存的数据复制。使用 `mmap` 模块可以告诉操作系统使用其虚拟内存将文件内容直接映射到程序可访问的内存中，避免操作系统和 `file` 对象内部缓冲区之间的数据复制。

* 使用了 `ASCII` 中不可用字符的文本数据通常以 `Unicode` 格式保存。由于标准的 `file` 操作将文件的每个字节都表示为一个字符，因此当读取多字节的 `Unicode` 文本数据时需要额外的处理。`codecs` 模块可以自动地进行编码和解码，因此，在很多情况下都可以使用非 `ASCII` 文件，而不用对程序做任何修改。

## 1.  `pathlib` — 文件路径对象

`pathlib` 可以用于解析，构建，检测文件名和路径而不是低级的字符串操作。

```python
"EINVAL", "ENOENT", "ENOTDIR", "Path", "PosixPath", "PurePath", "PurePosixPath", "PureWindowsPath", "S_ISBLK", "S_ISCHR", "S_ISDIR", "S_ISFIFO", "S_ISLNK", "S_ISREG", "S_ISSOCK", "Sequence", "WindowsPath", "_Accessor", "_Flavour", "_NormalAccessor", "_PathParents", "_PosixFlavour", "_PreciseSelector", "_RecursiveWildcardSelector", "_Selector", "_TerminatingSelector", "_WildcardSelector", "_WindowsFlavour", "__all__", "__builtins__", "__cached__", "__doc__", "__file__", "__loader__", "__name__", "__package__", "__spec__", "_is_wildcard_pattern", "_make_selector", "_normal_accessor", "_posix_flavour", "_windows_flavour", "attrgetter", "contextmanager", "fnmatch", "functools", "io", "nt", "ntpath", "os", "posixpath", "re", "supports_symlinks", "sys", "urlquote_from_bytes"
```

### 1.1 路径表示

`pathlib` 包含了大量用于管理 `POSIX` 标准或者 `Windows` 语法的文件系统路径的类。它包含所谓的“纯“类，仅仅用于去操作字符串而不与实际的文件系统交互；也包含“具体“类，它们扩展了 `API` 以包含反映或修改本地文件系统数据的操作。

`PurePosixPath` 和 `PureWindowsPath` 可以实例化于任何的操作系统，仅仅用做处理路径名称。如果要实例化一个与真实文件系统相关的具体类，应该使用 `Path`, 它会根据当前的操作系统类型得到 `PosixPath` 或者 `WindowsPath` 的实例。 

### 1.2 创建路径

要实例化一个新路径，将一个字符串作为类的第一个参数，这个字符串是该路径对象的字符串形式。要创建一个相对于现有路径的新路径，可是使用 `/` 运算符进行扩展，该运算符的参数可以是一个字符串或者一个路径对象。正如 `root` 展示的那样，`/` 运算符仅仅是将给定的参数组合起来而已，当结果中包含父目录引用 `..`时，并没有去解析。而且，如果一个路径片段是以路径分隔符 `/` 开始，它将被作为一个新的根路径，就像 `os.apth.jon()`。额外的路径分隔符会从路径的中间移除，如同 `etc` 示例。

```python
import pathlib

usr = pathlib.PurePosixPath('/usr')
print(usr)

usr_local = usr / 'local'
print(usr_local)

usr_share = usr / pathlib.PurePosixPath('share')
print(usr_share)

root = usr / '..'
print(root)

etc = root / '/etc/'
print(etc)

# 具体路径类包含一个 resolve() 方法，它会通过查找文件系统和符号链接去生成该名称引用的规范化的绝对路径。这里的相对路径被解析成绝对路径 /usr/share。如果输入路径中包含符号链接，那么也会扩展这些符号链接以允许解析路径直接引用目标。
usr_local = pathlib.Path('/usr/local')
share = usr_local / '..' / 'share'
print(share.resolve())
# 如果要在事先不知道路径片段时构建路径，可以使用 joinpath() ，只需要将每个路径片段作为一个独立的参数传递给它。如同 / 运算符，joinpath() 创建了一个新的实例。
root = pathlib.PurePosixPath('/')
subdirs = ['usr', 'local']
usr_local = root.joinpath(*subdirs)
print(usr_local)

# 给定一个存在的路径对象，可以新建一个有细微差别的新路径，例如引用相同目录下的不同文件。可以给 with_name() 方法传递一个不同的文件名称创建一个新的路径，相比原路径只是替换掉文件部分。使用 with_suffix() 方法也可以创建一个新的路径，只是用新一个新的扩展名替换掉原来的。
ind = pathlib.PurePosixPath('source/pathlib/index.rst')
print(ind)

py = ind.with_name('pathlib_from_existing.py')
print(py)

pyc = py.with_suffix('.pyc')
print(pyc)
```

### 1.3 解析路径

`Path` 对象具有从名称中提取部分值的方法和属性。例如，`parts` 属性会生成一个基于路径分隔符解析的路径片段序列。结果序列是一个元组，反映出路径实例的不变性。有两种方式从给定的路径对象中“向上“导航文件系统层次结构。`parent` 属性引用一个包含当前路径的目录的新实例，如同 `os.path.dirname()` 的返回值。`parents` 属性生成一个父目录可迭代对象，从当前目录“向上“直到根目录。

```python
p = pathlib.PurePosixPath('/usr/local')
print(p.parts)

# 注意下面是使用 parent 属性直接输出父路径。之后遍历 parents 属性并且打印成员
p = pathlib.PurePosixPath('/usr/local/lib')

print('parent: {}'.format(p.parent))

print('\nhierarchy:')
for up in p.parents:
    print(up)
    
# 路径的其他部分可以通过路径对象的属性进行访问。name 属性包含路径最后一部分的值，即最后一个路径分隔符后面的值（等同于 os.path.basename() ）。suffix 代表扩展分隔符后面的值，stem 属性代表后缀之前的部分。尽管 suffix 和 stem 的值看起来有点像 os.path.splittext() 的结果，但是他仅仅基于 name 属性的值而不是完整的路径。
p = pathlib.PurePosixPath('./source/pathlib/pathlib_name.py')
print('path  : {}'.format(p))
print('name  : {}'.format(p.name))
print('suffix: {}'.format(p.suffix))
print('stem  : {}'.format(p.stem))
```

### 1.4 遍历文件内容

有三个访问目录列表的方法，用以发现文件系统上可用的文件名称。`iterdir()` 是一个生成器，生成目录列表中每一个文件的 `Path` 实例。需要注意⚠️如果 `Path` 不是引用一个目录，那么 `iterdir()` 将会引发 `NotADirectoryError`。

```python
import pathlib

p = pathlib.Path('.')

for f in p.iterdir():
    print(f)
    
# 可以使用 glob() 去查找到那些匹配模式的文件。
p = pathlib.Path('..')

# 这里使用了 glob 进行文件匹配。glob 处理器支持使用模式前缀 ** 进行递归查找或者直接使用 rglob()，直白地说 rglob("*.py") 等同于 glob("**/*.py")  
for f in p.glob('*.rst'):
    print(f)
    
# 例子中是从当前脚本的父目录开始，因此需要进行递归搜索才能找到匹配 pathlib_*.py 的示例文件。
for f in p.rglob('pathlib_*.py'):
    print(f)
```

### 1.5 读写文件

每个 `Path` 实例都包含了处理它引用的文件内容的方法。可以使用 `read_bytes()` 或者 `read_text()` 来即时获取文件内容。使用  `write_bytes()` 或者 `write_text()` 来写文件。可以使用 `open()` 方法打开文件获得文件描述符，而不是将文件名传递给内建的 `open()` 方法。这些便捷的方法会在打开或者写入文件之前进行类型检查，否则他们就等同于直接进行操作。

```python
f = pathlib.Path('example.txt')

f.write_bytes('This is the content'.encode('utf-8'))

with f.open('r', encoding='utf-8') as handle:
    print('read from open(): {!r}'.format(handle.read()))

print('read_text(): {!r}'.format(f.read_text('utf-8')))
```

### 1.6 操作目录和符号链接

表示不存在的目录或者符号链接的路径实例可以用于去创建与系统关联的实体。如果路径确实已经存在， `mkdir()` 将会引发 `FileExistsError` 错误。

```python
p = pathlib.Path('example_dir')

print('Creating {}'.format(p))
p.mkdir()

# 运行第二次时回报错 FileExistsError
```

可以使用 `symlink_to()` 创建一个符号链接。链接名称将会被命名为 path 实例的值并且引用传递给 `symlink_to()` 的目标。这个例子创建了一个符号链接，然后用 `resolve()` 方法读取符号链接指向的目标的名称。

```python
p = pathlib.Path('example_link')

p.symlink_to('index.rst')

print(p)
print(p.resolve().name)		# 这里使用了 resolve 方法来得到链接文件
```

### 1.7 文件类型及其检查

一个 `Path` 实例包含了几个用于去检测引用的文件类型的方法。这个例子创建了几个不同类型的文件并检测这些文件以及本地系统上可用的其他特定设备文件。`is_dir()`, `is_file()`, `is_symlink()`, `is_socket()`, `is_fifo()`, `is_block_device()` 以及  `is_char_device()` 都不需要参数。

```python
import itertools
import os
import pathlib

root = pathlib.Path('test_files')

# Clean up from previous runs.
if root.exists():
    for f in root.iterdir():
        f.unlink()
else:
    root.mkdir()

# Create test files
(root / 'file').write_text(
    'This is a regular file', encoding='utf-8')
(root / 'symlink').symlink_to('file')
os.mkfifo(str(root / 'fifo'))

# Check the file types
to_scan = itertools.chain(
    root.iterdir(),
    [pathlib.Path('/dev/disk0'),
     pathlib.Path('/dev/console')],
)
hfmt = '{:18s}' + ('  {:>5}' * 6)
print(hfmt.format('Name', 'File', 'Dir', 'Link', 'FIFO', 'Block',
                  'Character'))
print()

fmt = '{:20s}  ' + ('{!r:>5}  ' * 6)
for f in to_scan:
    print(fmt.format(
        str(f),
        f.is_file(),
        f.is_dir(),
        f.is_symlink(),
        f.is_fifo(),
        f.is_block_device(),
        f.is_char_device(),
    ))
```

### 1.8 文件属性及权限

文件的详细信息可以通过 `stat()` 或者 `lstat()` （检查符号链接状态）查看。这两个方法的返回值同 `os.stat()` 和 `os.lstat()` 一样。示例代码输出结果依赖于代码如何存放，可以通过给脚本文件传入不同的文件而观察输出结果。

```python
# pathlib_stat.py
import pathlib
import sys
import time

if len(sys.argv) == 1:
    filename = __file__
else:
    filename = sys.argv[1]

p = pathlib.Path(filename)
stat_info = p.stat()

print('{}:'.format(filename))
print('  Size:', stat_info.st_size)
print('  Permissions:', oct(stat_info.st_mode))
print('  Owner:', stat_info.st_uid)
print('  Device:', stat_info.st_dev)
print('  Created      :', time.ctime(stat_info.st_ctime))
print('  Last modified:', time.ctime(stat_info.st_mtime))
print('  Last accessed:', time.ctime(stat_info.st_atime))

# 启用时，可以使用 python pathlib_stat.py，或者传入其他文件 python pathlib_stat.py other_file.extention
```

要更简单地访问文件的用户信息，可以使用 `owner()` 和 `group() ` 方法。`stat()` 方法只是返回了数字类型的系统 `ID` ，但是 `owner()` 和 `group()` 会查找与 ID 相关的名称。`touch()` 方法于 Unix 命令 `touch` 类似，可以用于创建文件或者更新现有文件的修改时间和权限。

```python
p = pathlib.Path(file)

print('{} is owned by {}/{}'.format(p, p.owner(), p.group()))

# 下面是使用 touch 方法
p = pathlib.Path('touched')
if p.exists():
    print('already exists')
else:
    print('creating new')

p.touch()
start = p.stat()

time.sleep(1)

p.touch()
end = p.stat()

print('Start:', time.ctime(start.st_mtime))
print('End  :', time.ctime(end.st_mtime))
```

在类 `Unix` 系统上，文件权限模式可以作为整数传递给 `chmod()` 方法进行更改。权限模式值可以通过 `stat` 模块中的常量进行构造。本示例切换了用户的执行权限。

```python
import os
import pathlib
import stat

# 创建一个全新的测试文件
f = pathlib.Path('pathlib_chmod_example.txt')
if f.exists():
    f.unlink()
f.write_text('contents')

# 使用 stat 方法来检测文件权限
existing_permissions = stat.S_IMODE(f.stat().st_mode)
print('Before: {:o}'.format(existing_permissions))

# 决定用啥方法来处理
if not (existing_permissions & os.X_OK):
    print('Adding execute permission')
    new_permissions = existing_permissions | stat.S_IXUSR
else:
    print('Removing execute permission')
    # 使用 xor 来移除用户可执行权限
    new_permissions = existing_permissions ^ stat.S_IXUSR

# 修改权限，并打印修改后的权限结果
f.chmod(new_permissions)
after_permissions = stat.S_IMODE(f.stat().st_mode)
print('After: {:o}'.format(after_permissions))
```

这有两个方法用于移除文件系统上的文件或者目录。移除一个空目录可以使用 `rmdir()`。当移除的目录不存在的时候，就会引发 `FileNotFoundError` 异常。尝试删除一个非空目录也会引起错误。

```python
# 下面是删除文件
p = pathlib.Path('example_dir')

print('Removing {}'.format(p))
p.rmdir()

# 对于文件，系统链接以及其他大多数的路径类型应该使用 unlink() 
p = pathlib.Path('touched')

p.touch()

print('exists before removing:', p.exists())

p.unlink()

print('exists after removing:', p.exists())
```

## 2. `glob` ——文件名模式匹配

作用是使用 `UNIX shell`  规则查找与一个模式匹配的文件名，尽管 `glob` 的 `API` 很小，但是这个模块的功能很强大，只要程序需要查找文件系统中的名字与某模式匹配的一组文件，这里的模式可以匹配特定的扩展名、前缀或者中间都有某个共同的字符串——这样可以使用 `glob` 而不用编写特定的代码来扫描目录内容。需要注意，`glob` 模式规则与 `re` 模块使用的正则表达式规则不同，因为 `glob` 模式遵循标准的 `UNIX` 的路径扩展规则——这里只使用几个特殊字符来实现不同的通配符和字符区间；此外模式规则要应用于文件名中的段，另外路径可以是绝对路径和相对路径；`shell` 变量名和波浪线都不会扩展

```python
"__all__", "__builtins__", "__cached__", "__doc__", "__file__", "__loader__", "__name__", "__package__", "__spec__", "_glob0", "_glob1", "_glob2", "_iglob", "_ishidden", "_isrecursive", "_iterdir", "_rlistdir", "escape", "fnmatch", "glob", "glob0", "glob1", "has_magic", "iglob", "magic_check", "magic_check_bytes", "os", "re"
```

注意⚠️，在 `python 3.x` 中存在一个 `glob2` 模块，两者不是相同的。

需要注意后续需要存在如下的文件结构，如不存在则需先创建。

```python
dir
dir/file.txt
dir/file1.txt
dir/file2.txt
dir/filea.txt
dir/fileb.txt
dir/file?.txt
dir/file*.txt
dir/file[.txt
dir/subdir
dir/subdir/subfile.txt
```

### 2.1 通配符——`Wildcards`

星号（“*“) 匹配一个文件名中的 0 个或多个字符，下面的模式会匹配目录 “dir” 中的所有路径名——包括路径上的文件和目录，但是不会 **递归** 搜索目录，如果需要列出子目录的文件，需要吧子目录包括在模式中。问号（“?”）是另一个通配符，它只会匹配该位置的单个字符

```python
import glob
for name in sorted(glob.glob('dir/*')):
    print(name)
    
# output
dir/file*.txt
dir/file.txt
dir/file1.txt
dir/file2.txt
dir/file?.txt
dir/file[.txt
dir/filea.txt
dir/fileb.txt
dir/subdir
         
 # 下面的方式是罗列子目录，这里需要注意一下，如果还有另外一个字，子目录则通配符方式会匹配这两个子目录，并包含这两个子目录的文件名
 print('Named explicitly:')
for name in sorted(glob.glob('dir/subdir/*')):
    print('  {}'.format(name))

print('Named with wildcard:')
for name in sorted(glob.glob('dir/*/*')):
    print('  {}'.format(name))
         
#output
Named explicitly:
  dir/subdir/subfile.txt
Named with wildcard:
  dir/subdir/subfile.txt
         
# 下面是可以通配 file 之后具有一个字符且末尾为 .txt 结尾
for name in sorted(glob.glob('dir/file?.txt')):
    print(name)
         
# output
dir/file*.txt
dir/file1.txt
dir/file2.txt
dir/file?.txt
dir/file[.txt
dir/filea.txt
dir/fileb.txt
```

### 2.2 字符区间——`Character Ranges`

使用区间进行陪陪可以限制范围，比问号匹配范围更小，其中 `[0-9]` 可以使用 `[0123456789]`  表示。

```python
for name in sorted(glob.glob('dir/*[0-9].*')):
    print(name)
    
# output
dir/file1.txt
dir/file2.txt
```

### 2.3 逃逸元字符——`Escaping Meta-Character`

有时，需要使用特殊元字符来进行匹配，这里就需要使用 `escape` 函数来创建合适的匹配逃逸模式，这样就不会被 `glob` 扩展而是作为特殊字符来解释。

```python
specials = '?*['

for char in specials:
    pattern = 'dir/*' + glob.escape(char) + '.txt'
    print('Searching for: {!r}'.format(pattern))
    for name in sorted(glob.glob(pattern)):
        print(name)
    print()
    
# 下面是每个特殊字符来匹配的方式
# output
Searching for: 'dir/*[?].txt'
dir/file?.txt

Searching for: 'dir/*[*].txt'
dir/file*.txt

Searching for: 'dir/*[[].txt'
dir/file[.txt
```

## 3. `fnmatch`—— `Unix` 风格的 `Glob` 模式匹配

作用是以 `Unix` 方式的进行文件名比较，`fnmatch` 用于比较针对 `Unix shell` 所使用的 `glob-style` 模式的文件名。

```python
"__all__", "__builtins__", "__cached__", "__doc__", "__file__", "__loader__", "__name__", "__package__", "__spec__", "_compile_pattern", "filter", "fnmatch", "fnmatchcase", "functools", "os", "posixpath", "re", "translate"
```

### 3.1 简单匹配

`fnmatch` 方法将模式与单一文件名进行比较，且返回一个 `bool` 值表示它们是否匹配。比较是否大小写敏感依赖于操作系统是否使用了大小写敏感的文件系统。但是可以强制进行大小写敏感方式比较，而忽略操作系统系统设置，应该使用 `fnmatchcase` 方法

```python
import fnmatch
import os

pattern = 'fnmatch_*.py'
print('Pattern :', pattern)
print()

files = os.listdir('.')
for name in sorted(files):
    print('Filename: {:<25} {}'.format(
        name, fnmatch.fnmatch(name, pattern)))

# output
Pattern : fnmatch_*.py

Filename: fnmatch_filter.py         True
Filename: fnmatch_fnmatch.py        True
Filename: fnmatch_fnmatchcase.py    True
Filename: fnmatch_translate.py      True
Filename: index.rst                 False
    
# 下面是进行大小写敏感方式匹配
pattern = 'FNMATCH_*.PY'
print('Pattern :', pattern)
print()

for name in sorted(files):
    print('Filename: {:<25} {}'.format(
        name, fnmatch.fnmatchcase(name, pattern)))
    
# output
Pattern : FNMATCH_*.PY

Filename: fnmatch_filter.py         False
Filename: fnmatch_fnmatch.py        False
Filename: fnmatch_fnmatchcase.py    False
Filename: fnmatch_translate.py      False
Filename: index.rst                 False
```

### 3.2 筛选——`filtering`

为了检查一个文件名序列，使用 `filter` 方法，它将返回一个匹配模式参数的文件名**列表**。

```python
import fnmatch
import os
import pprint

pattern = 'fnmatch_*.py'
print('Pattern :', pattern)

files = list(sorted(os.listdir('.')))

print('\nFiles   :')
pprint.pprint(files)

print('\nMatches :')
pprint.pprint(fnmatch.filter(files, pattern))

# output
Pattern : fnmatch_*.py

Files   :
['fnmatch_filter.py',
 'fnmatch_fnmatch.py',
 'fnmatch_fnmatchcase.py',
 'fnmatch_translate.py',
 'index.rst']

Matches :
['fnmatch_filter.py',
 'fnmatch_fnmatch.py',
 'fnmatch_fnmatchcase.py',
 'fnmatch_translate.py']
```

### 3.3 翻译模式——`translating pattern`

`fnmatch` 方法将 `glob` 模式转为一个正则表达式，然后使用  `re` 模块比较文件名和模式。`translate` 方法是一个公共的 `API` 用于将 `glob` 模式转换为正则表达式。使用 `translate` 更有效，它将匹配模式转换为可用的正则表达式模式。

```python
import fnmatch

pattern = 'fnmatch_*.py'
print('Pattern :', pattern)
print('Regex   :', fnmatch.translate(pattern))

# output
Pattern : fnmatch_*.py
Regex   : (?s:fnmatch_.*\.py)\Z
```

## 4. `tempfile` ——临时文件系统对象

作用是创建临时文件系统对象，可以安全地创建具有唯一名称的临时文件，以防止被试图破坏应用或窃取数据的人猜出。`TemporaryFile` 方法可以打开并返回一个未命名的文件，`NamedTemporaryFile` 方法打开并返回一个命名文件，`mkdtemp` 方法可以创建一个临时目录并返回其目录名。

```python
"NamedTemporaryFile", "SpooledTemporaryFile", "TMP_MAX", "TemporaryDirectory", "TemporaryFile", "_O_TMPFILE_WORKS", "_Random", "_RandomNameSequence", "_TemporaryFileCloser", "_TemporaryFileWrapper", "__all__", "__builtins__", "__cached__", "__doc__", "__file__", "__loader__", "__name__", "__package__", "__spec__", "_allocate_lock", "_bin_openflags", "_candidate_tempdir_list", "_errno", "_exists", "_functools", "_get_candidate_names", "_get_default_tempdir", "_infer_return_type", "_io", "_mkstemp_inner", "_name_sequence", "_once_lock", "_os", "_sanitize_params", "_shutil", "_stat", "_text_openflags", "_thread", "_warnings", "_weakref", "gettempdir", "gettempdirb", "gettempprefix", "gettempprefixb", "mkdtemp", "mkstemp", "mktemp", "tempdir", "template"
```

### 4.1 临时文件

如果需要临时文件来存储数据，而且不需要与其他程序共享数据，则可以使用 `TemporaryFile` 方法来创建文件。这个方法会在平台支持的地方创建一个文件，并会立即断开链接。这样其他程序就不可能找到活打开这个文件，因为**文件系统表中没有该文件的引用**。另外此文件调用 `close` 方法还是上下文管理的方式，在文件关闭时都会自动删除

```python
import os
import tempfile

print('Building a filename with PID:')
filename = '/tmp/guess_my_name.{}.txt'.format(os.getpid())
with open(filename, 'w+b') as temp:
    print('temp:')
    print('  {!r}'.format(temp))
    print('temp.name:')
    print('  {!r}'.format(temp.name))

# Clean up the temporary file yourself.
os.remove(filename)

print()
print('TemporaryFile:')
with tempfile.TemporaryFile() as temp:
    print('temp:')
    print('  {!r}'.format(temp))
    print('temp.name:')
    print('  {!r}'.format(temp.name))

# 这个例子展示了采用不同方法创建临时文件的差别，其中使用 TemporaryFile 创建的文件没有名字
# output
Building a filename with PID:
temp:
  <_io.BufferedRandom name='/tmp/guess_my_name.12151.txt'>
temp.name:
  '/tmp/guess_my_name.12151.txt'

TemporaryFile:
temp:
  <_io.BufferedRandom name=4>
temp.name:
  4

# 另外默认的这种方式的文件时 w+b 的，所有可以进行全平台的读取和写入
with tempfile.TemporaryFile() as temp:
    temp.write(b'Some data')

    temp.seek(0)	# 这里需要注意⚠️在读写数据之后，如果需要回转文件句柄，需要使用 seek
    print(temp.read())
   
# output
b'Some data'

# 另外还可以将文件使用文本模式打开文件，那么需要传入参数 w+t
with tempfile.TemporaryFile(mode='w+t') as f:
    f.writelines(['first\n', 'second\n'])

    f.seek(0)
    for line in f:
        print(line.rstrip()
          
# output
first
second
```

### 4.2 命名文件——`Named Files`

有些时候，需要有一个命名的临时文件，例如对于跨多个进程甚至主机的应用，为文件命名时在应用不同部分之间传递文件的最简单的方法。`NamedTemporaryFile` 方法会创建文件，但不会断开链接，所以会保留其文件名。当然在处理完全之后，文件也会被删除

```python
import os
import pathlib
import tempfile

with tempfile.NamedTemporaryFile() as temp:
    print('temp:')
    print('  {!r}'.format(temp))
    print('temp.name:')
    print('  {!r}'.format(temp.name))

    f = pathlib.Path(temp.name)

print('Exists after close:', f.exists())
# output
temp:
  <tempfile._TemporaryFileWrapper object at 0x1011b2d30>
temp.name:
  '/var/folders/5q/8gk0wq888xlggz008k8dr7180000hg/T/tmps4qh5zde'
Exists after close: False
```

### 4.3 缓冲文件——`Spooled Files`

因为临时文件只能保存相对少量的数据，，因此使用 `SpooledTemporaryFile` 可能效率更高，因为它在内容数量超过阈值之前，使用 `io.BytesIO` 或者 `io.StringIO` 将数据保存到内存中。当数据量超过阈值之后，数据将会被写入磁盘保存，与此同时，缓冲池也会被替换为 `TemporaryFile()`。

```python
import tempfile

with tempfile.SpooledTemporaryFile(max_size=100,
                                   mode='w+t',
                                   encoding='utf-8') as temp:
    print('temp: {!r}'.format(temp))

    for i in range(3):
        temp.write('This line is repeated over and over.\n')
        print(temp._rolled, temp._file)
        
# 例子中使用了 SpooledTemporaryFile 的私有属性去检测数据何时写入到磁盘。除非调整缓冲区大小，通常是没必要的去检测这个状态
# output
temp: <tempfile.SpooledTemporaryFile object at 0x1007b2c88>
False <_io.StringIO object at 0x1007a3d38>
False <_io.StringIO object at 0x1007a3d38>
True <_io.TextIOWrapper name=4 mode='w+t' encoding='utf-8'>

# 显式调用  rollover()  或者  fileno() 方法将数据写入到磁盘。例子中，因为缓冲池容量远大于数据量，除非显式调用 rollover()  否则不会创建文件
with tempfile.SpooledTemporaryFile(max_size=1000,
                                   mode='w+t',
                                   encoding='utf-8') as temp:
    print('temp: {!r}'.format(temp))

    for i in range(3):
        temp.write('This line is repeated over and over.\n')
        print(temp._rolled, temp._file)
    print('rolling over')
    temp.rollover()
    print(temp._rolled, temp._file)
    
# output
temp: <tempfile.SpooledTemporaryFile object at 0x1007b2c88>
False <_io.StringIO object at 0x1007a3d38>
False <_io.StringIO object at 0x1007a3d38>
False <_io.StringIO object at 0x1007a3d38>
rolling over
True <_io.TextIOWrapper name=4 mode='w+t' encoding='utf-8'>
```

### 4.4 临时目录

当需要多个临时文件时，也许使用创建临时目录来打开所有的文件的方式更方便。`TemporaryDirectory` 方法能够创建临时目录。

```python
import pathlib
import tempfile

# 上下文管理器生成了目录的名称，然后可以在上下文中使用该名称创建其它文件
with tempfile.TemporaryDirectory() as directory_name:
    the_dir = pathlib.Path(directory_name)
    print(the_dir)
    a_file = the_dir / 'a_file.txt'
    a_file.write_text('This file is deleted.')

print('Directory exists after?', the_dir.exists())
print('Contents after:', list(the_dir.glob('*')))

# output
/var/folders/5q/8gk0wq888xlggz008k8dr7180000hg/T/tmp_urhiioj
Directory exists after? False
Contents after: []
```

### 4.5 预测名称——`Predicting Names`

虽然生成的临时文件名称中包含可预测部分比起严格匿名文件安全性较低，但可以找到该文件并对其进行检查以用于调试。到目前讲述的所有方法都采用三个参数在一定程度上控制文件名，名称生成规则如下：`dir + prefix + random + suffix`。四个参数中除了 `random` 都可以传递给相应方法用于创建临时文件和目录

```
import tempfile
# prefix 和 suffix 以及随机字符串组合起来用于构建文件名称，dir 参数用于新文件创建的位置
with tempfile.NamedTemporaryFile(suffix='_suffix',
                                 prefix='prefix_',
                                 dir='/tmp') as temp:
    print('temp:')
    print('  ', temp)
    print('temp.name:')
    print('  ', temp.name)
    
# output
temp:
   <tempfile._TemporaryFileWrapper object at 0x1018b2d68>
temp.name:
   /tmp/prefix_q6wd5czl_suffix
```

## 5. `shutil` ——高级文件操作

作用是复制、设置权限等的文件高级操作

```python
"Error", "ExecError", "ReadError", "RegistryError", "SameFileError", "SpecialFileError", "_ARCHIVE_FORMATS", "_BZ2_SUPPORTED", "_LZMA_SUPPORTED", "_UNPACK_FORMATS", "_ZLIB_SUPPORTED", "__all__", "__builtins__", "__cached__", "__doc__", "__file__", "__loader__", "__name__", "__package__", "__spec__", "_basename", "_check_unpack_options", "_copyxattr", "_destinsrc", "_ensure_directory", "_find_unpack_format", "_get_gid", "_get_uid", "_make_tarball", "_make_zipfile", "_ntuple_diskusage", "_rmtree_safe_fd", "_rmtree_unsafe", "_samefile", "_unpack_tarfile", "_unpack_zipfile", "_use_fd_functions", "chown", "collections", "copy", "copy2", "copyfile", "copyfileobj", "copymode", "copystat", "copytree", "disk_usage", "errno", "fnmatch", "get_archive_formats", "get_terminal_size", "get_unpack_formats", "getgrnam", "getpwnam", "ignore_patterns", "make_archive", "move", "os", "register_archive_format", "register_unpack_format", "rmtree", "stat", "sys", "unpack_archive", "unregister_archive_format", "unregister_unpack_format", "which"
```

### 5.1 复制文件

`copyfile` 方法是通过将源内容复制到目标文件，这里需要对目标文件有写入权限否则要报 `IOError`，另外对于某些特殊源文件（如 `Unix` 设备节点）是不能使用 `copyfile` 方法复制为新的特殊文件。其实现方式是使用了底层函数 `copyfileobj` ——它的第三个可选参数可以调整读入块的一个缓冲区长度。

```python
import glob
import shutil

print('BEFORE:', glob.glob('shutil_copyfile.*'))

shutil.copyfile('shutil_copyfile.py', 'shutil_copyfile.py.copy')

print('AFTER:', glob.glob('shutil_copyfile.*'))

# output
BEFORE: ['shutil_copyfile.py']
AFTER: ['shutil_copyfile.py', 'shutil_copyfile.py.copy']
```

下面的示例是使用底层函数 `copyfileobj`，并且使用了不同的块大小参数来显示结果

```python
import io
import os
import shutil
import sys


class VerboseStringIO(io.StringIO):

    def read(self, n=-1):
        next = io.StringIO.read(self, n)
        print('read({}) got {} bytes'.format(n, len(next)))
        return next


lorem_ipsum = '''Lorem ipsum dolor sit amet, consectetuer
adipiscing elit.  Vestibulum aliquam mollis dolor. Donec
vulputate nunc ut diam. Ut rutrum mi vel sem. Vestibulum
ante ipsum.'''

print('Default:')
input = VerboseStringIO(lorem_ipsum)
output = io.StringIO()
shutil.copyfileobj(input, output)

print()

print('All at once:')
input = VerboseStringIO(lorem_ipsum)
output = io.StringIO()
shutil.copyfileobj(input, output, -1)

print()

print('Blocks of 256:')
input = VerboseStringIO(lorem_ipsum)
output = io.StringIO()
shutil.copyfileobj(input, output, 256)

# output
Default:
read(16384) got 166 bytes
read(16384) got 0 bytes

All at once:
read(-1) got 166 bytes
read(-1) got 0 bytes

Blocks of 256:
read(256) got 166 bytes
read(256) got 0 bytes
```

另外还有一种复制方式，使用 `copy` 方法的方式和 `Unix` 使用 `cp` 方式相同，而且文件权限可能发生变更。另外 `copy2` 方法会修改元数据例如访问和修改时间

```python
import glob
import os
import shutil

os.mkdir('example')
print('BEFORE:', glob.glob('example/*'))

shutil.copy('shutil_copy.py', 'example')

print('AFTER :', glob.glob('example/*'))

# output
BEFORE: []
AFTER : ['example/shutil_copy.py']

def show_file_info(filename):
    stat_info = os.stat(filename)
    print('  Mode    :', oct(stat_info.st_mode))
    print('  Created :', time.ctime(stat_info.st_ctime))
    print('  Accessed:', time.ctime(stat_info.st_atime))
    print('  Modified:', time.ctime(stat_info.st_mtime))


os.mkdir('example')
print('SOURCE:')
show_file_info('shutil_copy2.py')

shutil.copy2('shutil_copy2.py', 'example')

print('DEST:')
show_file_info('example/shutil_copy2.py')

# output
SOURCE:
  Mode    : 0o100644
  Created : Wed Dec 28 19:03:12 2016
  Accessed: Wed Dec 28 19:03:49 2016
  Modified: Wed Dec 28 19:03:12 2016
DEST:
  Mode    : 0o100644
  Created : Wed Dec 28 19:03:49 2016
  Accessed: Wed Dec 28 19:03:49 2016
  Modified: Wed Dec 28 19:03:12 2016
```

复制文件元数据——默认情况下，Unix 上创建一个新文件的时候，它的权限依赖于当前用户的 umask。为了复制文件权限，使用 `copymode` 方法。另外还有一个 `copystat` 可以复制文件其他权限。

```python
import os
import shutil
import subprocess

with open('file_to_change.txt', 'wt') as f:
    f.write('content')
os.chmod('file_to_change.txt', 0o444)

print('BEFORE:', oct(os.stat('file_to_change.txt').st_mode))

shutil.copymode('shutil_copymode.py', 'file_to_change.txt')

print('AFTER :', oct(os.stat('file_to_change.txt').st_mode))

# output
BEFORE: 0o100444
AFTER : 0o100644
    
# 下面是使用 copystat 复制权限
import os
import shutil
import time


def show_file_info(filename):
    stat_info = os.stat(filename)
    print('  Mode    :', oct(stat_info.st_mode))
    print('  Created :', time.ctime(stat_info.st_ctime))
    print('  Accessed:', time.ctime(stat_info.st_atime))
    print('  Modified:', time.ctime(stat_info.st_mtime))


with open('file_to_change.txt', 'wt') as f:
    f.write('content')
os.chmod('file_to_change.txt', 0o444)

print('BEFORE:')
show_file_info('file_to_change.txt')

shutil.copystat('shutil_copystat.py', 'file_to_change.txt')

print('AFTER:')
show_file_info('file_to_change.txt')

# output
BEFORE:
  Mode    : 0o100444
  Created : Wed Dec 28 19:03:49 2016
  Accessed: Wed Dec 28 19:03:49 2016
  Modified: Wed Dec 28 19:03:49 2016
AFTER:
  Mode    : 0o100644
  Created : Wed Dec 28 19:03:49 2016
  Accessed: Wed Dec 28 19:03:49 2016
  Modified: Wed Dec 28 19:03:46 2016
```

### 5.2 处理目录树

`shutil` 模块提供了三个方法处理目录树。为了复制目录到另一个目标，可以使用 `copytree` 方法 。它递归源目录内容，将每个文件复制到目标目录，要求目标目录必须先存在。`symlinks` 参数控制符号链接是被赋值为链接还是文件。默认情况下时将内容复制到新的文件。如果这个参数是 `true` ，将会在目标目录树中创建新的符号链接。

```python
import glob
import pprint
import shutil

print('BEFORE:')
pprint.pprint(glob.glob('/tmp/example/*'))

shutil.copytree('../shutil', '/tmp/example')

print('\nAFTER:')
pprint.pprint(glob.glob('/tmp/example/*'))
```

`copytree()` 方法接受两个可调用参数控制它的行为。`ignore` 参数在每个目录或者子目录以及目录中内容被复制时调用，它返回一个应该被复制的内容列表。`copy_function` 参数用于在文件实际复制时调用。例子中，`ignore_patterns()` 用于去创建一个忽略方法跳过 Python 源文件。`verbose_copy()` 复制的文件名称然后调用 `copy2()` 复制，它是默认的复制方法

```python
import glob
import pprint
import shutil


def verbose_copy(src, dst):
    print('copying\n {!r}\n to {!r}'.format(src, dst))
    return shutil.copy2(src, dst)


print('BEFORE:')
pprint.pprint(glob.glob('/tmp/example/*'))
print()

shutil.copytree(
    '../shutil', '/tmp/example',
    copy_function=verbose_copy,
    ignore=shutil.ignore_patterns('*.py'),
)

print('\nAFTER:')
pprint.pprint(glob.glob('/tmp/example/*'))
```

目录删除需要使用 `rmtree` 方法，错误默认情况下引发为异常，但是如果第二个参数为 `true` 将被忽略，也可以通过第三个参数提供一个错误处理方法。另外可以使用 `move` 方法将一个文件或者目录从一个地方移到另一个地方，类似于 `mv` 明令。

```python
import glob
import pprint
import shutil

print('BEFORE:')
pprint.pprint(glob.glob('/tmp/example/*'))

shutil.rmtree('/tmp/example')

print('\nAFTER:')
pprint.pprint(glob.glob('/tmp/example/*'))

# 下面是使用 move 方法

import glob
import shutil

with open('example.txt', 'wt') as f:
    f.write('contents')

print('BEFORE: ', glob.glob('example*'))

shutil.move('example.txt', 'example.out')

print('AFTER : ', glob.glob('example*'))
```



## 参考

1. [Managing File System Permissions](https://pymotw.com/3/os/index.html#os-stat)  Discussion of `os.stat()` and `os.lstat()`.

2. [glob](https://pymotw.com/3/glob/index.html#module-glob) Unix shell pattern matching for filenames

3. [PEP 428](https://www.python.org/dev/peps/pep-0428) The pathlib module

4. [Pattern Matching Notation](http://www.opengroup.org/onlinepubs/000095399/utilities/xcu_chap02.html#tag_02_13) An explanation of globbing from The Open Group’s Shell Command Language specification.

5. [Standard library documentation for linecache](https://docs.python.org/3.6/library/linecache.html) 

   `linecache` 模块可以从文件或者导入的 `Python` 模块中检索文本行，并保存结果的缓存，使得同一文本的多行读取效率更高。处理 `Python` 源文件时，`linecache` 模块通常用于 `Python` 标准库的其它部分。缓存实现了在内存中保存文件内容（解析为单独的行）。`API` 通过索查询引列表返回请求的行，相比反复读取文件并解析行然后找到所需的内容，这样节省了很多时间。这个方法在查找同一个文件中的多行时尤其有用，，例如为错误报告生成跟踪记录（**traceback**）。

   

   常用的方法是 `getline` ，可以读取特定的行，并且是原生字符串（即空行返回 “\n”），而且使用此方法是对超过文件行值的行数会返回空字符串

    