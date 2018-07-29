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

## 6. `mmap`——内存映射文件

建立内存映射文件而不是直接读取内容，建立一个文件的内存映射将使用操作系统虚拟内粗系统直接访问文件系统中的数据，而不使用 `I/O` 方式。这样可以提高性能，因为使用内存映射时，不会对每个访问产生单独系统调用，且不会在缓冲区之间复制数据，这样内核和用户都会直接访问内存。

内存映射文件可以看作是可以修改的字符串或类文件对象，具体情况更具具体需要。内存映射文件支持一般的文件 `API` 方法，例如 `close`, `flush`, `read`, `readline`, `seek`, `tell` 以及 `write`，同时支持字符串的方法。

### 6.1 文件读取

使用 `mmap` 函数可以创建一个内存映射文件，第一个参数是文件描述符，或者来自 `file` 对象的 `fileno` 方法，也可以来自 `os.open()` 方式。第二个参数传入 `mmap()` 的参数是要确定是多大的字节大小去映射的文件内容。如果值是 `0` ，那么代表映射整个文件。如果这个只存超过当前文件，文件将会被扩展。还有一个可选的参数 `access` 在两个平台都是支持的，使用 `ACCESS_READ` 表示只读，`ACCESS_WRITE` 表示直接写（对内存的操作直接写入文件），或者 `ACCESS_COPY` 用于写时复制（内存分配不写入文件）。

```python
import mmap

# 文件指针会追踪切片操作上次读取的位置。这个例子中，第一次读取之后指针向前移动了 10 字节。在切片操作开始之前，文件指针重置到文件开始处，然后又向前移动了 10 字节。切片操作之后，调用 read(10) 将会得到文件 11-20 字节的内容
with open('lorem.txt', 'r') as f:
    with mmap.mmap(f.fileno(), 0,
                   access=mmap.ACCESS_READ) as m:
        print('First 10 bytes via read :', m.read(10))
        print('First 10 bytes via slice:', m[:10])
        print('2nd   10 bytes via read :', m.read(10))
```

### 6.2 文件写入

为了设置一个内存映射文件去接受更新，要以模式 `r+` （而不是 `w`）打开然后再进行映射，才能进行添加。然后可以使用任何更新数据的 `API`（`write()`，赋值到切片等方式）。

下一个例子使用了默认的访问模式 `ACCESS_WRITE`，然后通过将值赋给切片的方式修改文件的部分行。

```python
import mmap
import shutil

# Copy the example file
shutil.copyfile('lorem.txt', 'lorem_copy.txt')

word = b'consectetuer'
reversed = word[::-1]
print('Looking for    :', word)
print('Replacing with :', reversed)

# 内存和文件中第一行中间部分的 consectetuer 将被替换为逆序
with open('lorem_copy.txt', 'r+') as f:
    with mmap.mmap(f.fileno(), 0) as m:
        print('Before:\n{}'.format(m.readline().rstrip()))
        m.seek(0)  # rewind

        loc = m.find(word)
        m[loc:loc + len(word)] = reversed
        m.flush()

        m.seek(0)  # rewind
        print('After :\n{}'.format(m.readline().rstrip()))

        f.seek(0)  # rewind
        print('File  :\n{}'.format(f.readline().rstrip()))
```

此外内存映射文件，可以使用正则表达式进行处理字符串。

[TOC]

## 7. `codecs`——字符串编码和解码

作用在不同的文本装欢中作为编码器和解码器，`codecs` 模块提供了流接口和文件接口来转换数据，通常用于处理 `Unicode` 文本，当然可以处理其他编码来作其他用途。

```python
"OM", "BOM32_BE", "BOM32_LE", "BOM64_BE", "BOM64_LE", "BOM_BE", "BOM_LE", "BOM_UTF16", "BOM_UTF16_BE", "BOM_UTF16_LE", "BOM_UTF32", "BOM_UTF32_BE", "BOM_UTF32_LE", "BOM_UTF8", "BufferedIncrementalDecoder", "BufferedIncrementalEncoder", "Codec", "CodecInfo", "EncodedFile", "IncrementalDecoder", "IncrementalEncoder", "StreamReader", "StreamReaderWriter", "StreamRecoder", "StreamWriter", "__all__", "__builtins__", "__cached__", "__doc__", "__file__", "__loader__", "__name__", "__package__", "__spec__", "_false", "ascii_decode", "ascii_encode", "backslashreplace_errors", "builtins", "charmap_build", "charmap_decode", "charmap_encode", "decode", "encode", "escape_decode", "escape_encode", "getdecoder", "getencoder", "getincrementaldecoder", "getincrementalencoder", "getreader", "getwriter", "ignore_errors", "iterdecode", "iterencode", "latin_1_decode", "latin_1_encode", "lookup", "lookup_error", "make_encoding_map", "make_identity_dict", "namereplace_errors", "open", "raw_unicode_escape_decode", "raw_unicode_escape_encode", "readbuffer_encode", "register", "register_error", "replace_errors", "strict_errors", "sys", "unicode_escape_decode", "unicode_escape_encode", "unicode_internal_decode", "unicode_internal_encode", "utf_16_be_decode", "utf_16_be_encode", "utf_16_decode", "utf_16_encode", "utf_16_ex_decode", "utf_16_le_decode", "utf_16_le_encode", "utf_32_be_decode", "utf_32_be_encode", "utf_32_decode", "utf_32_encode", "utf_32_ex_decode", "utf_32_le_decode", "utf_32_le_encode", "utf_7_decode", "utf_7_encode", "utf_8_decode", "utf_8_encode", "xmlcharrefreplace_errors"
```

