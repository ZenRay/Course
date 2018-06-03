**目录**

[toc]

## 解决 `GitHub` 中不能对 `Latex` 公式渲染
这个是因为 `GitHub` 本身的 `markdown` 解析是一个不支持 `Latex` 的库${^{[1]}}$，所以没有从设置的角度来解决 `GitHub` 不能渲染的问题。这里的思路是将对象转换为一个 `HTML` 的对象，来使其在网页端被渲染。而使用的对象是通过[第三方在线 LaTeX 公式编辑器](https://www.codecogs.com/latex/eqneditor.php) 进行创建了一个对象等方式。例如需要添加 `y=ax+b` 的公式，那么可以通过添加 `img` 对象来实现或者 `img` 这个 `html`  标签实现：

```
![](https://latex.codecogs.com/gif.latex?y=ax&plus;b" title="y=ax+b)
// HTML 方式
<img src="https://latex.codecogs.com/gif.latex?y=ax&plus;b" title="y=ax+b" />
```

结果如下：

![](https://latex.codecogs.com/gif.latex?y=ax&plus;b)



## 参考
1. [How to show math equations in general github's markdown(not github's blog)](https://stackoverflow.com/questions/11256433/how-to-show-math-equations-in-general-githubs-markdownnot-githubs-blog)
