**目录**

[TOC]

### 可用 pakcage 及其方法

#### 1. 文本常量常用`package`

目前使用的 `Python` 版本是 `3.6.5`，用到的 `package` 为 `string`，其中的类和函数方法：

```python
"Formatter","Template","_ChainMap","_TemplateMetaclass","__all__","__builtins__","__cached__","__doc__","__file__","__loader__","__name__","__package__","__spec__","_re","_string","ascii_letters","ascii_lowercase","ascii_uppercase","capwords","digits","hexdigits","octdigits","printable","punctuation","whitespace"
```

* `capwords`：作用是将首字母大写，相当于字符串的 `title` 属性

* `maketrans` 和 `translate`：这两个方法被移动到了 `str` 中，这个两个的作用是通过 `maketrans` 来创建一个“密码字典”，使用 `translate` 来将字符串中对应到“密码字典”中的“键值”。在用法上，和 `pandas` 中的 `map` 属性很相似（它是直接通过字典来解决键值映射）

  ```python
  # note: str 不需要 import
  leet = str.maketrans("ab", "12")
  
  s = "tada, backup"
  
  s.translate(leet)
  
  # output
  t1d1, 31cku2
  ```



##### `Template` 常用方法

`Template`：它的类型是 `string._TemplateMetaclass`，作用是创建一个模版，以变量名的方式（通过在变量名前面添加前缀 `$`来标识变量，如果需要与两侧的文本进行区分，可以使用大括号进行区分）来引用相应的值。在创建了一个对象之后，可以使用 `substitute` 进行对应变量替换；另外还可以使用 `safe_substitute` 方法来进行安全替换，以避免未能提供模版所需要的全部参数时发生异常

```python
# 使用一个简单模版和一个使用 % 操作符的类似字符串拼接进行比较，也就是说通过 $ 和 % 来作为粗发器字符完成转义。其中 % 就是相当于格式化字符串的方式
import string

# initial the variable name
values = {"var":"foo"}

# create the template
template = string.Template("""
Variable		: $var
Escape			: $$
Variable in text: ${var}iable
""")

print("Template:", template.substitute(values))

# output
Template:
Variable		: foo
Escape			: $
Variable in text: fooiable


second_template = """
Variable		: %(var)s
Escape			: %%
Variable in text: %(var)siable
"""

print("Interpolation:", second_template % values)

# output
Variable		: foo
Escape			: %
Variable in text: fooiable
    
# 使用 safe_substitute 进行替换

third_template = string.Template("$var is here but $missing is not provided")

try:
    print("Substitute:", third_template.substitute(values))
except KeyError, err:
    print("ERROR:", str(err))
# output
ERROR: 'missing'
    
print("Safe_Substitute:", third_template.safe_substitute(values))

# output
Safe_Substitute: foo is here but $missing is not provided
```

**注意⚠️：** 使用字符串进行拼接（interpolation）时，使用`%` 进行转义的时候需要对变量名之后添加一个 `s` 以指示说明替换字符串。另外使用的键值来映射的话，需要使用小括号将变量名给包裹

以上两者在实际情况下，存在某些区别：模版不考虑参数类型；而格式化字符串转换需要转换为字符串

##### Template 高级用法

模板本质上是使用的正则表达式的方式（注意创建的 `template` 可以通过 `template.pattern` 下的属性方式来查询到相关的正则表达式），因此可以通过修改相应的类属性（例如 `delimiter` 和 `idpattern`）

```python
import string
template_text = """
	delimiter	: %%
	replaced	: %with_underscore
	ignored		: %notunderscore
"""

d = {"with_underscore":"replaced",
	"notunderscored":"not replaced"}
	
# 这里是新创建了一个 Template 类以更改原有相关属性
class MyTemplate(string.Template):
	delimiter = "%"
	idpattern = "[a-z]+_[a-z]+"		# 注意这要求了需要下划线
	
t = MyTemplate(template_text)

print(t.safe_substitute(d))

# output
delimiter	: %
replaced	: replaced
ignored		: %notunderscore
    
# print the four name group
print(t.pattern.pattern)
    \%(?:
      (?P<escaped>\%) |   # Escape sequence of two delimiters
      (?P<named>[a-z]+_[a-z]+)      |   # delimiter and a Python identifier
      {(?P<braced>[a-z]+_[a-z]+)}   |   # delimiter and a braced identifier
      (?P<invalid>)              # Other ill-formed delimiter exprs
    )
```

