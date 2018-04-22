---
layout: post
title: python冒泡排序和快速排序
author: zzxun
date: 2018-04-23 02:15:25
categories:
tags:
- Python
- 算法相关
---

把一些最常用的算法python代码放在这里，可以从python代码中很快回忆起实现的思路和细节，比文字来的快。


## 首先是冒泡排序
> 函数输入:待排序的列表
> 函数返回值：从小到大排序后的列表

~~~python
def B_sort(temp):
    arrlist = temp[:]
    length = len(arrlist)
    exchang = length - 1
    while exchang != 0:
        bound = exchang
        exchang = 0
        for i in range(bound):
            if arrlist[i] > arrlist[i+1]:
                tem = arrlist[i+1]
                arrlist[i+1] = arrlist[i]
                arrlist[i] = tem
                exchang = i
     return arrlist
~~~

依次从系列中拿一个元素和后面的所有元素做比较，只要比其大就交换当前位置和被比较元素的位置，直到所有元素都比其右边元素小，就是不能再交换位置。

## 快速排序
> 函数输入:待排序的列表
> 函数返回值：排序后的列表

~~~python
def Q_sort(temp_list):
    if len(temp_list) < 2:
        return temp_list
    else:
        mid = temp_list[0]
        greater = [tem for tem in temp_list[1:] if tem > mid]
        less = [tem for tem in temp_list[1:] if tem <= mid]
    return Q_sort(less) + [mid] + Q_sort(greater)
~~~

基本思路，随机挑一个，比其大的放右边，比其小的放左边，然后对左边的系列和右边的系列分别重复此操作直至子系列中少于三个元素。所有子序列合起来就是总系列的排序。
