[toc]

## Algorithmic Toolbox
内容是针对 Coursera 中专项课程 [Data Structures and Algorithms ](https://www.coursera.org/specializations/data-structures-algorithms) 的第一个课程。

### 1 算法设计流程
1. 理解问题
2. 设计一个算法
3. 执行算法
4. 测试和 debug 算法

	>测试的过程主要需要从一下几个方面考虑：手动测试、溢出测试、大值测试以及压力测试；结果需要在限定的硬件设备上，从运行时间和运行结果两个方面考虑
	
### 2 算法
算法的作用，一方面是通过合适的方式解决问题，另一方面是优化算法提高问题解决效率。从以下算法运行比价结果来看，考虑算法的优化一方面要考虑解决的问题思路，另一方面需要从数据的结构考虑。

* 递归解决斐波那契数列的方法

	> 递归的方式解决斐波那契数列，是通过不断去将数值变小，并最终从内向结算。这样导致重复计算，计算开销变大
	
* 数组解决斐波那契数列方法

	>提供了一个线性数据表，减少了重复计算的消耗
	
	```{blueprint}
	create an array F[0...n]
	F[0] <- 0
	F[1] <- 1
	
	for i from 2 to n:
		F[i] <- F[i - 1] + F[i - 2]
	
	return F[n]
	```	
* 直接循环方式求解最大公因数（ Greatest Common Divisor ）

	> GCD的应用，不仅是在寻找质数、除数，而且对加密方面也有应用
	
	```{blueprint}
	# 简单方式
	function NaiveGCD(a, b)
	best <- 0
	for d from 1 to a + b:
		if a % d and b / d:
			best <- d
	return best
	```
* 优化方式求解最大公因数

	> GCD 优化是利用了数学公里——假设 `a` 除以 `b` 具有余数 `a'`，那么村杂 ${GCD(a, b)=GCD(a', b)}=GCD(b, a')$。具体解释见 [The Euclidean Algorithm (article) | Khan Academy](https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/the-euclidean-algorithm)。该方法的步骤数降为 `log(ab)`。
	
	```{blueprint}
	# Euclidean 优化方式
	function EuclidGCD(a, b)
	if b = 0:
		return a
	a' <- the remainder when a is divided by b
	
	return EuclidGCD(b, a') # 这里 b 的位置需要交换
	```
	
### 3 算法评估
在机器运行代码的过程中，所有的语言都需要被编码为机器语言才能被运行。因此在机器层面来说，算法运行的评估需要考虑存储开销、地址查询开销、算法运行开销，这样导致实际对算法进行评估过于复杂（而且在实际过程中机器的性能对运行开销也有影响）。但是在实际进行算法评估中，对这类底层架构不用细化考虑，不用对运行时间进行详细评估。

计算机算法运行架构图：

![](img/system_architecture.png)

因此在实际进行算法评估的过程中，忽略了机器运行时候的常数，而是采用输入的规模变化对运行时间影响来评估算法。文档说明见[Asymptotic notation (article) | Algorithms | Khan Academy](https://www.khanacademy.org/computing/computer-science/algorithms/asymptotic-notation/a/asymptotic-notation)

* Big O 概念

	>定义：f(n) = O(g(n))(f is Big-O of g), if there exist constants N and c so that for all n > N, f(n) <= c * g(n).
	
	>定义说明了 f 存在一个上界，由常数和函数 g 相乘。因为 f 函数的增量在一定情况下是由函数中的最大变化量决定的（利用渐近线分析——最终在达到某个输入量的时候，会趋于稳定），所有通过这样评估方式即采用 Big O 来评估算法。
	>它的优势在于通过输入量来决定算法的运行时间，可以大概评估出在达到多大的输入范围事，算法可能“无法”解决问题，可以比较不同算法之间的运行效率
	
	需要注意在使用 Big O 来评估算法的时候，是忽略了很多重要信息例如函数中的常数 N 和 c；而且 Big O 仅仅是渐进方式评估算法。下图中是对优化的斐波那契数列算法评估的实际应用举例：
	
	![](img/big_o_practice.png)
	
* 算法的其他评估概念—— Big Theta 和 Big Omega

![](img/other_runtime_notation.png)

算法练习：

1. ${n^2=O(n^3)}$: ${n^a}$ grows slower than ${n^b}$ for constants ${a<b}$
2. ${n=O(\sqrt{n})}$: ${\sqrt{n}=n^{1/2}}$ grows slower than ${n=n^1}$ as ${1/2<1}$
3. ${5^{log_2n}\neq{O(n^2)}}$: Recall that ${a^{log_bc}=c^{log_ba}}$ so ${5^{log_2n}=n^{log_25}}$. This grows faster than ${n^2}$ since ${log_25=2.321…>2}$
4. ${2^n=O(2^{n+1})}$ : ${2^{n+1}=2*2n}$, that is, ${2^n}$ and ${2^{n+1}}$ have the same growth rate and hence ${2^n=Θ(2^{n+1})}$

### 4 算法的实际应用

#### 4.1 贪心算法

贪心算法的流程，在不断地迭代过程中更新取值范围和结果——这样通过不断地将大问题变为小的子问题，以达到最后求解的方式。首先需要选择一个合适的贪婪抉择，证明其是一个合适的选择，将问题减少一个子问题，解决这个子问题。需要注意这是一个不断迭代的过程，以达到最终解决问题的目的。如下为获取最大值的数字：
	
```
# 在 3,9,5,9,7,1 几个数字中排序获得最大数字
LargestNumber(3,9,5,9,7,1)：
	“9” + LargestNumber(3,5,9,7,1)
```
另一例子是在 A、B 之间以最少次数加油的策略达到终点，${x_n}$ 表示有加油站的距离（实际应用中可以当作数组）：
![](img/car_filling.png)
	
算法时间评估：
![](img/car_filing_runingtime.png)

对贪心算法进行总结，该算法主要的步骤如下：

1. safe move
2. prove safe
3. solve subproblem
4. estimate running time

对贪心算法，优化排序策略可以从以下几个方面进行考虑：

1. 输入对象是否可以排序
2. 排序方式是否可以更快速筛选
3. 贪心算法运行是否更快速

##### 4.1.1 分组事件

分群算法的例子，是对一群儿童进行分组，其中每组组内的儿童年龄最大相差不超过一年，对这样的条件内可以分出最少的群组数量。算法逻辑如下：
	
```
# C 为整体数量
MinGroup(C)：
	m <- len(C)
	for each partition into groups
	C = G1 U G2 U G3 U ... Gk:	# C 被分为 k 个群组
		good <- true	# 设置一个检验逻辑值，用于判断每次迭代的结果是否可行
		
		for i from 1 to k:
			if max(Gi) - min(Gi) > 1:
				good <- false
		
		if good:
			m <- min(m, k)	# 判断得到的群组数量和 C 的总体数量进行比较，获取最小值
	
```
	
因为以上的简单算法，评估的运行时间 ${\Omega}$ 值为 ${2^n}$，当运行的数据规模越大的时候，耗费时间太大。该分群算法可以优化，思路是因为分群是限制了取值的范围了。初始阶段可以先通过建立一个合适的取值范围，不断优化最左端值和最小值来构建合适的范围——以此保证最左端数据点在分群内；其后需要不断迭代，找出之后的组。具体解释如下：
![](img/group_optimize.png)
经过以上方式来进行新的算法更新后，算法的运行时间为 ${O}$ 的值为 ${nlog(n)}$，注意该算法需要一个排序过程以获得最左端值。算法说明如下：
	
```
# 该算法是取得取值范围， R 是一个范围集合
PointsCoverSorted(X1,...,Xn):
	R <- {}, i <- 1
	while i<= N:
		[l, r] <- [Xi, Xi + 1]
		R <- R U {[l, r]}	# 将 [l, r] 以集合的并集更新到 R 中
		i <- i + 1
		while i <= n and Xi <= r:
			i <- i + 1
	return R
```
	
##### 4.1.2 部分背包事件——Fractional Knapsack
	
事件是为了解决长途旅行中，装入包裹中的物品如何保障最大能量，以能够行走最大的旅程。该事件进行分析，结构如下：

![](img/fractional_knapsack.png)

对以上说明，每样食物重量和每样食物能量值，包裹可装最大容量作为输入；获得最大包装容量的情况下能获得的最大能量值作为输出。**注意⚠️：**在实际应用过程中需要注意到，计算应该用到的是每项物品的单位值而非整体值，以下的例子中应该考虑最大单位值优先以获取最大能量值，最大值应该是 42：

![](img/fractional_knapsack_example.png)

Knapsack 算法伪代码如下：

![](img/knapsack_algorithm.png)

对于以上代码，其算法运行时间 ${O}$ 为 ${n^2}$。从其中可以看出，每轮 loop 都需要对筛选出最大的 ${\frac{v_i}{w_i}}$，这样增大了算法开销。可以通过优先对 w 通过最大单位价值进行排序，在装包。优化伪代码如下：

![](img/knapsack_better_algorithm.png)

更新后的伪代码运行时间开销  ${O}$ 为 ${n\ logn}$。
