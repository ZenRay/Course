**目录**

[TOC]

## 简介

监督式学习，是对有 `label` 标记的 `training example` 进行学习的问题（这个过程是一个启发式( heuristics) 的过程）。一般情况下的，通用的公式：$Y=f(X)+\epsilon$，其公式的参数解释：

* $X$ (input) 
* $Y$ (output)
* $f$ (function) : 描述了 $X$ 和 $Y$ 之间的关系的函数
* $\epsilon$ (epsilon):  **平均值为 $0$ ** 的随机误差项
  *  **不可约误差( Irreducible Error )** $^{[1]}$ ，这是因为数据集中存在的噪声，在理论的极限范围内，它也会被模型算法给体现出来。这个就像用模型来模拟抛硬币的结果，它不可能得到绝对正确的结果
  *  还有一类误差是，因为创建的条件匹配的模型，并不能在实际复杂的数据集中得到良好的表现结果

监督式学习算法中，包括了线性回归（**Linear Regression**）和分类（**Classification**）。

### 线性回归

线性回归——最小二乘回归（**Ordinary Least Squares(OLS) Resgress**）

* 利用给定的 $X$ 得到新的 $y$ 以尽可能小的误差来学习线性模型

* 原理：线性回归是假定存在 $X$ 和 $y$ 的函数形式的参数法（**Parametric Method**），$\hat{y}=\beta_0+\beta_1*x+\epsilon$。目标是通过学习模型参数 $\beta_0$ 和 $\beta_1$ 来最小化模型预计的误差

* 步骤：

  1. 定义损失函数（**Cost Function** 或者 **Loss Function**）用于评估模型预计值的不准确度

     损失函数 $Cost=\frac{\displaystyle{\sum_i^n((\beta_1x_i+\beta_0)-y_i)^2}}{2*n}$，其中 $n$ 为数据规模，其中在分母中使用 $2*n$ 是为了方便在求导计算最小损失时，让表达式更清洁。然而随着损失函数的复杂度增加（例如 $\beta$ 参数数量增加，数据特征增加），难以通过微积分法来实现求解。因此引入了另一种迭代方法——梯度下降（**Gradient Descent**），它可以见下损失函数的复杂性。

     梯度下降的目标是找到模型的损失函数的最小值，其需要通过不断的迭代来得到越来越近似的值。即每一步都沿着“坡度”下降最大的一步来做，当达到越来越平坦时即是较优解。算法收敛（**Converged**）和损失值的最小化，表示最终取得了较优解

  2. 找到损失值最小的参数

### 分类

分类的结果是预测的离散型 `label` ，是为了解决观测值可能是属于哪一个类别（**class**）

#### 逻辑回归

* 逻辑回归（**Logistic Regression**）一种分类方法，模型输出的结果是分类属于哪一个类的概率。逻辑回归不仅可以进行分析二分类（**Binary Classification**），而且可以进行多类别分类——例如数字识别。常用的例子，信用欺诈分析。

  > 最小二乘法不适用于二分类问题，因为预测的结果是 $0$ 或者 $1$，预测得到的概率是小于 0 或者大于 1 的，这样导致概率没有意义。因此需要使用逻辑回归模型，这样得到的概率值就是在 $0\%$ 和 $100\%$ 之间以此来确认结果属于哪个类别

* 数学原理：

  这里使用的是 **Sigmoid** 函数， $S(x)=\frac{1}{1+e^{-x}}$。而在实际应用层面上，模型是一个复合函数，$。P(Y=1|x)=F(g(x))=\frac{1}{1+e^{-(\beta_0+\beta_1*x)}}$通过数学方式转换可以转换为一个“线性模型”， $\ln(\frac{p}{1-p})=\beta_0+\beta_1x+\epsilon$，这样就转换为了一个自然对数的 **Odds Ratio($\frac{p}{1-p}$)**。需要注意⚠️ $\beta_1$ 参数表示的是随着 $x$ 变化，**log-odds ratio** 的变化率——即是 **log-odds** 的斜率，而非概率的斜率

  ![odd_ratio](../img/odd_ratio.png)