### 7.1 `Unicode` 入门

`CPython 3.x` 版本中文本和字节存在差别。`bytes` 实例使用一系列8位字节值。相反，`str` 字符串内部被作为一系列 `Unicode` 码点（**Code Points**）管理。每个码点被存储为 2-4 字节的序列，这个取决于 `Python` 编译时给出的选项。

当输出 `str` 值时，它使用几种标准方案之一进行编码，以便稍后字节序列可以被重建为相同的文本字符串。编码值的字节不一定与码点相同，并且编码定义了两组值之间转换的方式。读取 Unicode 数据还需要知道编码，以便传入的字节可以转换为 Unicode 类使用的内部表示。

西方语言最常见的编码是 `UTF-8` 和 `UTF-16` ，它们分别使用一个或者两个字节序列表示每个代码点。对于大多数字符用于两个字节的码点存储可能不太适合，所以其他的编码可能更高效。

#### 7.1.1 编码——`Encodings`

理解编码的最好方式是去查看用不同方式对相同字符串编码产生的不同字节序列。下面的例子用这个函数格式化字节字符串以更好地阅读。

```python
import binascii

# 这个函数使用 binascii 得到字符串的16进制表示，然后在返回之前每隔 nbytes 插入一个空格
def to_hex(t, nbytes):
    """Format text t as a sequence of nbyte long values
    separated by spaces.
    """
    chars_per_item = nbytes * 2
    hex_version = binascii.hexlify(t)
    return b' '.join(
        hex_version[start:start + chars_per_item]
        for start in range(0, len(hex_version), chars_per_item)
    )
    
print(to_hex(b'abcdef', 1))
print(to_hex(b'abcdef', 2))

# output
b'61 62 63 64 65 66'
b'6162 6364 6566'
```

 下面的示例中第一个编码示例首先使用 `unicode` 类的原始表示法打印文 `français`，然后从 Unicode 数据库中输出每个字符的名称。接下来两行分别将字符串编码为 `UTF-8` 和 `UTF-16`，并将编码结果显示为16进制。

```python
import unicodedata
from codecs_to_hex import to_hex		# 这里的 codecs_to_hex 是上面的代码脚本名称

text = 'français'

print('Raw   : {!r}'.format(text))
for c in text:
    print('  {!r}: {}'.format(c, unicodedata.name(c, c)))
print('UTF-8 : {!r}'.format(to_hex(text.encode('utf-8'), 1)))
print('UTF-16: {!r}'.format(to_hex(text.encode('utf-16'), 2)))

# output
Raw   : 'français'
  'f': LATIN SMALL LETTER F
  'r': LATIN SMALL LETTER R
  'a': LATIN SMALL LETTER A
  'n': LATIN SMALL LETTER N
  'ç': LATIN SMALL LETTER C WITH CEDILLA
  'a': LATIN SMALL LETTER A
  'i': LATIN SMALL LETTER I
  's': LATIN SMALL LETTER S
UTF-8 : b'66 72 61 6e c3 a7 61 69 73'
UTF-16: b'fffe 6600 7200 6100 6e00 e700 6100 6900 7300'
```

给一个编码字节序列作为 `bytes` 实例，`decode()` 方法将会把它们翻译为 Unicode 码点并返回一个 `str` 实例。编码方式不会改变输出类型。需要注意默认的编码方式是在程序启动时设置, 当 `site` 加载时。有关默认编码的讨论请参考 `sys` 关于 `Unicode Defaults` 的部分

```python
from codecs_to_hex import to_hex

text = 'français'
encoded = text.encode('utf-8')
decoded = encoded.decode('utf-8')

print('Original :', repr(text))
print('Encoded  :', to_hex(encoded, 1), type(encoded))
print('Decoded  :', repr(decoded), type(decoded))

# output
Original : 'français'
Encoded  : b'66 72 61 6e c3 a7 61 69 73' <class 'bytes'>
Decoded  : 'français' <class 'str'>
```

### 7.2 处理文件

当处理 `I/O ` 操作的时候，字符串编码和解码特别重要的。不论是写入到文件， `socket` 或者其它流，数据必须被恰当的编码。所有的文本数据当它被读的时候需要从字节形式解码，写入的时候必须从内部值转换为特定的表示。程序可以显性地编码和解码数据，但依赖所使用的编码，确定是否读取了足够的字节以完全解码数据是非常重要的。 `codecs` 模块提供了数据编码和解码的类，因此程序中一般不需要再处理这类工作。

 `codecs` 提供的简单接口可以用来替代内置的 `open()` 方法。新版本工作方式类似内置方法，但是添加了两个参数来指定编码以及错误处理技术。

```python
from codecs_to_hex import to_hex

import codecs
import sys

encoding = sys.argv[1]
filename = encoding + '.txt'

print('Writing to', filename)
with codecs.open(filename, mode='w', encoding=encoding) as f:
    f.write('français')

# Determine the byte grouping to use for to_hex()
nbytes = {
    'utf-8': 1,
    'utf-16': 2,
    'utf-32': 4,
}.get(encoding, 1)

# Show the raw bytes in the file
print('File contents:')
with open(filename, mode='rb') as f:
    print(to_hex(f.read(), nbytes)
   
# 这个例子以带有 ç 的 unicode 字符串开头，并使用在命令行上指定的编码将文本保存到文件   
# output
$ python3 codecs_open_write.py utf-8
Writing to utf-8.txt
File contents:
b'66 72 61 6e c3 a7 61 69 73'

$ python3 codecs_open_write.py utf-16

Writing to utf-16.txt
File contents:
b'fffe 6600 7200 6100 6e00 e700 6100 6900 7300'

$ python3 codecs_open_write.py utf-32

Writing to utf-32.txt
File contents:
b'fffe0000 66000000 72000000 61000000 6e000000 e7000000 61000000
69000000 73000000'
```

