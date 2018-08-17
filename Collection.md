**目录**

[TOC]

# 说明
针对已经学习的课程，整理出的相关笔记、课程中的代码以及其他练习代码


### Andreas Mueller: Word Cloud Generator in Python——文字云
该网站提供了文字云的示例，超赞👍。下面分别为网站和 `GitHub` 地址:

1. [word clouds in Python — wordcloud 1.3 documentation](https://amueller.github.io/word_cloud/)

2. [GitHub - amueller/word_cloud: A little word cloud generator in Python](https://github.com/amueller/word_cloud)

### 字符串编码的技术细节
* [What Every Programmer Absolutely, Positively Needs to Know About Encodings and Character Sets to Work With Text](http://kunststube.net/encoding/)

>在许多不同的位序列中，可以对任何字符进行编码，任何特定位序列可以表示许多不同的字符，但这取决于使用哪种编码来读取或写入这些字符。原因是不同的编码对每个字符使用不同的位数，以及不同的值来表示不同的字符。

### Seaborn 绘图指导

* [Python数据处理学习笔记 - seaborn统计数据可视化篇 — Corkine's BlOG](http://blog.mazhangjing.com/2018/03/29/learn_seaborn/)

* [seaborn: statistical data visualization — seaborn 0.8.1 documentation](https://seaborn.pydata.org/)

该文档基本上列出了常用的 `seaborn` 方式，可以作为参考（⚠️该 `blog` 值得关注）。但是解决问题的最好方式，还是需要查看官方文档 

### 机器学习中逻辑回归的知识流程

[Guide to an in-depth understanding of logistic regression](https://www.dataschool.io/guide-to-logistic-regression/) 

链接中给出了很多丰富的资源，不仅包括逻辑回归的相关知识，而且还从实践以及理论文档（[paper by Andrew Ng](http://ai.stanford.edu/~ang/papers/nips01-discriminativegenerative.pdf) ——比较了逻辑回归和朴素贝叶斯性能）

### 机器学习决策树

[A Complete Tutorial on Tree Based Modeling from Scratch (in R & Python)](https://www.analyticsvidhya.com/blog/2016/04/complete-tutorial-tree-based-modeling-scratch-in-python/#thirteen) 

对于理解决策树模型构建以及模型调试的依据，讲解了其他多种多种树模型

### 理解 Q-Q plots

[Understanding Q-Q Plots | University of Virginia Library Research Data Services + Sciences](https://data.library.virginia.edu/understanding-q-q-plots/)

理解这个图非常重要，是分析数据分布情况的图，另外还有一种检验方法，可以用于检验数据是否是正太分布[Kolmogorov-Smirnov 检验](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test) 

### 机器学习中数据预处理

[Is it a good practice to always scale/normalize data for machine learning? - Cross Validated](https://stats.stackexchange.com/questions/189652/is-it-a-good-practice-to-always-scale-normalize-data-for-machine-learning) 

### 自助法与最佳统计量

下列是发现 "最佳统计量" 估计技巧最常见的三种方式，之前曾经提到过：

- [最大似然估计](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation)
- [矩估计方法](https://onlinecourses.science.psu.edu/stat414/node/193)
- [贝叶斯估计](https://en.wikipedia.org/wiki/Bayes_estimator)

虽然这些超出了这个课程覆盖的范围，但是数据学家可以很好地理解这些技巧，他们需要理解如何估计一些除了平均数或方差以外不常见的数值。使用其中一种方法"最佳估计"，具有必要性。

### 博客参考——包括了各个方面的内容

[Chris Albon](https://chrisalbon.com/#articles)