* 阈值（**Threshold**）

  阈值的设定，指示了分类问题的概率划分。**依据** 于具体任务对假正例（**False Positives**）和假负例（**False Negative**）忍耐，因为不同的时间对两者要求存在差异

* 损失函数

  $Cost(\beta)=\frac{\displaystyle{\sum_{i=1}^n}(y^i\log(h_{\beta}(x^i))+(1-y^i)\log(1-h_{\beta}(x^i))^2}{2*n}+\lambda\displaystyle{\sum_{j=1}^k}\beta_j^2$，该函数包括了第一部分数据损失，以及第二部分正则损失。需要注意这里的损失函数是最大似然数的方式来推导的，这个[逻辑回归损失函数解释 ](https://www.zhihu.com/question/47744216/answer/146117429)说明了它的推导方式。

#### 支持向量机(`SVM`)

`SVM` 是一个参数模型，主要解决的也是二分类问题，并且和逻辑回归有同样的优异表现；但是它是以几何的角度来建立的模型，而非概率角度建立模型。

* 原理：`SVM` 建立的是一个区分线（**Separating Line**）、高维空间中超平面（**Hyperplane**）来区分数据，需要建立的是最近的点到线或平面的距离（即 **Margin**）达到最大。 例如下面的二维数据

  ![](../img/SVM.png)

* 流程：在确认超平面之前，需要首先找到支持向量；通过找到的支持向量，就可以找到超平面来最大化的将两侧数据区分开。区分超平面（**Separating Hyperlane**）是在其他两个超平面之间，而这两个超平面会经过支持向量（**Support Vector**——即数据点）

* 优化方面： 1）从原理上来说需要数据完整分割的情况下，得到最大的 `margin`；2）对于难以完整区分的数据，可以通过软化区分的定义——即允许少量数据划分错误，另外还有一种方案是将数据 **高维化**（例如将数据使用 $x^2, x^3, \cos(x)$ 转换——核心思想是 **kernel** [技巧](../img/kernel_tric.pdf)。 $y_i=\vec{x}\cdot \vec{w}+b$ 是分类函数，其中 $\vec{w}$ 是超平面的法向量，而且分类结果是 $y_i\in\{-1, 1\}$，如果 $y_i=0$ 说明数据在决策边界上

  1. 假设“正类”的结果中， $\vec{x}\cdot\vec{w}+b=1$，而“负类” 的结果是 $\vec{x}\cdot\vec{w}+b=-1$，通过 $y_i(\vec{x}\cdot\vec{w}+b) -1 =0$，可以将正类和负类转换，这样就得到了限制条件。而之前的公式中训练集的结果，可能是不完全满足 $\hat{y}\in\{-1, 1\}$，而是通过符号（即：$sign(\vec{x}\cdot\vec{w}+b)$）来验证结果是否属于正类还是负类 [参考](https://pythonprogramming.net/support-vector-assertions-machine-learning-tutorial/?completed=/vector-basics-machine-learning-tutorial/)

  2. 到这里就是进行支持向量机的优化问题，需要得到的结果是 $\vec{w}$ 和 $b$ 两个的值。为了满足每个特征集，所以设定 $y_i(\vec{x}\cdot\vec{w}+b)\ge1$。这样可以得到测试数据集可能位于支持向量的超平面或决策边界之间，而训练数据集的结果则不可能。

  3. 最终需要得到的结果最小化 $\parallel\vec{w}\parallel$，最大化 $b$ 的结果，以此满足 $y_i(\vec{x}\cdot\vec{w}+b)\ge1$。这里需要注意⚠️满足条件的 $\vec{w}$ 的条件，并非是最小化的 $\vec{w}$ 而是最小化的模长

  4. 优化方法方面，有多种方法。方法之一是通过超平面上的支持向量得到宽度最大的结果，这里的好处是计算方式不需要使用 $b$，而表示式式 $width=(\vec{x_+}-\vec{x_\_})\cdot \frac{\vec{w}}{\parallel \vec{w}\parallel}$，示例如图：

     ![](https://pythonprogramming.net/static/images/machine-learning/support-vector-width.png)

  关于更详细的 `SVM`推导内容 内容可以参考博客 [支持向量机通俗导论（理解SVM的三层境界](https://blog.csdn.net/v_july_v/article/details/7624837)

### **SVM 这里存在理解问题尚未解决**

### 非参数类模型

以上使用的模型都是参数类模型，还有一些模型可以不通过参数进行构建：`KNN`, `Decision Trees`, `Random Forests`

#### `KNN` 模型

其模型的主要思想比较简洁，即寻找 `k` 个邻近数据点的平均值或者众数，以确认数据的标签。参考 [wikipedia 解释](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) 。对于 `KNN` 模型可以解决 **连续性数据** 和 **分类型数据**（这样可以解决分类型数据，例如猫狗分类。这可以使用众数来构建模型）。

* 流程：例如对连续型数据（房价预测）——1）获得数据，需要将各特征转换为训练数据集矩阵；2）通过相似性将数据集进行排序；3）筛选出 `k` 个数据的平均值

  这里模型的重点是定义和计算“最近”距离特征。而常用的测量方式是使用 **欧式距离**，另一种计算距离的方式是 **曼哈顿距离（Manhattan Distance）**——在特定情况下，它更有用，例如解决司机的驾驶距离问题

* 在进行 `KNN` 模型构建的过程中，需要通过 `Cross-validation` 进行选择 `k` 值来调参。需要注意的是在筛选 `k` 值的过程中，高的 `k` 值虽然可以避免过拟合，但是也会产生高偏差和低灵活性（**Inflexible**）的问题

* 实际应用中， `KNN` 不仅可以解决分类和回归问题，还可以用于解决缺失数据的问题——通过 `KNN` 来进行插入值。参考 [R语言中的缺失值处理](http://www.ituring.com.cn/article/214504) 

#### `Decision Tree` 模型

决策树的模型很像 “20 question” 的游戏，其目的就是尽可能地将数据区分的越干净越好，因此需要通过区分（**Split**）来将信息增益（**Information Gain**） 最大化。有多种方法可以对信息增益进行定量化计算，这样就可以对每一次的分割进行验证——通过数据 `features` 构建的学习规则进行数据分割，同时这样也可以高效地预测结果标签和结果。

* 数据集的无序性可以通过熵来进行计算，而评估的方式可以通过基尼系数（**Gini Index**）[Gini coefficient](https://en.wikipedia.org/wiki/Gini_coefficient)  或者交叉熵（**Cross-Entropy**）[Cross entropy](https://en.wikipedia.org/wiki/Cross_entropy) 。
* 在决策树的实际应用中，可以解决回归问题，例如房价预测——根据重要特征来确定房屋的价格，要以多大的房屋平方米，或者多少个客房来等区分方式来确定房屋价格
* 在实际参数调整方面，需要通过 `max_depth` 和 `max_leaf_nodes` 来调整

因为 `Decision Tree` 的以上特点，它在某些方面具有很强的优势：

1. 解释和理解简单，可以对 `Tree` 进行可视化
2. 可以不必进行过多的数据处理，例如其他模型需要对数据进行正太化（**Normalization**），哑变量处理（**Dummy Variables**），缺失值处理。缺失值处理还是必要的
3. 可以对数值型数据和分类行数据进行分析
4. 可以处理多结果问题
5. 进行的是白盒模型——模型中给定的条件是可见的，模型可以通过逻辑方式解释
6. 可以通过统计学检验的方式验证模型，这样对模型的可信赖度是可描述的
7. 即使咋模型假设的结果与真实模型提供的数据不一致，但表现结果可能依旧良好

同样的在其他方面需要注意缺点：

1. 模型容易过拟合，因此需要使用其他策略以避免过拟合。例如剪枝，设置也节点所需最小样本树，或者设置树的最大深度
2. 决策树模型不稳定，细微差异可能导致决策树的不同解释
3. 在优化方面和简化概念方面，决策优化问题是一个 `NP` 问题。因此，实际上决策树是基于启发式算法的问题 [启发式搜索- Wikipedia](https://zh.wikipedia.org/wiki/%E5%90%AF%E5%8F%91%E5%BC%8F%E6%90%9C%E7%B4%A2) ——例如铜鼓即成学习训练多棵决策树缓解，它通过对特征和样本有放回随机采样来生成
4. 对某些特定的概念型模型难以使用决策树生成，例如 `XOR`，奇偶或者复用器的问题
5. 数据不平衡会导致树模型偏差

#### `Random Forest` 模型—— `Decision Trees` 的融合



## 名词解释

* 特征( **Features** )：一般指数据属性。而数据可能是数值型数据（**Numerical**），也有可能是类别性数据（**Categorical**）

* 偏导（**Partial Derivative**）[偏导](https://en.wikipedia.org/wiki/Partial_derivative) 说明了参数$\beta$ 增减变化，导致总损失值的变化

* 过拟合（**Overfitting**）：学习的模型能够完美解释训练数据，但是不能对未遇见的数据泛化。这是因为模型过分的将训练数据特性，来解释现实情况

* 欠拟合（**Underfitting**）：和过拟合相反，模型的复杂性不足以捕捉到数据的趋势

* 正则化（**Regularization**）

* 超参数（**Hyperparameter**)：模型中的通用设置，用于控制调节参数的增加和下降以提高模型表现。例如正则项中的 $\lambda$

* 交叉验证（**Cross-validation**）在模型训练的过程中，从训练数据留出一部分作为验证模型的数据集，用训练模型来验证对留出的数据解释情况

* 逻辑回归函数：
  $$
  \begin{cases}
    P(y=1|x, \beta)=\frac{1}{1+e^{-\beta^Tx}} \\
    P(x=0|x,\beta)=\frac{1}{1+e^{\beta^Tx}} =1-P(y=1|x,\beta) \\
  \end{cases} \\
  假设：h_\beta(x)=g(\beta^Tx)=\frac{1}{1+e^{-\beta^Tx}}
  $$




* 融合模型（**Ensemble Model**）：使用过个模型进行组合而成的模型——`A model comprised of many models `。

## 问题解决方案

### 1. 过拟合的解决方式

一般情况下，可以通过两种方式来进行控制过拟合：

* 增大训练数据集   使用的训练数据集越大，越难以过拟合
* 使用正则化  对损失函数时使用惩罚（**penalty**），这样一方面增加了任何 `feature` 的解释效用，另一方面也可以允许更多的 `features` 被纳入训练

$Cost=\frac{\displaystyle{\sum_i^n((\beta_1x_i+\beta_0)-y_i)^2}}{\displaystyle{2*n}}+\lambda \displaystyle{\sum_{i=0}^1\beta_i^2}$ 公式中，第二部分即是正则项，它对大的参数项给予更多的解释效用（**Explanatory Power**）——它可以控制数据避免过拟合。



正则项中的参数，主要包括两块：

* $\lambda$：它是损失函数中正则项的超参数，其值越大对大的参数（参数越大，潜在越可能过拟合）惩罚越严厉



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

   线性组合（**Linear Combination**），生成空间（**Span**），线性相关（**Linear Dependence**）：

   * 线性组合的表达式 $\it{Ax}=\displaystyle{\sum_i\it{x_i}A:,i}$，可以以向量集合 ($\{v^{(1)}, ...,v^{(n)}\}$) 的方式来表达—— $\it{Ax}=\displaystyle{\sum_ic_i v^{i}}$
   * 生成空间，指原始向量的线性组合可以所有的点集。这样的向量集合即是构成了生成空间

   奇异矩阵（**Singular Matrix**）和 方阵（**Square Matirx**）：

   - 当 $\mathbb{R^{m\times{n}}}$ 中 $m=n$ 时，且所有的列是线性不相关（**Linear Independent**），那么这样的矩阵即为方阵（或者说为非奇异矩阵）
   - 当 $\mathbb{R^{m\times{n}}}$ 中 $m=n$ 时，但有的列是线性相关（**Linear Dependent**），那么这样的矩阵即为奇异矩阵

   范数（**Norms**）：包括了 $L^p​$ 范数

   * 计算方式 $ \shortparallel \bold x \shortparallel_p=(\displaystyle\sum_i\mid x_i\mid ^p)^{\frac{1}{p}}$，其中 $p\in\mathbb{R}, p\ge1$
   * 特性：1）$f(x)=0\to x=0$；2）$f(x+y)\leq f(x) + f(y)$，即三角不等式性质；3）$\forall \alpha \in \mathbb{R}, f(\alpha x)=|\alpha|f(x)$
   * 当 $p=2$ 时，即计算的是欧式范数（**Euclidean Norm**）。它在机器学习中的实际应用，因为它针对邻近 **Origin** 的元素增长缓慢，  难以区分各元素是真为 $0$ 还是值很小但并不为 $0$。
   * 当 $p=1$，即 $\it{L^1}$ 范数，$\shortparallel{x}\shortparallel_{1}=\displaystyle{\sum_i|x_i|}$。它的实际应用是解决了欧式范数难以区分 $0$ 和值很小的情况
   * 当 $p=\infin$， 计算的是 $L^{\infin}$ 表示的是 **Max Norm**，$\shortparallel{x}\shortparallel_{\infin}=\displaystyle{\max_i}|x_i|$
   * 在深度学习中，常用的范数是弗罗贝尼乌斯范数（**Frobenius norm**）或希尔伯特-施密特范数（**Hilbert–Schmidt norm**），它是模拟了向量的欧式范数计算方式，$\parallel{A}\parallel_F=\sqrt{\displaystyle{\sum_{i,j}A_{i,j}^2}}$，

   特殊类型的矩阵和向量：

   * 对角矩阵（**Diagonal Matrix**）：在主对角线上具有非零值，而非对角线上具有零值。数学表表达式——$\forall i\ne j, \it{D_{i,j}}=0 \iff \it{D}\ is\ diagonal\ matrix$。对角线矩阵的向量表示，$diag(v)$ 表示向量 $v$ 的每个元素可以表达对角方阵中的值，因此下面的这个表达式结果是相同的 $diag(v)x=v \bigodot x$

   * 对称矩阵（**Symmetric Matrix**）：转置矩阵和原矩阵相同的一类矩阵，其表达式是：$\it{A}=\it{A^{T}}$。在实际表现为，两个参数的函数不依赖参数的顺序，例如矩阵的距离测量——给定的 $i$ 到 $j$ 的距离计算与顺序无关， $\it{A_{i,j}}=\it{A_{j,i}}$，因为距离函数是对称的

   * 单位向量（**Unit Vector**）：模为单位值的向量，$\parallel x \parallel_2 = 1$

   * 向量正交（**Orthogonal**）如果向量之间存在 $\it{x^Ty}={0}$ 的关系，那么两个向量互相存在正交关系。如果两个向量模长为非零，即说明两个向量的 **夹角** 为 $90^o$。如果向量不仅是正交而且是具有单位模长（ unit norm），那么这样的向量具有标准正交性（**Orthonormality**）

   * 正交矩阵（**Orthogonal Matrix**）方阵的行与行之间和列与列之间是相互正交， $\it{A^TA}=\it{AA^T}=\it{I}$，而这也说明了 $A^{-1}=A^T$——因此，正交矩阵的逆计算很方便

   * 特征分解（**Eigendecomposition**）

     在数学对象中，通过将对象分解为组成“部件”，或者找到具有普遍代表特性，并且不是因为人为选择的原因所具有的某些特性。例如整数可以被分解为质数，这样不因为书写进制差异，都能表示出整数的特性（例如整除）$12=2 \times 2 \times 3$ 式子表示了 12 可以被 3 整除 而不能被 5 整除

     同样的在矩阵中，使用同样的方式从矩阵中找到数据方式表达。这种方式即是特征分解，矩阵被分解为特征向量（**Eigenvectors**）和特征值（**Eigenvalues**），其表达式是 $\it{Av}=\it{\lambda v}$， 非零向量 $v$ 乘以 $\it{A}$ 等于标量 $\lambda$ （即是特征值）与向量 $v$ （即特征向量，可以用右特征向量称，这是因为存在左特征向量 $v^TA=\lambda v^T$ 。常用右特征向量来表示特征向量）相乘

     假设矩阵 $A$ 具有 $n$ 个线性不相关的特征向量 ${v^{(1)}, ..., v^{(n)}}$ 以及对应的特征值 $\lambda_1, ..., \lambda_n$，通过将特征转换为矩阵形式 $V={v^{(1)}, ..., v^{(n)}}$ 以及 $\rm{\lambda}=\lambda_1, ..., \lambda_n$ ，此时的矩阵的特征分解为：

     $$A=\it{V}diag(\lambda)\it{V^{-1}}$$

     ![ml_eigendecomposition](../img/ml_eigendecomposition.png)

     * 正定矩阵（**Positive Definite**）特征值都是正数的矩阵，它保证了 $x^TAx=0 \Rightarrow x=0$
     * 半正定矩阵（**Positive Semidefinite**）特征值是正数或者零值的矩阵，它保证了 $\forall x, x^TAx \ge 0$
     * 负定矩阵（**Negative Definite**）特征值全是负数的矩阵
     * 半负定矩阵（**Negative Semi definite**） 特征值是负数或者零值的矩阵

   * 奇异值分解（**Singular Value Decomposition**）：

     奇异值分解提供了另一种方法将矩阵分为奇异向量（**Singular Vectors**）和奇异值（**Singular Values**）。它提供了可以特征分解解析得到的相同信息，但是它更具有实用性。每一个矩阵均可以进行奇异值分解，但是却不一定有特征值分解——例如非方阵矩阵。其中奇异值对应的表达式为 $A=UDV^{-1}$，假设矩阵 $A \in \mathbb R^{m\times n}$，$U \in \mathbb R^{m \times m}$， $D\in \mathbb R^{m\times n}$，$V\in \mathbb R^{n \times n}$，其中 $V$ 和 $U$ 均是正交矩阵， $D$ 是一个对角矩阵（可以不一定为方阵）。其中 $D$ 的对角上的元素值为矩阵 $A$ 的奇异值，$U$ 是一个左奇异向量（可以通过特征值分解来做解释，即特征向量 $AA^T$），$V$ 为右奇异向量（可以通过特征值分解来做解释， 即特征向量 $A^TA$)。

   * 摩尔-彭若斯广义逆（**Moore-Penrose Pseudoinverse**）

     对非方阵的逆矩阵此前尚未定义，因为之前的定义中是通过得到矩阵的左逆来得到结果 $Ax=y , \Rightarrow x=By$——它是依赖矩阵 $A$ 的唯一映射产生 $B$ 来得到结果，当 $m\neq n$ 时是难以通过该方式来得到结果。

     广义逆克服了该问题，表达式为 $A^+=\displaystyle{\lim_{\alpha\searrow 0}}(A^TA+\alpha I)^{-1}A^T$。在实际应用层面上，并非使用该表达式而是使用了 $A^+ = VD^+U^T$。

     * 针对列数大于行数的问题，通过广义逆提供的其中可能解来解决线性等式。特别是提供的可能解 $x=A^+y$ 的最小欧式模长 $\parallel x \parallel_2$ 的值是最可能解
     * 针对行数大于列数的问题，一般情况下是没法求解。但是可以使用广义逆的方式 $Ax$ 趋近于 $y$ 的欧式距离（$\parallel Ax-y \parallel_2$）来检验求得 $x$

   * 迹运算（**Trace Operator**）：计算的是矩阵对角线上元素的和 $Tr(A) = \displaystyle{\sum_i A_{i,i}}$。

3. [An Introduction to Gradient Descent and Linear Regression](https://spin.atomicobject.com/2014/06/24/gradient-descent-linear-regression/)

   从示例演示以及数学解释的角度，来说明了线性回归中的梯度下降。其中演示的代码地址[GradientDescentExample](https://github.com/mattnedrich/GradientDescentExample)

4. [Understanding gradient descent - Eli Bendersky's website](https://eli.thegreenplace.net/2016/understanding-gradient-descent/)

   从数学的角度，严谨地解释了梯度下降

5. [16. Learning: Support Vector Machines - YouTube](https://www.youtube.com/watch?v=_PwhiWxHK8o) 

   讲解了 `SVM` 的相关信息：

   * 注意，`margin` 的最大值指的是两边边界之间达到最大
   * 使用拉格朗日乘数来解决优化问题

6. [overview of the supervised learning process](https://github.com/rasbt/pattern_classification/blob/master/machine_learning/supervised_intro/introduction_to_supervised_machine_learning.md) 

   机器学习中监督式学习的一般流程

7. [ref_convex_optimization](ref_convex_optimization.md) 凸优化参考笔记