使用 `open` 直接读取数据，首先就需要明确编码方式，这样才能得到正确的解码序列。某些数据格式指明编码方式，例如：XML，但这通常由应用程序管理来决定的（不同的程序要求不一样）。`codecs` 简单地将编码作为参数，并假设它是正确的。

```python
import codecs
import sys

encoding = sys.argv[1]
filename = encoding + '.txt'

print('Reading from', filename)
with codecs.open(filename, mode='r', encoding=encoding) as f:
    print(repr(f.read()))
    
# output
$ python3 codecs_open_read.py utf-8

Reading from utf-8.txt
'français'

$ python3 codecs_open_read.py utf-16

Reading from utf-16.txt
'français'

$ python3 codecs_open_read.py utf-32

Reading from utf-32.txt
'français'
```

### 7.3 字节序——`Byte Order`

在不同计算机系统之间传输数据的时候（可能通过直接复制或者网络通信复制文件），多字节编码（如 `UTF-16` 和 `UTF-32`）可能会产生问题。不同系统使用不同的高低字节排序。数据的这种特性（称为其字节序），依赖于硬件体系结构，操作系统和应用开发人员的选择等因素。通常没有办法确定给定的一组数据要使用哪种子节序，因此多字节编码还包括字节顺序标记（`BOM`——`Byte Order Marker`），这个标记出现在编码输出的前几个字节。例如，按照 `UTF-16` 定义， `0xFFFE` 和 `0xFEFF` 不是有效字符，但是它们是被用于标识字节顺序。`codecs` 定义了表示 `UTF-16` 和 `UTF-32` 字节顺序的常量。取决于当前系统的固有子节序，`BOM`, `BOM_UTF16` 和 `BOM_UTF-32` 会自动的设置为适当的大端（`Big-endian`）和小段（`Little-endian`）值。

```python
import codecs
from codecs_to_hex import to_hex

BOM_TYPES = [
    'BOM', 'BOM_BE', 'BOM_LE',
    'BOM_UTF8',
    'BOM_UTF16', 'BOM_UTF16_BE', 'BOM_UTF16_LE',
    'BOM_UTF32', 'BOM_UTF32_BE', 'BOM_UTF32_LE',
]

for name in BOM_TYPES:
    print('{:12} : {}'.format(
        name, to_hex(getattr(codecs, name), 2)))
        
# output
BOM          : b'fffe'
BOM_BE       : b'feff'
BOM_LE       : b'fffe'
BOM_UTF8     : b'efbb bf'
BOM_UTF16    : b'fffe'
BOM_UTF16_BE : b'feff'
BOM_UTF16_LE : b'fffe'
BOM_UTF32    : b'fffe 0000'
BOM_UTF32_BE : b'0000 feff'
BOM_UTF32_LE : b'fffe 0000'
```

`codecs` 中的解码器会自动检查和处理子节序，不过编码时也可以显式的指定子节序。下面的例子中，首先得出内置子节序，然后显式的使用候选形式，以便下一个例子可展示读取时自动检测到的子节序。

```python
import codecs
from codecs_to_hex import to_hex

# Pick the nonnative version of UTF-16 encoding
if codecs.BOM_UTF16 == codecs.BOM_UTF16_BE:
    bom = codecs.BOM_UTF16_LE
    encoding = 'utf_16_le'
else:
    bom = codecs.BOM_UTF16_BE
    encoding = 'utf_16_be'

print('Native order  :', to_hex(codecs.BOM_UTF16, 2))
print('Selected order:', to_hex(bom, 2))

# Encode the text.
encoded_text = 'français'.encode(encoding)
print('{:14}: {}'.format(encoding, to_hex(encoded_text, 2)))

with open('nonnative-encoded.txt', mode='wb') as f:
    # Write the selected byte-order marker.  It is not included
    # in the encoded text because the byte order was given
    # explicitly when selecting the encoding.
    f.write(bom)
    # Write the byte string for the encoded text.
    f.write(encoded_text)
    
# output
Native order  : b'fffe'
Selected order: b'feff'
utf_16_be     : b'0066 0072 0061 006e 00e7 0061 0069 0073'
```

下面的例子中，在运行文件时没有指定子节序，所以解码器会使用文件前两个子节中的 BOM 值来去定子节序。

```python
import codecs
from codecs_to_hex import to_hex

# Look at the raw data
with open('nonnative-encoded.txt', mode='rb') as f:
    raw_bytes = f.read()

print('Raw    :', to_hex(raw_bytes, 2))

# Re-open the file and let codecs detect the BOM
with codecs.open('nonnative-encoded.txt',
                 mode='r',
                 encoding='utf-16',
                 ) as f:
    decoded_text = f.read()

print('Decoded:', repr(decoded_text))

# 因为前两个子节用于子节序检测，所以它们并不包含在 read 返回的数据中
# output
Raw    : b'feff 0066 0072 0061 006e 00e7 0061 0069 0073'
Decoded: 'français'
```

### 7.4 错误处理

