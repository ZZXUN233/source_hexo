---
layout: post
title: Python中一些知识点1.0
author: zzxun
date: 2018-08-09 15:17:43
categories:
- 编程
tags:
- python知识点
---
## 列表 ##
1. 列表元素多样化
~~~python
lis = [1,2,"a",'c',True,[1,2],(233,233),{1:"a","2":"b"}]
lis[1] = lis  #这个列表已经废了
~~~
虽然列表一般不这么混乱的用，但是这很python（虽然其它语言可能也有，但是这里我只做关于Python的记录）
2. 于是有了多维数组的表示
~~~python
lis1 = [1]
lis2 = [lis1,lis1]
lis3 = [lis2,lis2]
lis4 = [lis3,lis3]

# 这样不够直观的话，可以换下下面这样
>>> import numpy as np
>>> lis1 = np.array([1])
>>> lis2 = np.array([lis1,lis1])
>>> lis3 = np.array([lis2,lis2])
>>> lis4 = np.array([lis3,lis3])
>>> lis = [lis1,lis2,lis3,lis4]
>>> for li in lis:
	print(li.shape)

(1,)
(2, 1)
(2, 2, 1)
(2, 2, 2, 1)
~~~

于是关于维度问题，有了下面的图(俄罗斯套娃)：
{% asset_img TaoWa.jpg %}
** 数组的维度，由其下标支持访问元素时的最大方括号数决定！a[1][1][1]元素存在的话，说明它至少是3维的。（同样只说python，不说其它支持此功能的其它语言）**

3. 关于切片
~~~python
>>> lis
[1, 2, 3, 4, 5, 6]
>>> lis[-100:100:]
[1, 2, 3, 4, 5, 6]
>>> lis[::-1]
[6, 5, 4, 3, 2, 1]
>>> lis= [str,list,tuple]
>>> lis
[<class 'str'>, <class 'list'>, <class 'tuple'>]
# 上面三个都是序列
~~~
没有什么好说的，记住lis[a:b:c]中，(a,b,c)可以为任意整数（具体能否截到东西就看缘分了O_O）,a,b,c分别表示起始位置，结束位置，取元素的步距，记住正向从0开始到len(lis)结束，逆向从-1开始表示最后一个元素到结束。** 特别注意，无论怎么切片得到的都是列表 **
 
4. 生成器
~~~python
>>> lis=[i for i in range(10)]
>>> lis
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> 
~~~
