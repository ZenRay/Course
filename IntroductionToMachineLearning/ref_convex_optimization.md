**目录**

[TOC]

[斯坦福 凸优化 Convex Optimization I&II (Stanford)_哔哩哔哩 (゜-゜)つロ 干杯~-bilibili](https://www.bilibili.com/video/av21419893/) 

数学优化问题的一般形式：
$$
\begin{align}
  minimize\ \ \ \ f_0(x) \\
  subject\ to \ \ \ \ f_i(x) \le b_i\\
\end{align}\\
 i=1, ..., m
$$
向量 $x=(x_1,...,x_n)$ 为问题的**优化变量**，$f_0:R^n \to R$ 函数为**目标函数（Objective Function）**；$f_i:R^n\to R, i=1,...m$ 函数为**约束函数（Inequality / Constraint function）**，其中常数 $b_1,...,b_m$ 称为约束上限或者约束边界。如果存在 $x^\star$ 是所有满足约束向量中对应的目标函数值最小，也就是说对满意任意约束的向量，如果有 $f_0(x) \ge f_0(x^\star)$，那么 $x^\star$ 为最优解或者解。

线性规划的条件：$f_i(\alpha x+\beta y)=\alpha f_i(x)+\beta f_i(y)$ ，其中 $x,y \in R^n, and\ \alpha, \beta \in R$。若不满足以上线性规划条件的优化问题，则为非线性规划。凸优化问题目标函数和约束函数都是凸函数，满足这样的等式 $\forall x,y \in R^n, \alpha, \beta \in R,\ and\ \alpha+\beta=1, \alpha\ge0,\beta\ge0\ \rightarrow f_i(\alpha x+\beta y)\le \alpha f_i(x)+\beta f_i(y)$。因此线性规划可以被纳入凸优化中