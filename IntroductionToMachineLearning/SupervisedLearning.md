**目录**

[TOC]

## 简介

监督式学习，是对有 `label` 标记的 `training example` 进行学习的问题（这个过程是一个启发式( heuristics) 的过程）。一般情况下的，通用的公式：$Y=f(X)+\epsilon$，其公式的参数解释：

* $X$ (input) 
* $Y$ (output)
* $f$ (function) : 描述了 $X$ 和 $Y$ 之间的关系的函数
* $\epsilon$ (epsilon):  **平均值为 $0$ ** 的随机误差项
  *  **不可约误差( Irreducible Error )** $^{[1]}$ ，这是因为数据集中存在的噪声，在理论的极限范围内，它也会被模型算法给体现出来。这个就像用模型来模拟抛硬币的结果，它不可能得到绝对正确的结果
  * 还有一类误差是，因为创建的条件匹配的模型，并不能在实际复杂的数据集中得到良好的表现结果

### 名词解释

* 特征( **Features** )：一般指数据属性。而数据可能是数值型数据（**Numerical**），也有可能是类别性数据（**Categorical**）





## 参考

1. [利用学习曲线诊断模型的偏差和方差 ](https://www.jiqizhixin.com/articles/2018-01-23)

2. [LinearAlgebra](http://www.deeplearningbook.org/contents/linear_algebra.html)

   解释了线性代数的常用知识:

   * **Scalers**: 仅指单一数字，可能是一个自然数或者实数
   * **Vectors**：数值数组 $\mathbb{R}^n$ ——表示了 $n$ 行数据；
   * **Matrices**：二维数值数组，一般用  $\it{A}\in{\mathbb{R}^{m\times{n}}}$ 表示 $m$ 行 $n$ 列数组，其元素表示 $\it{A}_{i,j}$
   * **Tensors**：超过二维的数组， 一般用 $\bold{A}$ ，其元素表示方法为 $\bold{A}_{i,j,k}$

   **Matrix** 运算：

   * 加法运算：$\it{C_{i,j}}=\it{A_{i,j}}+\it{B_{i,j}}$
   * 标量乘积和标量加：$\it{D_{i,j}}=a\dot{}\it{B_{i,j}} +c$
   * 向量加：$\it{C_{i,j}}=\it{A_{i,j}}+b_{j}$，向量会隐形转换为 $i$ 行进行运算
   * 乘积运算（即 **dot product**）：$\it{C_{i,j}}=\displaystyle \sum_{k} \it{A_{i,k}}\it{B_{k,j}}$，这个和每个元素级别的相乘不同（注意：向量的乘法也遵从同维度性要求 $\it{x}^T\it{y}$），元素的相乘（即 **Hadamard product**）的表示方法是 $\it{A}\bigodot\it{B}$
   * 分配律（**distributive**）$\it{A}(\it{B}+\it{C})=\it{AB}+\it{AC}$
   * 结合律（**associative**）$\it{A}(\it{B}\it{C})=(\it{A}\it{B})\it{C}$，需要注意维度要求，另外矩阵的交换律不一定相等，然而向量交换律一定相等

   单位矩阵（**Identity Matrix**）：

   - 定义：当乘以任何向量时，不会改变向量的矩阵。$\forall \it{x} \in \mathbb{R^n}, \mit{I_n}\it{x}=\it{x}$
   - 特点：沿着对角线上值为 $1$，而其他值为 $0$

   矩阵逆（**Inverse Matrix**）：

   - 定义：$\it{A}$ 的逆表示 $\it{A}^{-1}$。$\it{A^{-1}A}=\it{I_n}$
   - 作用：可逆矩阵可以用于求解值 $\it{I_nx}=\it{A^{-1}b}$，它是由该公式推导出来的 $\it{A^{-1}Ax}=\it{A^{-1}b}$

   奇异矩阵（**Singular Matrix**）和 方阵（**Square Matirx**）：

   - 当 $\mathbb{R^{m\times{n}}}$ 中 $m=n$ 时，且所有的列是线性不相关（**Linear Independent**），那么这样的矩阵即为方阵
   - 当 $\mathbb{R^{m\times{n}}}$ 中 $m=n$ 时，且所有的列是线性相关（**Linear Dependent**），那么这样的矩阵即为奇异矩阵

   范数（**Norms**）：包括了 $L^p​$ 范数

   * 计算方式 $ \shortparallel \bold x \shortparallel_p=(\displaystyle\sum_i\mid x_i\mid ^p)^{\frac{1}{p}}$，其中 $p\in\mathbb{R}, p\ge1$
   * 特性：1）$f(x)=0\to x=0$；2）$f(x+y)\leq f(x) + f(y)$，即三角不等式性质；3）$\forall \alpha \in \mathbb{R}, f(\alpha x)=|\alpha|f(x)$
   * 当 $p=2$ 时，即计算的是欧式范数（**Euclidean Norm**）。它在机器学习中的实际应用，因为它针对邻近 **Origin** 的元素增长缓慢，  难以区分各元素是真为 $0$ 还是值很小但并不为 $0$。
   * 当 $p=1$，即 $\it{L^1}$ 范数，$\shortparallel{x}\shortparallel_{1}=\displaystyle{\sum_i|x_i|}$。它的实际应用是解决了欧式范数难以区分 $0$ 和值很小的情况
   * 当 $p=\infin$， 计算的是 $L^{\infin}$ 表示的是 **Max Norm**，$\shortparallel{x}\shortparallel_{\infin}=\displaystyle{\max_i}|x_i|$
   * 在深度学习中，常用的范数是弗罗贝尼乌斯範数（**Frobenius norm**）或希尔伯特-施密特範数（**Hilbert–Schmidt norm**），它是模拟了向量的欧式范数计算方式，$\parallel{A}\parallel_F=\sqrt{\displaystyle{\sum_{i,j}A_{i,j}^2}}$，

   







## 补充

1. `The primary difference between this and human learning is that machine learning runs on computer hardware and is best understood through the lens of computer science and statistics, whereas human pattern-matching happens in a biological brain (while accomplishing the same goals). `

   在文中看见了这句话，这里强调了 `human learning` 和 `machine learning` 的区别是“硬件”的区别，不敢苟同——人是一个“有机”系统，这个带来了更大的波动性。就目前看来尚未看见一个 “有机” `machine` 的。这点思考是基于 《反脆弱》的思路模式。