在读写文件时需要知道其所使用的编码，正确地设置编码很重要：1）如果读取文件时未能正确地配置编码，就无法正确地解释数据，严重的时候数据可能被破坏甚至无法解码；2）在 `Unicode` 字符中，并不是都可以使用所有编码表示（某些 `Unicode` 字符无法使用其他字符集表示）。所以写文件时使用了错误的编码，就会发生错误，数据也会丢失。

而在实际工作中， `unicode`， `str` 以及 `codecs` 的编码和解码使用了五种错误处理选项，如下：



| 错误模式            | 处理描述                               |
| ------------------- | -------------------------------------- |
| `stric`             | 如果数据无法转换，产生异常             |
| `replace`           | 将无法编码的数据替换为一个特殊的标识符 |
| `ignore`            | 跳过数据                               |
| `xmlcharrefreplace` | `XML` 字符（仅适用于编码）             |
| `backslashreplace`  | 转移序列（仅适用于编码）               |

#### 7.4.1 编码错误

最常见的错误条件是从一个 `ASCII` 输出流写 `Unicode` 数据时收到 `UnicodeEncodeError`。下例中试验了不同的错误处理模式

```python
import codecs
import sys

error_handling = sys.argv[1]

text = 'français'

try:
    # Save the data, encoded as ASCII, using the error
    # handling mode specified on the command line.
    with codecs.open('encode_error.txt', 'w',
                     encoding='ascii',
                     errors=error_handling) as f:
        f.write(text)

except UnicodeEncodeError as err:
    print('ERROR:', err)

else:
    # If there was no error writing to the file,
    # show what it contains.
    with open('encode_error.txt', 'rb') as f:
        print('File contents: {!r}'.format(f.read()))
# 要确保一个程序显式地为所有 I/O 操作正确，strict 是最安全的。但也如下的结果一样，它会因为异常而导致程序崩溃       
# output
$ python3 codecs_encode_error.py strict
ERROR: 'ascii' codec can't encode character '\xe7' in position
4: ordinal not in range(128)
    
# 另外一些模式更为灵活，但代价可能是丢失一些无法转换为所需编码的数据，例如 replace。pi 的 unicode 字符仍然无法用 ASCII 编码，但是这种错误处理不会报错，使用了 ? 替换字符
$ python3 codecs_encode_error.py replace

File contents: b'fran?ais'
    
# 使用 ignore 将直接丢弃无法编码的数据
$ python3 codecs_encode_error.py ignore

File contents: b'franais'
    
# 还有两种无损的错误处理方式，这两种模式会用一个不同于编码的标准中定义的候选表示符来替换字符。xmlcharrefreplace 使用了 XML 的字符——引用了 W3C 的定义字符列表
$ python3 codecs_encode_error.py xmlcharrefreplace

File contents: b'fran&#231;ais'

# 最后一种 backslashreplace 生成的输出格式类似于打印 Unicode 对象的 repr() 时返回的值。Unicode 字符会替换为 \u, 后面跟有码点的十六进制值
$ python3 codecs_encode_error.py backslashreplace

File contents: b'fran\\xe7ais'
```

#### 7.4.2 解码错误

数据解码时也有可能遇到错误，特别是在使用了错误的编码时。下面分别演示了不同的方式来解码

```python
# codecs_decode_error.py
import codecs
import sys

from codecs_to_hex import to_hex

error_handling = sys.argv[1]

text = 'français'
print('Original     :', repr(text))

# Save the data with one encoding
with codecs.open('decode_error.txt', 'w',
                 encoding='utf-16') as f:
    f.write(text)

# Dump the bytes from the file
with open('decode_error.txt', 'rb') as f:
    print('File contents:', to_hex(f.read(), 1))

# Try to read the data with the wrong encoding
with codecs.open('decode_error.txt', 'r',
                 encoding='utf-8',
                 errors=error_handling) as f:
    try:
        data = f.read()
    except UnicodeDecodeError as err:
        print('ERROR:', err)
    else:
        print('Read         :', repr(data))
        
# strict 模式下，产生一个 UnicodeDecodeError——因为 UTF-16BOM 的部分转换为一个使用 UTF-8 的解码器 
$ python3 codecs_decode_error.py strict

Original     : 'français'
File contents: b'ff fe 66 00 72 00 61 00 6e 00 e7 00 61 00 69 00
73 00'
ERROR: 'utf-8' codec can't decode byte 0xff in position 0:
invalid start byte

# 使用 ignore 导致解码器跳过不合法的子节，结果仍然不是原来的期望，因为其中嵌入了 null 子节
$ python3 codecs_decode_error.py ignore

Original     : 'français'
File contents: b'ff fe 66 00 72 00 61 00 6e 00 e7 00 61 00 69 00
73 00'
Read         : 'f\x00r\x00a\x00n\x00\x00a\x00i\x00s\x00'

# 使用 replace，非法的子节会替换为 \uFFFD，这个是 Unicode 官方替换字符，即菱形背景中有一个问号
$ python3 codecs_decode_error.py replace

Original     : 'français'
File contents: b'ff fe 66 00 72 00 61 00 6e 00 e7 00 61 00 69 00
73 00'
Read         : '��f\x00r\x00a\x00n\x00�\x00a\x00i\x00s\x00'
```

### 7.5 编码翻译——`Encoding Translation`

