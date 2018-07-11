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

```
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

  

