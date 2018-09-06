---
layout: post
title: Python的random.py
author: zzxun
date: 2018-07-26 12:15:59
categories:
- 编程
tags:
- 随机数
- Python
- random
---

* 一时兴起，看了一下python中random的源代码。*
# random.py注释说明 (这是random开头的注释，主要介绍该随机数发生器的功能，支持的随机类型)#
  * 整数：*
  1. 支持特定范围内的整数生成
  * 系列： *
  1. 随机获取序列中的元素
  2. 随机获取系列实例
  3. 获取加权后的随机实例
  4. 产生随机排列
  * 对于实线上的分布：*
  1. 均匀分布
  2. 三角分布
  3. 正态（高斯）分布
  4. 对数正态分布
  5. 负指数分布
  6. gamma分布
  7. beta分布
  8. 柏拉图分布
  9. 威布尔分布
  对于底层的Mersenne Twister核心生成器的一些说明：

  * 该生成器的周期是 2**19937-1
  * 它是现存的最广泛受测试过的生成器之一
  * random()方法由C语言实现，该函数在单个Python步骤中执行，所以能保证线程安全（补充线程安全的含义是：函数在多线程环境中背调用时，能够正确的处理多个线程之间的共享变量，使得程序功能正确完成。）


我们调用的random中的函数为
1. random.random()  #产生0~1之间的随机浮点数
2. random.randint(start,stop)  #产生包含端点的start~stop之间随机整数
3. random.randrange(start,stop,step)  #产生start~stop之间，步长为step的列表中的一个随机数。
4. random.choice(list)  #获取list中的一个随机元素
5. random.shuffle(list) #洗牌，打乱list中的元素顺序
6. random.sample(list,len)  #随机获取list中长度为len的一个系列

{% asset_img sample.png %}