虽然大多数程序可以在内部使用 `str` 数据，但是编码和解码是被作为`I/O` 操作的一部分，有时候更改文件的编码但不需要保留中间数据格式是非常有用的。`EncodedFile` 方法将使用了打开的文件句柄其使用了编码或者被包装为一个类，这个类在 `I/O`发生时可以将数据转换为另外一种编码。下面例子显示了从 `EncodedFile` 返回并写入单独句柄的过程。无论是用于读还是写，`file_encoding` 始终引用打开的文件句柄的编码，`data_encoding` 当 `read` 或者 `write` 调用的时候使用。表现的作用就是使用 `EncodedFile` 方法，利用 `I/O` 方式来读取数据

```python
from codecs_to_hex import to_hex

import codecs
import io

# Raw version of the original data.
data = 'français'

# Manually encode it as UTF-8.
utf8 = data.encode('utf-8')
print('Start as UTF-8   :', to_hex(utf8, 1))

# Set up an output buffer, then wrap it as an EncodedFile.
output = io.BytesIO()
encoded_file = codecs.EncodedFile(output, data_encoding='utf-8',
                                  file_encoding='utf-16')
encoded_file.write(utf8)

# Fetch the buffer contents as a UTF-16 encoded byte string
utf16 = output.getvalue()
print('Encoded to UTF-16:', to_hex(utf16, 2))

# Set up another buffer with the UTF-16 data for reading,
# and wrap it with another EncodedFile.
buffer = io.BytesIO(utf16)
encoded_file = codecs.EncodedFile(buffer, data_encoding='utf-8',
                                  file_encoding='utf-16')

# Read the UTF-8 encoded version of the data.
recoded = encoded_file.read()
print('Back to UTF-8    :', to_hex(recoded, 1))


# output
Start as UTF-8   : b'66 72 61 6e c3 a7 61 69 73'
Encoded to UTF-16: b'fffe 6600 7200 6100 6e00 e700 6100 6900
7300'
Back to UTF-8    : b'66 72 61 6e c3 a7 61 69 73'
```

### 7.6 非 `Unicode` 编码

尽管先前的例子都是用于 `Unicode` 编码，但是 `codecs` 模块可以用于许多其他的数据翻译。例如 `Python` 中的 `codecs` 可以用于处理 `base-64`，`bzip2`，`ROT-13`，`ZIP` 等其它数据格式。任何可以表示为可以接受单个参数且能返回子节或者 `Unicode` 字符串的函数即可作为转换，这种类型的转换可以被登记为解码器（**Codec**）。例如下面的 `rot_13` 解码器，接受了一个 `Unicode` 字符串作为输入，其结果返回的结果也是一个 `Unicode`。

```python
# 下面的例子使用了 rot-13 的数据格式
import codecs
import io

buffer = io.StringIO()
stream = codecs.getwriter('rot_13')(buffer)	
# stream 类型是 encodings.rot_13.StreamWriter

text = 'abcdefghijklmnopqrstuvwxyz'

stream.write(text)
stream.flush()

print('Original:', text)
print('ROT-13  :', buffer.getvalue())

# output
Original: abcdefghijklmnopqrstuvwxyz
ROT-13  : nopqrstuvwxyzabcdefghijklm
```

下面的例子是使用 `codecs` 封装数据流相比直接使用 `zlib` 提供了更简单的接口。并非所有的压缩和编码系统都支持通过使用流接口 `readline()` 或者 `read()` 方式来读取部分数据，因为它们需要找到压缩段的末尾来扩展它。如果程序不能在内存中保存所有未压缩的数据，使用压缩库的增量访问功能而不是编解码器。

```python
import codecs
import io

from codecs_to_hex import to_hex

buffer = io.BytesIO()
stream = codecs.getwriter('zlib')(buffer)

text = b'abcdefghijklmnopqrstuvwxyz\n' * 50

stream.write(text)
stream.flush()

print('Original length :', len(text))
compressed_data = buffer.getvalue()
print('ZIP compressed  :', len(compressed_data))

buffer = io.BytesIO(compressed_data)
stream = codecs.getreader('zlib')(buffer)

first_line = stream.readline()
print('Read first line :', repr(first_line))

uncompressed_data = first_line + stream.read()
print('Uncompressed    :', len(uncompressed_data))
print('Same            :', text == uncompressed_data)

# output
Original length : 1350
ZIP compressed  : 48
Read first line : b'abcdefghijklmnopqrstuvwxyz\n'
Uncompressed    : 1350
Same            : True
```

### 7.7 增量编码——`Incremental Encoding`

有些编码可能会在数据流处理时大幅改变数据流的长度，特别是 `zlib` 或者 `bz2`。对于大数据集，这样的编码操作最好是渐进式的，一次只处理少量数据块。`IncrementalEncoder` 和 `IncrementalDecoder` 的 `API` 设计作用于此。每次传递数据给编码器或者解码器的时候，其内部状态会更新。当状态一致的时候（由 `codecs` 定义），数据将被返回并且状态重置。在为达到状态之前，调用 `encode()` 或者 `decode()` 将不会返回任何数据。当传入最后一批数据时，参数 `final` 应该设置为 `True`， `codecs` 将刷新并输出所有剩余的缓冲数据。

