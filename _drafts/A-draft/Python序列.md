---
layout: post
title: Python序列
author: zzxun
date: 2018-09-28 10:18:59
categories:
- 编程
tags:
- Python
- Python系列
---

# 序列 #

>数学上，序列是被排成一列的对象（或事件）；这样，每个元素不是在其他元素之前，就是在其他元素之后。 这里，元素之间的顺序非常重要。

** 序列在编程中是务必会被用到的一种数据容器，当我们发现一个一个创造变量已经不够使用了，这个时候需要批量的创造变量，而变量需要储存变量的容器，于是就有了序列，附加了各种特征的序列就成了各种基本数据结构。其实一个变量也是系列，计算机底层表示一个变量同样是用0或1 (bit) 有序排列在固定长度的存储区间里，ASCII表就定义了表示变量的bit序列。 **

# 序列分类 #

在Python中序列有以下两种分类方式：

## 按照存放数据的方式 ##

+ 容器系列
  > list、tuple、collections.deque  可以存放不同类型的数据（的引用）
+ 扁平序列
  > str、bytes、bytearray、memoryview、array.array 只可以存放一种类型

## 按照能否被修改来分类 ##

+ 可变序列
  > list、bytearray、array.array、collections.deque和memoryview
+ 不可变序列
  > tuple、str和bytes

# 列表推导式 #

# 生成器表达式 #