在所用的正则表达式模式中，提供了 4 个命名组，分别是**转义定界符**、**命名变量**、**用大括号括住的变量名**以及**不合法的定界符模式**。下面演示定制化模式命名组值：

```python
import re
import string

class MyTemplate(string.Template):
    delimiter = "{{"
    pattern = r"""
    \{\{(?:
    (?P<escaped>\{\{)|
    (?P<named>[_a-z][_a-z0-9]*)\}\}|
    (?P<braced>[_a-z][_a-z0-9]*)\}\}|
    (?P<invalid>)
    )"""

t = MyTemplate("""
{{{{
{{var}}
""")

print("matches:", t.pattern.findall(t.template))
# output
[('{{', '', '', ''), ('', 'var', '', '')]
print("substitued:", t.safe_substitute(var="replacement"))
# output 
substitued:
{{
replacement
```



#### 2. 格式化文本段落

通过调整换行符在段落中的位置来格式化文本，使用的 `package` 为 `textwrap`，其中属性如下：

```python
"TextWrapper", "__all__", "__builtins__", "__cached__", "__doc__", "__file__", "__loader__", "__name__", "__package__", "__spec__", "_leading_whitespace_re", "_whitespace", "_whitespace_only_re", "dedent", "fill", "indent", "re", "shorten", "wrap"
```

* `fill` 以文本作为输入参数，以及使用 `width` 来控制输出宽度。但是该方式保留了文本中的原生空格（例如文档字符串每行开头空白），被嵌入到新的段落中

  ```python
  import textwrap
  
  textwrap.fill(text, width=50)
  ```

* `dedent` 删除所有行中都有的空白符前缀，但是也仅仅是相当于减少了缩进

  可以将 `fill` 和`dedent` 结合使用，同时还可以调整 `fill` 的其他参数来单独控制第一行的缩进，以区别后面没行。

  ```python
  import textwrap
  # dedent text
  dedented_text = textwrap(text).strip()
  
  textwrap.fill(dedented_text,
               initial_indent="",				# 第一行不变化
               subsequent_indent=" " * 4,		# 后续需要增加缩进，⚠️缩进值可以选择其他字符
               width=50,
               )
  ```

  

#### 3. 正则表达式

* 匹配模式指示符

  正式表达式 `pattern` 构建中，可以使用标志以说明相应的搜索选项。另外可以使用冒号加缩写符结合的方式（例如不区分大小写，可以使用 ?i ），指示如何计算和解析表达式，所以需要放在表达式最前面——主要也是针对不方便些出匹配模式的表达式

|    标志    | 缩写 | 作用                                                         |
| :--------: | :--: | ------------------------------------------------------------ |
| IGNORECASE |  i   | 不区分大小写匹配模式                                         |
| MULTILINE  |  m   | 多行输入模式，控制匹配模式对包含换行符的文本进行锚定命令。并且对开头和结尾添加 `^` 和 `$` |
|   DOTALL   |  s   | 多行输入模式，运行使用点符号匹配换行符；一般情况下，点符号（.）可以与除换行符以外的所有字符进行匹配 |
|  UNICODE   |  u   |                                                              |
|  VERBOSE   |  x   | 详细表达式表示，可以使用文档字符串来建 pattern，并且可以用 # 来进行注释 |

​	下面使用缩写方式，来对各个命名组说明匹配模式举例：

```python
import re

pattern = r"(?imu)\bT\w+"
regex = re.compile(pattern)		# 这里使用多种匹配模式，不区分大小写，多行输入以及 unicode 编码
```