```python
import codecs
import sys

from codecs_to_hex import to_hex

text = b'abcdefghijklmnopqrstuvwxyz\n'
repetitions = 50

print('Text length :', len(text))
print('Repetitions :', repetitions)
print('Expected len:', len(text) * repetitions)

# Encode the text several times to build up a
# large amount of data
encoder = codecs.getincrementalencoder('bz2')()
encoded = []

print()
print('Encoding:', end=' ')
last = repetitions - 1
for i in range(repetitions):
    en_c = encoder.encode(text, final=(i == last))
    if en_c:
        print('\nEncoded : {} bytes'.format(len(en_c)))
        encoded.append(en_c)
    else:
        sys.stdout.write('.')

all_encoded = b''.join(encoded)
print()
print('Total encoded length:', len(all_encoded))
print()

# Decode the byte string one byte at a time
decoder = codecs.getincrementaldecoder('bz2')()
decoded = []

print('Decoding:', end=' ')
for i, b in enumerate(all_encoded):
    final = (i + 1) == len(text)
    c = decoder.decode(bytes([b]), final)
    if c:
        print('\nDecoded : {} characters'.format(len(c)))
        print('Decoding:', end=' ')
        decoded.append(c)
    else:
        sys.stdout.write('.')
print()

restored = b''.join(decoded)

print()
print('Total uncompressed length:', len(restored))

# output
Text length : 27
Repetitions : 50
Expected len: 1350

Encoding: .................................................
Encoded : 99 bytes

Total encoded length: 99

Decoding: ........................................................................................
Decoded : 1350 characters
Decoding: ..........

Total uncompressed length: 1350
```

### 7.5 `Unicode` 数据和网络通信

类似于标准输入和输出文件的描述符，网络套接字也是字节流，因此将 `Unicode` 数据写至一个套接字之前必须先编码为子节。下例子中，服务器会把接收到的数据传回给发送者

```python
import sys
import socketserver


class Echo(socketserver.BaseRequestHandler):

    def handle(self):
        # Get some bytes and echo them back to the client.
        data = self.request.recv(1024)
        self.request.send(data)
        return


if __name__ == '__main__':
    import codecs
    import socket
    import threading

    address = ('localhost', 0)  # let the kernel assign a port
    server = socketserver.TCPServer(address, Echo)
    ip, port = server.server_address  # what port was assigned?

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)  # don't hang on exit
    t.start()

    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # Send the data
    # WRONG: Not encoded first!
    text = 'français'
    len_sent = s.send(text)

    # Receive a response
    response = s.recv(len_sent)
    print(repr(response))

    # Clean up
    s.close()
    server.socket.close()
    
# 在每次调用 send() 之前显式编码数据，但是如果缺少一个 send() 调用将导致编码错误——实际就是缺少一个编码
# output
Traceback (most recent call last):
  File "codecs_socket_fail.py", line 43, in <module>
    len_sent = s.send(text)
TypeError: a bytes-like object is required, not 'str'
```

下面使用 `makefile()` 为套接字获取类文件句柄，然后使用基于流的读取器或者写入器对其进行封装，这意味着 `Unicode` 字符串将在进出套接字的过程中进行编码。且使用 `PassThrough` 去显示发送之前编码的数据，以及在客户端接收响应后对其进行解码。

```python
import sys
import socketserver


class Echo(socketserver.BaseRequestHandler):

    def handle(self):
        """Get some bytes and echo them back to the client.

        There is no need to decode them, since they are not used.

        """
        data = self.request.recv(1024)
        self.request.send(data)


class PassThrough:

    def __init__(self, other):
        self.other = other

    def write(self, data):
        print('Writing :', repr(data))
        return self.other.write(data)

    def read(self, size=-1):
        print('Reading :', end=' ')
        data = self.other.read(size)
        print(repr(data))
        return data

    def flush(self):
        return self.other.flush()

    def close(self):
        return self.other.close()


if __name__ == '__main__':
    import codecs
    import socket
    import threading

    address = ('localhost', 0)  # let the kernel assign a port
    server = socketserver.TCPServer(address, Echo)
    ip, port = server.server_address  # what port was assigned?

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)  # don't hang on exit
    t.start()

    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # Wrap the socket with a reader and writer.
    read_file = s.makefile('rb')
    incoming = codecs.getreader('utf-8')(PassThrough(read_file))
    write_file = s.makefile('wb')
    outgoing = codecs.getwriter('utf-8')(PassThrough(write_file))

    # Send the data
    text = 'français'
    print('Sending :', repr(text))
    outgoing.write(text)
    outgoing.flush()

    # Receive a response
    response = incoming.read()
    print('Received:', repr(response))

    # Clean up
    s.close()
    server.socket.close()
    
# output
Sending : 'français'
Writing : b'fran\xc3\xa7ais'
Reading : b'fran\xc3\xa7ais'
Reading : b''
Received: 'français'
```

### 7.6 定义定制编码——`Defining a Custom Encoding`

由于 `Python` 已经提供了大量的标准编解码，一般情况下应用不太可能需要自定义解码器和编码器。如果确实需要的时候，`codecs` 中有很多基类，能够轻易的定义定制变啊吗。

第一步是去了解编码的转换性质。下面例子将使用 “invertcaps” 编码，它将进行大小写转换。下面是一个编码函数的简单定义，它会对一个输入字符串完成这个转换

```python
import string

# 这里的编码器和解码器都是同一个函数，和前面的 ROT_13 很相似
def invertcaps(text):
    """Return new string with the case of all letters switched.
    """
    return ''.join(
        c.upper() if c in string.ascii_lowercase
        else c.lower() if c in string.ascii_uppercase
        else c
        for c in text
    )


print(invertcaps('ABCdef'))
print(invertcaps('abcDEF'))
    
# output
abcDEF
ABCdef
```

