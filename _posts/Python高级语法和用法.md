---
layout: post
title: Python高级语法和用法2.0
author: zzxun
date: 2018-08-12 14:58:44
categories:
- 编程
tags:
- Python
- 闭包
- 函数式编程的皮毛
- 高阶函数(map,reduce,filter)
---

## 闭包 ##
> 闭包是个很高大上的定义。闭包是函数式编程的一种实现手段。
> 1. 闭包 = 函数+环境变量（这里的环境变量就能充当一个全局变量使用）
> 2. 闭包的使用可以减少全局变量的使用，从而怎加函数的封闭性
> 3. 闭包不是非用不可，Python支持闭包，但是闭包的使用不合理容易造成内存泄漏
> 4. 在Python中使用闭包时需要明确知道变量的各种作用域，同时理解**global**和**nolocal**的用法

应用小场景：旅行者，一个旅行者每天接着前一天的路程上走一定的路程，编程来表示旅行者每次行进后走过的总路程。
1. 非函数式编程，使用全局变量来记录总路程，每次调用函数就操作全局变量
~~~python 
pos = 0     #起点

def move(length):
    global pos      #使用全局变量
    pos += length
    return pos

print(move(2))
print(move(3))
print(move(7))
print(pos)
~~~
>运行结果：
~~~bash
2
5
12
12  # pos用作全局变量，值被改变了
~~~
2. 函数式编程，使用闭包，将路程当作环境变量，移动的操作当作函数。
~~~python
pos = 0

def start(pos):
    def move(length):
        nolocal pos
        new_pos = pos + length
        pos = new_pos
        return pos
    return move

tourist = start(pos)    # 之前的pos被当作参数使用，这样做的好处是pos的值不会被改变
print(tourist(2))
print(tourist(3))
print(tourist(7))
print(pos)
~~~
<!--more-->
>运行结果：
~~~bash
2
5
12
0   #可以看到非函数式编程下，pos被作为全局变量，值被改变了
~~~
也可以像这样写：
~~~python 
def start():
    pos = 0
    def move(length):
        nonlocal pos
        new_pos = pos + length
        pos = new_pos
        return pos
    return move

tourist = start()    # 这次就看不到函数外有任何变量来记录总路程
print(tourist(2))
print(tourist(3))
print(tourist(7))
~~~
>运行结果：
~~~bash
2
5
12
~~~
这次pos就作为局部变量在函数内部。编程中要尽量减少全局变量的使用，避免多处修改全局变量，全局变量尽量用作一个类的属性，通过类的关系来约束全局变量，这样做的好处在于减少程序运行中某个数据的状态不确定性，避免程序出现莫名其妙的bug！（个人观点）

## lambda ##
>1. lambda表达式是Python中的匿名函数
>2. lambda只能用作表达式函数的定义
>3. lambda 配合在下面几个函数中可以发挥最大优势
~~~python
func1 = lambda x:x**(1/2)
func2 = lambda x:x*func2(x-1) if x>=1 else 1
print(func1(5))
print(func1(4))

print(func2(5))
print(func2(4))
~~~
>运行结果：
~~~bash
2.23606797749979
2.0
120
24
~~~
func1就是一个简单的开平方根函数，func2就比较有趣了，是一个递归求解正整数阶乘的函数**(一行代码求阶乘！)**。虽然说是匿名函数，但是可以看到函数其实还是有一个名字的，而且正常使用中这个名字还要有别于变量名，避免和普通变量混淆，其实lambda表达式的主要用途还是在下面的高阶函数中。
## map ##
>1. for循环的简写版本
>2. “映射函数”，对一个或多个系列中的元素逐一执行某函数的操作
>3. map和lambda都不能提高代码的运行效率，只能增加代码简洁性
>4. map传入多个列表作为参数时，map会自动截取相同长度的列表进行映射计算。

~~~python
lis1 = [i for i in range(10)]
lis2 = [i for i in range(8)]
mul_list = map(lambda x,y:x*y,lis1,lis2)
print(type(mul_list))
print(list(mul_list))
~~~
> 运行结果：
~~~bash
<class 'map'>
[0, 1, 4, 9, 16, 25, 36, 49]
~~~
两个长度不一的列表元素互相相乘得到的结果中元素的个数与短列表的元素个数一致。

## reduce ##
>1. map后并整合结果
>2. 同样是映射型函数调用，但只返回一个结果
>3. 映射到的函数中，必须接收两个参数
一个实例，求1/1-1/3+1/5-1/7+1/9-....
~~~python 
import math
from functools import reduce

lis_num = [i for i in range(1,100000)]
result = reduce(lambda x,y :x-1/(2*y+1) if y%2!=0 else x+1/(2*y+1),lis_num,1)
print(result*4)
print("--------")
print(math.pi)      
~~~
> 运行结果：
~~~bash
3.1415826535897198
--------
3.141592653589793
~~~
## filter ##
>1. 过滤器
>2. 也是映射型的函数调用，用于筛选列表元素
>3. filter中的函数用作筛选条件，只有列表元素经函数后返回值为True才能通过筛选，留在返回结果中

例如筛选出0~1000内的所有素数：
~~~python
num_lis = [i for i in range(1001)]


def ifDiv(num):
    if num <= 2:
        return True
    else:
        for i in range(2, round(num/2**0.5)):
            if num % i == 0:
                return False
        return True


result_lis = filter(ifDiv, num_lis)
print(list(result_lis))
# 结果就不放这里了，这里ifDiv这个函数不便用lambda表达式定义了
~~~
** 还有一些装饰器的内容下次记录了，这些内容多数是听七月老师的课后记录的笔记 **