* 匹配方向——前向和后向

  针对匹配的模式中的部分，但是还需要同时匹配模式中某部分，才能算完全匹配。例如：`Email` 中的尖括号需要两个都存在或者都不存在时，才算匹配。而前向断言语法为 `(?=pattern)`，否定前向断言语法为 `(?!pattern)`——要求匹配模式不匹配当前位置后面的文本

  ```python
  # 向前断言示例
  import re
  
  address = re.compile(
      '''
      # A name is made up of letters, and may include "."
      # for title abbreviations and middle initials.
      ((?P<name>
         ([\w.,]+\s+)*[\w.,]+
       )
       \s+
      ) # name is no longer optional
  
      # LOOKAHEAD
      # Email addresses are wrapped in angle brackets, but only
      # if both are present or neither is.
      (?= (<.*>$)       # remainder wrapped in angle brackets
          |
          ([^<].*[^>]$) # remainder *not* wrapped in angle brackets
        )
  
      <? # optional opening angle bracket
  
      # The address itself: username@domain.tld
      (?P<email>
        [\w\d.+-]+       # username
        @
        ([\w\d.]+\.)+    # domain name prefix
        (com|org|edu)    # limit the allowed top-level domains
      )
  
      >? # optional closing angle bracket
      ''',
      re.VERBOSE)
  
  candidates = [
      u'First Last <first.last@example.com>',
      u'No Brackets first.last@example.com',
      u'Open Bracket <first.last@example.com',
      u'Close Bracket first.last@example.com>',
  ]
  
  for candidate in candidates:
      print('Candidate:', candidate)
      match = address.search(candidate)
      if match:
          print('  Name :', match.groupdict()['name'])
          print('  Email:', match.groupdict()['email'])
      else:
          print('  No match')
          
  # output
  Candidate: First Last <first.last@example.com>
    Name : First Last
    Email: first.last@example.com
  Candidate: No Brackets first.last@example.com
    Name : No Brackets
    Email: first.last@example.com
  Candidate: Open Bracket <first.last@example.com
    No match
  Candidate: Close Bracket first.last@example.com>
    No match
  ```

  针对否定前向断言的示例：

  ```python
  import re
  
  address = re.compile(
      '''
      ^
  
      # An address: username@domain.tld
  
      # Ignore noreply addresses
      (?!noreply@.*$)
  
      [\w\d.+-]+       # username
      @
      ([\w\d.]+\.)+    # domain name prefix
      (com|org|edu)    # limit the allowed top-level domains
  
      $
      ''',
      re.VERBOSE)
  
  candidates = [
      u'first.last@example.com',
      u'noreply@example.com',
  ]
  
  for candidate in candidates:
      print('Candidate:', candidate)
      match = address.search(candidate)
      if match:
          print('  Match:', candidate[match.start():match.end()])
      else:
          print('  No match')
          
  # output
  
  Candidate: first.last@example.com
    Match: first.last@example.com
  Candidate: noreply@example.com
    No match
  ```

  在其他匹配方向上，还可以选择**否定后向断言（negative look-behind assertion）**的模式`(?<!pattern)` ；另外还可以使用 **肯定后向断言（positive look-behind assertion）**的模式 `(?<=pattern)`

  ```python
  # 不要用前向检查 Email 地址 username 部分中的 noreply 的否定后向断言模式
  
  import re
  
  address = re.compile(
      '''
      ^
  
      # An address: username@domain.tld
  
      [\w\d.+-]+       # username
  
      # Ignore noreply addresses
      (?<!noreply)
  
      @
      ([\w\d.]+\.)+    # domain name prefix
      (com|org|edu)    # limit the allowed top-level domains
  
      $
      ''',
      re.VERBOSE)
  
  candidates = [
      u'first.last@example.com',
      u'noreply@example.com',
  ]
  
  for candidate in candidates:
      print('Candidate:', candidate)
      match = address.search(candidate)
      if match:
          print('  Match:', candidate[match.start():match.end()])
      else:
          print('  No match')
      
  # output
  Candidate: first.last@example.com
    Match: first.last@example.com
  Candidate: noreply@example.com
    No match
  ```

  肯定后向断言的方式示例，这里只要字符序列前面有一个 `@` 就匹配：

  ```python
  import re
  
  twitter = re.compile(
      '''
      # A twitter handle: @username
      (?<=@)
      ([\w\d_]+)       # username
      ''',
      re.VERBOSE)
  
  text = '''This text includes two Twitter handles.
  One for @ThePSF, and one for the author, @doughellmann.
  '''
  
  print(text)
  for match in twitter.findall(text):
      print('Handle:', match)
      
  # output
  This text includes two Twitter handles.
  One for @ThePSF, and one for the author, @doughellmann.
  
  Handle: ThePSF
  Handle: doughellmann
  ```