尽管容易理解，但它的实现效率不高，特别是对非常大的字符串。`codecs` 提供了一些辅助函数可以根据字符映射（**Character Map**）创建编码，如 `invertcaps` 编码。这个映射包括了编码映射（**Encoding Map**）永固嫁给你字符值转换为输出中的子节值；以及解码映射（**Decoding Map**）用于相反功能。需要首先创建解码映射，然后使用 `make_encoding_map` 方法将它转换为一个编码映射，该方法还有一个作用可以检测哪些情况下多个输入字符编码为相同的输出子节，并把编码值替换为 `None` 将编码标记为未定义

```python
import codecs
import string

# Map every character to itself
decoding_map = codecs.make_identity_dict(range(256))

# Make a list of pairs of ordinal values for the lower
# and uppercase letters
pairs = list(zip(
    [ord(c) for c in string.ascii_lowercase],
    [ord(c) for c in string.ascii_uppercase],
))

# Modify the mapping to convert upper to lower and
# lower to upper.
decoding_map.update({
    upper: lower
    for (lower, upper)
    in pairs
})
decoding_map.update({
    lower: upper
    for (lower, upper)
    in pairs
})

# Create a separate encoding map.
encoding_map = codecs.make_encoding_map(decoding_map)

print(codecs.charmap_encode('abcDEF', 'strict',
                            encoding_map))
print(codecs.charmap_decode(b'abcDEF', 'strict',
                            decoding_map))
print(encoding_map == decoding_map)
    
# output
(b'ABCdef', 6)
('ABCdef', 6)
True
```

字符映射编码器和解码器支持前面描述的所有标准错误处理方法，因此不需要额外的工作来遵循相关的 `API` 标准。因为 `π` 的 `Unicode` 码点没有在这个编码图中，严格模式错误处理将会引发一个异常。

```python
import codecs
from codecs_invertcaps_charmap import encoding_map	# codecs_invertvaps_charmap 是吧之前的代码放在该脚本中

text = 'pi: \u03c0'

for error in ['ignore', 'replace', 'strict']:
    try:
        encoded = codecs.charmap_encode(
            text, error, encoding_map)
    except UnicodeEncodeError as err:
        encoded = str(err)
    print('{:7}: {}'.format(error, encoded))
    
# output
ignore : (b'PI: ', 5)
replace: (b'PI: ?', 5)
strict : 'charmap' codec can't encode character '\u03c0' in
position 4: character maps to <undefined>
```

在定义了编码映射和解码映射之后，还需要设置一些额外的类，同时编码需要被被注册。`register` 方法向注册表添加搜索功能，以方便使用编解码器时可以找到它。搜索函数必须采用一个表示编码名称的字符串作为参数，并在找到编码时返回 `CodecInfo` 对象，否则返回 `None`。下面是注册多个搜索函数，并依次调用每个搜索函数，直到返回一个 `CodecInfo` 或者消耗完的列表。`codecs` 内部注册的搜索函数知道怎么去加载标准的编解码器，例如，编码中的 `UTF-8` ，这类名称永远不会传递到自定义搜索函数——实际上就是为了方便加载解码器和编码器。

```python
import codecs
import encodings

def search1(encoding):
    print('search1: Searching for:', encoding)
    return None

def search2(encoding):
    print('search2: Searching for:', encoding)
    return None


codecs.register(search1)
codecs.register(search2)

utf8 = codecs.lookup('utf-8')
print('UTF-8:', utf8)

try:
    unknown = codecs.lookup('no-such-encoding')
except LookupError as err:
    print('ERROR:', err)
    
# output
UTF-8: <codecs.CodecInfo object for encoding utf-8 at
0x1007773a8>
search1: Searching for: no-such-encoding
search2: Searching for: no-such-encoding
ERROR: unknown encoding: no-such-encoding
```

`CodecInfo` 实例是通过搜索函数返回的，这个实例会告诉 `codecs` 如何使用所有不同支持机制来进行编码和解码：无状态（**Stateless**），增量（**Incremental**）和流（**Stream**）。`codecs` 包含基类以帮助设置字符映射编码。下例将所有这些部分放在一起来注册一个所搜函数，该函数返回为 `invertcaps` 编解码器配置的 `CodecInfo` 实例。

```python
import codecs

from codecs_invertcaps_charmap import encoding_map, decoding_map


class InvertCapsCodec(codecs.Codec):
    "Stateless encoder/decoder"

    def encode(self, input, errors='strict'):
        return codecs.charmap_encode(input, errors, encoding_map)

    def decode(self, input, errors='strict'):
        return codecs.charmap_decode(input, errors, decoding_map)


class InvertCapsIncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        data, nbytes = codecs.charmap_encode(input,
                                             self.errors,
                                             encoding_map)
        return data


class InvertCapsIncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        data, nbytes = codecs.charmap_decode(input,
                                             self.errors,
                                             decoding_map)
        return data


class InvertCapsStreamReader(InvertCapsCodec, codecs.StreamReader):
    pass


class InvertCapsStreamWriter(InvertCapsCodec,codecs.StreamWriter):
    pass

def find_invertcaps(encoding):
    """Return the codec for 'invertcaps'.
    """
    if encoding == 'invertcaps':
        return codecs.CodecInfo(
            name='invertcaps',
            encode=InvertCapsCodec().encode,
            decode=InvertCapsCodec().decode,
            incrementalencoder=InvertCapsIncrementalEncoder,
            incrementaldecoder=InvertCapsIncrementalDecoder,
            streamreader=InvertCapsStreamReader,
            streamwriter=InvertCapsStreamWriter,
        )
    return None


codecs.register(find_invertcaps)

# Stateless encoder/decoder
encoder = codecs.getencoder('invertcaps')
text = 'abcDEF'
encoded_text, consumed = encoder(text)
print('Encoded "{}" to "{}", consuming {} characters'.format(
    text, encoded_text, consumed))

# Stream writer
import io
buffer = io.BytesIO()
writer = codecs.getwriter('invertcaps')(buffer)
print('StreamWriter for io buffer: ')
print('  writing "abcDEF"')
writer.write('abcDEF')
print('  buffer contents: ', buffer.getvalue())

# Incremental decoder
decoder_factory = codecs.getincrementaldecoder('invertcaps')
decoder = decoder_factory()
decoded_text_parts = []
for c in encoded_text:
    decoded_text_parts.append(
        decoder.decode(bytes([c]), final=False)
    )
decoded_text_parts.append(decoder.decode(b'', final=True))
decoded_text = ''.join(decoded_text_parts)
print('IncrementalDecoder converted {!r} to {!r}'.format(
    encoded_text, decoded_text))
    
# output
Encoded "abcDEF" to "b'ABCdef'", consuming 6 characters
StreamWriter for io buffer:
  writing "abcDEF"
  buffer contents:  b'ABCdef'
IncrementalDecoder converted b'ABCdef' to 'abcDEF'
```

