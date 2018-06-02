**目录**

[toc]

## `pandas` 类型处理

1. `astype` 类型强制转换

`Pandas` 可以使用 `astype` 进行强制类型转换，转换需要具有几个常用条件：1）数据整洁性，这样可以容易被转换；2）数值类型转换字符串类型比较容易。但是需要注意 `ValueError` 报错类型：

```
# 报错：因为对于某些字符串类型或者逗号分隔无法顺利进行数值类型转换
ValueError: could not convert string to float: '$15,000.00'

ValueError: invalid literal for int() with base 10: 'Closed'
```

这个是说强之类型转换失败，上面两个错误：第一个是因为第一个有逗号及单位符号；第二个错误是因为 `cloed` 是字符串。

⚠️另外需要注意的是，当使用 `astype('bool')` 转换为逻辑类型的时候，非空字符串都会被转换为 `True`
