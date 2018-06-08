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

## 去除 `matplotlib` 绘图中科学计数标记
对于数据偏大时，绘图的坐标轴中会显示 `1e7`——即表示坐标刻度表示为 ${\times10^7}$，但是在实际绘图过程中可能并不需要显示相关计数方式。因此需要对相关对象进行调整，绘图中刻度标签是由 `formatter` 进行控制的，它有一个专门的对象[ScalarFormatter](https://matplotlib.org/api/ticker_api.html#matplotlib.ticker.ScalarFormatter)。但是可以通过其他接口完成图像的调整——即 `ax=plt.gca()` 方法获取得到的对象，之后进行其他相关的设置(需要使用其他方法， `get_major_formatter` 来得到 `formatter` 对象)：

```{Python}
ax = plt.gca()	# 得到对象接口
ax.get_xaxis().get_major_formatter().set_scientific(False)	# 分别是得到 x 坐标轴对象，得到主坐标轴的 formatter，设置取消科学计数标记
```


## `pandas` 中对时间类型转换
目前遇到比较多的时间类型转换的问题，主要是集中在字符串(即 `object` 类型)需要转换为 `timestamp` 类型。最近发现了一个比较好的方式，如果字符串数据是完全保留了 `timestamp` 模式的数据，而只是数据格式问题的话，那么可以通过 `apply` 方法传入 `pandas.Timestamp` 的方式来解决转换，具体事例如下：

```{Python}
twitter_archive_data_copy["timestamp"][:3]

# output 

0    2017-08-01 16:23:56 +0000
1    2017-08-01 00:17:27 +0000
2    2017-07-31 00:18:03 +0000
Name: timestamp, dtype: object

# transform the data type
twitter_archive_data_copy["timestamp"] = twitter_archive_data_copy["timestamp"].apply(pd.Timestamp)

twitter_archive_data_copy["timestamp"][:2]

# output

0   2017-08-01 16:23:56+00:00
1   2017-08-01 00:17:27+00:00
Name: timestamp, dtype: datetime64[ns, UTC]
```

## 参考
1. [Overview of Pandas Data Types - Practical Business Python](http://pbpython.com/pandas_dtypes.html)