无状态编解码器基类是 `Codec` ，使用新的实现重写了 `encode()` 和 `decode()` （这个例子中，分别调用了 `charmap_encode()` 和 `charmap_decode()`）。每个方法必须返回一个包含转换数据元祖以及消费的输入字节或者字符的数量。

`IncrementalEncoder` 和 `IncrementalDecoder` 作为增量接口的基类。增量类的 `encode()` 和 `decode()` 方法是这样定义的，它们只返回实际转换后的数据。然和有关缓冲池的信息都将保存为内部状态。「invertcaps」不需要缓冲数据（它使用一对一映射）。对于根据正在处理的数据产生不同输出量的编码（例如压缩算法），`BufferedIncrementalEncoder` 和 `BufferedIncrementalDecoder` 是更合适的基类，因为他们管理输入的未处理部分。

`StreamReader` 和 `StreamWriter` 也需要 `encode()` 和 `decode()` 方法，并且由于他们需要返回与 `Codec` 版本相同的值，因此可以使用多重继承来实现。 

 

## 参考

1. [Managing File System Permissions](https://pymotw.com/3/os/index.html#os-stat)  Discussion of `os.stat()` and `os.lstat()`.

2. [glob](https://pymotw.com/3/glob/index.html#module-glob) Unix shell pattern matching for filenames

3. [PEP 428](https://www.python.org/dev/peps/pep-0428) The pathlib module

4. [Pattern Matching Notation](http://www.opengroup.org/onlinepubs/000095399/utilities/xcu_chap02.html#tag_02_13) An explanation of globbing from The Open Group’s Shell Command Language specification.

5. [Standard library documentation for linecache](https://docs.python.org/3.6/library/linecache.html) 

   `linecache` 模块可以从文件或者导入的 `Python` 模块中检索文本行，并保存结果的缓存，使得同一文本的多行读取效率更高。处理 `Python` 源文件时，`linecache` 模块通常用于 `Python` 标准库的其它部分。缓存实现了在内存中保存文件内容（解析为单独的行）。`API` 通过索查询引列表返回请求的行，相比反复读取文件并解析行然后找到所需的内容，这样节省了很多时间。这个方法在查找同一个文件中的多行时尤其有用，，例如为错误报告生成跟踪记录（**traceback**）。

   

   常用的方法是 `getline` ，可以读取特定的行，并且是原生字符串（即空行返回 “\n”），而且使用此方法是对超过文件行值的行数会返回空字符串

6. `encodings` – Package in the standard library containing the encoder/decoder implementations provided by Python.

7. [**PEP 100**](https://www.python.org/dev/peps/pep-0100) – Python Unicode Integration PEP.

8. [Unicode HOWTO](https://docs.python.org/3/howto/unicode.html) – The official guide for using Unicode with Python.

9. [Text vs. Data Instead of Unicode vs. 8-bit](https://docs.python.org/3.0/whatsnew/3.0.html#text-vs-data-instead-of-unicode-vs-8-bit) – Section of the “What’s New” article for Python 3.0 covering the text handling changes.

10. [Python Unicode Objects](http://effbot.org/zone/unicode-objects.htm) – Fredrik Lundh’s article about using non-ASCII character sets in Python 2.0.

11. [How to Use UTF-8 with Python](http://evanjones.ca/python-utf8.html) – Evan Jones’ quick guide to working with Unicode, including XML data and the Byte-Order Marker.

12. [On the Goodness of Unicode](http://www.tbray.org/ongoing/When/200x/2003/04/06/Unicode) – Introduction to internationalization and Unicode by Tim Bray.

13. [On Character Strings](http://www.tbray.org/ongoing/When/200x/2003/04/13/Strings) – A look at the history of string processing in programming languages, by Tim Bray.

14. [Characters vs. Bytes](http://www.tbray.org/ongoing/When/200x/2003/04/26/UTF) – Part one of Tim Bray’s “essay on modern character string processing for computer programmers.” This installment covers in-memory representation of text in formats other than ASCII bytes.

15. [Endianness](https://en.wikipedia.org/wiki/Endianness) – Explanation of endianness in Wikipedia.

16. [W3C XML Entity Definitions for Characters](http://www.w3.org/TR/xml-entity-names/) – Specification for XML representations of character references that cannot be represented in an encoding.