* 自引用表达式

  匹配的值需要被用在表达式后面，例如匹配到的`Email` 中需要将匹配到的用户的姓和名拆开使用。要解决这个问题，可以使用 `\num` ——即反斜杠和数字——的方式模拟 `id` 的方式对匹配到的值分组。但是⚠️表达式改变时，这些组就必须重新编号；另外最多只能创建 99 个引用。

  ```python
  import re
  
  address = re.compile(
      r'''
  
      # The regular name
      (\w+)               # first name
      \s+
      (([\w.]+)\s+)?      # optional middle name or initial
      (\w+)               # last name
  
      \s+
  
      <
  
      # The address: first_name.last_name@domain.tld
      (?P<email>
        \1               # first name
        \.
        \4               # last name
        @
        ([\w\d.]+\.)+    # domain name prefix
        (com|org|edu)    # limit the allowed top-level domains
      )
  
      >
      ''',
      re.VERBOSE | re.IGNORECASE)
  
  candidates = [
      u'First Last <first.last@example.com>',
      u'Different Name <first.last@example.com>',
      u'First Middle Last <first.last@example.com>',
      u'First M. Last <first.last@example.com>',
  ]
  
  for candidate in candidates:
      print('Candidate:', candidate)
      match = address.search(candidate)
      if match:
          print('  Match name :', match.group(1), match.group(4))
          print('  Match email:', match.group(5))
      else:
          print('  No match')
          
  # output
  Candidate: First Last <first.last@example.com>
    Match name : First Last
    Match email: first.last@example.com
  Candidate: Different Name <first.last@example.com>
    No match
  Candidate: First Middle Last <first.last@example.com>
    Match name : First Last
    Match email: first.last@example.com
  Candidate: First M. Last <first.last@example.com>
    Match name : First Last
    Match email: first.last@example.com
  ```

  因为这种自引用表达式存在以上问题，所以建议使用`(?P=name)` 指示表达式中先前匹配的一个命名组的值，并将其引用到模式中

  ```python
  import re
  
  address = re.compile(
      '''
  
      # The regular name
      (?P<first_name>\w+)
      \s+
      (([\w.]+)\s+)?      # optional middle name or initial
      (?P<last_name>\w+)
  
      \s+
  
      <
  
      # The address: first_name.last_name@domain.tld
      (?P<email>
        (?P=first_name)
        \.
        (?P=last_name)
        @
        ([\w\d.]+\.)+    # domain name prefix
        (com|org|edu)    # limit the allowed top-level domains
      )
  
      >
      ''',
      re.VERBOSE | re.IGNORECASE)
  
  candidates = [
      u'First Last <first.last@example.com>',
      u'Different Name <first.last@example.com>',
      u'First Middle Last <first.last@example.com>',
      u'First M. Last <first.last@example.com>',
  ]
  
  for candidate in candidates:
      print('Candidate:', candidate)
      match = address.search(candidate)
      if match:
          print('  Match name :', match.groupdict()['first_name'],
                end=' ')
          print(match.groupdict()['last_name'])
          print('  Match email:', match.groupdict()['email'])
      else:
          print('  No match')
          
  # output
  Candidate: First Last <first.last@example.com>
    Match name : First Last
    Match email: first.last@example.com
  Candidate: Different Name <first.last@example.com>
    No match
  Candidate: First Middle Last <first.last@example.com>
    Match name : First Last
    Match email: first.last@example.com
  Candidate: First M. Last <first.last@example.com>
    Match name : First Last
    Match email: first.last@example.com
  ```

#### 4. 序列数据比较

对文本行以及序列数据，可以通过 `difflib` 进行比较，它的属性如下：

