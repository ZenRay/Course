**目录**

[TOC]

## 深度学习——`Deep Learning`

深度学习对于解决复杂数据问题——大量数据，大量特征等，依据通用函数拟合器（**universal function approximators**），使用隐藏层（**Hidden Layer**）解决复杂问题并能得到任何可能的函数。数学层次上来说，各层是通过激活函数（**Activation Functions**）来将激活值和权重的矩阵进行非线性转换；同时使用了梯度下降来训练参数









## 参考

1. [Neural networks and deep learning](http://neuralnetworksanddeeplearning.com/chap4.html) 

   解释了为什么神经网络可以解决任何复杂的问题，习得可能的函数。也就是说不论什么样的目标函数，都有可能得到一个结果或者近似的可能的结果。准确来讲，通用理论（**Universality Theorem**）是使用具有隐藏层的神经网络来得到近似的任何可能的连续函数并达到期待的精确度。在可视化 [create_step_function](../img/create_step_function.mp4) 中演示了单个隐藏层中权重和 $bias$ 值不同变化的对隐藏神经元的结果影响

2. [deeplearningbook](http://www.deeplearningbook.org/contents/intro.html)

   系统介绍了深度学习的相关信息

3. [Deep Reinforcement Learning: Pong from Pixels](http://karpathy.github.io/2016/05/31/rl/) 



### 其他信息

目前常用的 package 为 `Tensorflow`, `Caffe`, `Torch`, `Theano`。此外卷积神经网络（**Convolutional Neural Networks(CNNs)**）主要针对图像识别，递归神经网络（**Recurrent Neural Networks(RNNs)**）可以用于解决“记忆” 问题和语言问题——例如使用 LSTMs 来解决语言问题，参考[Understanding LSTM Networks -- colah's blog](http://colah.github.io/posts/2015-08-Understanding-LSTMs/) 。另外还有一个是增强式学习，针对的是最大化奖励问题——例如 CS，自动驾驶，股票交易等问题



