**目录**

[toc]

## `pandas` 类型处理${^{[1]}}$

1. `astype` 类型强制转换

	`Pandas` 可以使用 `astype` 进行强制类型转换，转换需要具有几个常用条件：1）数据整洁性，这样可以容易被转换；2）数值类型转换字符串类型比较容易。但是需要注意 `ValueError` 报错类型：
	
	```
	# 报错：因为对于某些字符串类型或者逗号分隔无法顺利进行数值类型转换
	ValueError: could not convert string to float: '$15,000.00'
	
	ValueError: invalid literal for int() with base 10: 'Closed'
	```
	
	这个是说强之类型转换失败，上面两个错误：第一个是因为第一个有逗号及单位符号；第二个错误是因为 `cloed` 是字符串。
	
	⚠️另外需要注意的是，当使用 `astype('bool')` 转换为逻辑类型的时候，非空字符串都会被转换为 `True`

2. 定制化类型转换——`apply` 方法使用

	该方法比较 **elegent**，因为它解决了 `astype` 对数据不整洁的转化报错的问题。其 **核心逻辑** 是利用利用函数（同样可以使用 `lambda` 匿名函数来解决问题）将数据直接解析转换为另一个数据类型。
	
	```{Python}
	def convert_currency(val):
	    """
	    Convert the string number value to a float
	     - Remove $
	     - Remove commas
	     - Convert to float type
	    """
	    new_val = val.replace(',','').replace('$', '')
	    return float(new_val)
	    
	# 使用 apply 方法调用函数
	df['2016'].apply(convert_currency)
	```

3. 功能性方法使用

	功能性方法是 `pandas` 自带方法，它们可以针对某些类型的数据进行转换，例如：`pd.to_datetime()`、`pd.to_numerical`。相关方法可以查询相关文档。

4. 类型转换的高阶应用

	它的重要作用是，将以上的方法直接应用到数据读取中，提高了数据读取效率。**核心逻辑** 是 `pandas` 的 `read` 方法中的 `converters` 参数。使用举例如下（不对数据进行解释，主要注意转换方法）：
	
	```{python}
	df = pd.read_csv("sales_data_types.csv",
	                   dtype={'Customer Number': 'int'},
	                   converters={'2016': convert_currency,
	                               '2017': convert_currency,
	                               'Percent Growth': convert_percent,
	                               'Jan Units': lambda x: pd.to_numeric(x, errors='coerce'),
	                               'Active': lambda x: np.where(x == "Y", True, False)
	                              })
	```

## 参考
1. [Overview of Pandas Data Types - Practical Business Python](http://pbpython.com/pandas_dtypes.html)