```python
"Differ", "HtmlDiff", "IS_CHARACTER_JUNK", "IS_LINE_JUNK", "Match", "SequenceMatcher", "__all__", "__builtins__", "__cached__", "__doc__", "__file__", "__loader__", "__name__", "__package__", "__spec__", "_calculate_ratio", "_check_types", "_count_leading", "_file_template", "_format_range_context", "_format_range_unified", "_legend", "_mdiff", "_namedtuple", "_nlargest", "_styles", "_table_template", "_test", "context_diff", "diff_bytes", "get_close_matches", "ndiff", "restore", "unified_diff"
```

这里主要针对任意类型的两个序列（需要值时可以被 `hash`）比较，并且能够删除对数据没有贡献的无用值。示例如下：

```python
import difflib

s1 = [1, 2, 3, 5, 6, 4]
s2 = [2, 3, 5, 4, 6, 1]

print('Initial data:')
print('s1 =', s1)
print('s2 =', s2)
print('s1 == s2:', s1 == s2)
print()

matcher = difflib.SequenceMatcher(None, s1, s2)
for tag, i1, i2, j1, j2 in reversed(matcher.get_opcodes()):

    if tag == 'delete':
        print('Remove {} from positions [{}:{}]'.format(
            s1[i1:i2], i1, i2))
        print('  before =', s1)
        del s1[i1:i2]

    elif tag == 'equal':
        print('s1[{}:{}] and s2[{}:{}] are the same'.format(
            i1, i2, j1, j2))

    elif tag == 'insert':
        print('Insert {} from s2[{}:{}] into s1 at {}'.format(
            s2[j1:j2], j1, j2, i1))
        print('  before =', s1)
        s1[i1:i2] = s2[j1:j2]

    elif tag == 'replace':
        print(('Replace {} from s1[{}:{}] '
               'with {} from s2[{}:{}]').format(
                   s1[i1:i2], i1, i2, s2[j1:j2], j1, j2))
        print('  before =', s1)
        s1[i1:i2] = s2[j1:j2]

    print('   after =', s1, '\n')

print('s1 == s2:', s1 == s2)

# output
Initial data:
s1 = [1, 2, 3, 5, 6, 4]
s2 = [2, 3, 5, 4, 6, 1]
s1 == s2: False

Replace [4] from s1[5:6] with [1] from s2[5:6]
  before = [1, 2, 3, 5, 6, 4]
   after = [1, 2, 3, 5, 6, 1]

s1[4:5] and s2[4:5] are the same
   after = [1, 2, 3, 5, 6, 1]

Insert [4] from s2[3:4] into s1 at 4
  before = [1, 2, 3, 5, 6, 1]
   after = [1, 2, 3, 5, 4, 6, 1]

s1[1:4] and s2[0:3] are the same
   after = [1, 2, 3, 5, 4, 6, 1]

Remove [1] from positions [0:1]
  before = [1, 2, 3, 5, 4, 6, 1]
   after = [2, 3, 5, 4, 6, 1]

s1 == s2: True
```

在上面的代码中 `matcher.get_opcodes()` ，其实是 `difflibg.get_opcodes()` 方法，它可以得到四种数据处理方式：

| Opcode  | Definition                         |
| ------- | ---------------------------------- |
| replace | Replace `a[i1:i2]` with `b[j1:j2]` |
| delete  | Remove `a[i1:i2]` entirely         |
| insert  | Insert `b[j1:j2]` at `a[i1:i1]`    |
| equal   | The subsequences are already equal |





### 参考

1. 正则表达式
   * [Wikipedia: Regular expression](https://en.wikipedia.org/wiki/Regular_expressions)
   * [pythex](http://pythex.org/)– A web-based tool for testing regular expressions created by Gabriel Rodríguez. Inspired by Rubular.
   * [Kodos](http://kodos.sourceforge.net/)– An interactive regular expression testing tool by Phil Schwartz.
   * [Regular Expression HOWTO](https://docs.python.org/3.5/howto/regex.html)– Andrew Kuchling’s introduction to regular expressions for Python developers