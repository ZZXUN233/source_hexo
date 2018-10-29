---
layout: post
title: leetCode最“简单”一题
author: zzxun
date: 2018-10-05 15:51:13
categories:
- 编程
tags:
- leetcode第一题
- 最简单的题
---

# 题目 #

Given an array of integers, return **indices** of the two numbers such that they add up to a specific target.

You may assume that each input would have **exactly** one solution, and you may not use the same element twice.

**Example:**

Given nums = [2, 7, 11, 15], target = 9,

Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].

<!--more-->

# 求解 #

一般思路下的伪码：

~~~
TWOSUM(nums,target)
for i=0 to nums.length
    for j = i+1 to nums.length
        if nums[j] == target-nums[i]
            return (i,j)
~~~

Python的代码总是很接近伪码描述，这就是它适合入门的一个原因吧！

~~~python
class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        for i in range(len(nums)):
            for j in range(i+1,len(nums)):
                if nums[j] == target - nums[i]:
                    return [i,j]
~~~

## 提交结果 ##

{% asset_img leetcode1.png %}
我们很可能丢下一个如下版本的代码，提交成功就离开了，那么这个简单的题就永远简单了！

## 换一种思路 ##

这个简单的算法还可以再优化吗？简单计算一下这个时间复杂度：
从第一个元素开始向后面 $n-1$ 个元素中找是否有满足第 $i$ 个元素和第 $j$ 个元素之和为 $target$ 的，而这里找后面的元素就涉及到遍历多次 $nums$ 中第$i$个元素之后的元素。所以贼浪费时间！那还有什么好的办法吗？换个思路：

+ 这次不去找后面的元素，而是找前面遍历过的元素
+ 前面每遍历过的一个元素就记录这个元素的位置和值
+ 现在的问题就成了怎么记住前面的元素和怎么快速拿到这个元素的问题了

## hash表来帮忙 ##

Python的字典就是hash表，是一种以键值对存放数据的数据结构，对于数组可以以$A[i]$整数$i$作为下表来取第$i$个元素，对于字典就可以用键$key$来取这个字典中$dic[key]$的这个元素，这里的$key$不再局限在整数中了，可以试试支持哪些数据类型:

~~~python
>>> dic={}
>>> dic[1]=1
>>> dic[1.1]=1.1
>>> dic['a']='a'
>>> dic[1+3j]=1+3j
>>> type(1+3j)
<class 'complex'>
>>> dic[(1,2,3)]=(1,2,3)
>>> dic[[1,2,3]]=[1,2,3]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
>>> dic[{1,2,3}]={1,2,3}
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'set'
>>> for key in dic.keys():
...     print(type(key))
...
<class 'int'>
<class 'complex'>
<class 'str'>
<class 'tuple'>
<class 'float'>
~~~

所以字典的键目前支持的常用数据类型有这些：```int,comples,float,str,tuple```，用Python的话说，这就是可哈希 (hashable) 的数据类型， (unhashable) 对应的描述就是 (mutable): ```List ,Carray , sets ,Dictionary ,Collections.deque```
** 此处就需要hash表来救场了，利用hash表记住扫描过的元素，下一次使用就直接寻找这个元素对应的键在hash表中有没有记录，有记录就可以直接以$O(1)$的时间复杂度获取到这个元素。 **
{% asset_img dic.png %} 图片来源： [Python基本数据结构时间复杂度](https://wiki.python.org/moin/TimeComplexity)

## 优化之后 ##

~~~python
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        scanned = dict()                #用于存放扫描的num
        for i in range(len(nums)):
            needed = target - nums[i]
            if needed in scanned:       # 判断字典中是否已经记录了这个键
                return [scanned[needed], i]
            else:
                scanned[nums[i]] = i    #没有存在则录入本次扫描到的数，以对应值作为key，以对应序作为值
~~~

{% asset_img letcode3.png %}

这是高手留在评论区中的C语言实现，击败100%。

~~~C
/**
 * C solution in O(n) time.
 */
#define SIZE 50000

int hash(int key) {
    int r = key % SIZE;
    return r < 0 ? r + SIZE : r;
}

void insert(int *keys, int *values, int key, int value) {
    int index = hash(key);
    while (values[index]) {
        index++;
        index %= SIZE;
    }
    keys[index] = key;
    values[index] = value;
}

int search(int *keys, int *values, int key) {
    int index = hash(key);
    while (values[index]) {
        if (keys[index] == key) {
            return values[index];
        }
        index++;
        index %= SIZE;
    }
    return 0;
}

int* twoSum(int* nums, int numsSize, int target) {
    int keys[SIZE];
    int values[SIZE] = {0};
    for (int i = 0; i < numsSize; i++) {
        int complements = target - nums[i];
        int value = search(keys, values, complements);
        if (value) {
            int *indices = (int *) malloc(sizeof(int) * 2);
            indices[0] = value - 1;
            indices[1] = i;
            return indices;
        }
        insert(keys, values, nums[i], i + 1);
    }
    return NULL;
}
~~~

结果：
{% asset_img letcode4.png %}

** 一些事物远没有想的那么简单 **