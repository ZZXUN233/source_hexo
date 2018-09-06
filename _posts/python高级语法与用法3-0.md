---
layout: post
title: python高级语法与用法3.0
author: zzxun
date: 2018-08-13 08:37:36
categories:
- 编程
tags:
- Python装饰器
- Python的switch替代方案
- None是什么鬼
---

# Python装饰器 #

1. 把装饰器当作一种函数Plus模块来使用
2. 装饰器的关键字符是** @ **
3. 装饰器作用于函数，同时由函数构成，也属于函数式编程
4. 装饰器定义时需要注意函数传参数的问题（*args,**kw）

## 装饰器的编写 ##

写一个自动计算函数运行时间的装饰器：看代码很快就能明白什么是装饰器，装饰器发挥的作用……

~~~python
import timeit
import random


def timmer(func):
    count = 0

    def get_timmer(*args, **kw):
        nonlocal count
        start = timeit.default_timer()
        result = func(*args, **kw)
        stop = timeit.default_timer()
        count += 1
        print("Func %d running for %ss" % (count, str(stop-start)))
        return result
    return get_timmer
~~~

<!--more-->

+ 说明： 这里的timmer就是一个装饰器了，外层函数timmer接受的参数被作为一个函数名在内层函数get_timmer中调用，get_timmer中的参数*args,**kw被用来解决装饰器调用时函数参数的不确定性，内层函数中的result用来解决函数返回值的不确定性，当调用装饰器的函数没有返回值时result返回的就是None，有返回值时返回的就是函数的返回值。

## 装饰器的调用 ##

在需要计时的函数定义的前一行使用@timmer就相当于给函数加了一个自动计时的功能模块，后面调用这个被装饰的函数时，函数就具备自动计时打印的功能。

实例如下：

~~~python
@timmer
def fun1(num):
    return num*fun1(num-1) if num >= 1 else 1
# 递归函数中使用装饰器，每次递归调用函数都会执行装饰器功能


@timmer
def count():
    count = 0
    for _ in range(1000):
        for _ in range(1000):
            count += 1
    print(count)


@timmer
def get_pi(times):
    count = 0
    for _ in range(times):
        p_x, p_y = random.random(), random.random()
        distance = (p_x**2+p_y**2)**(1/2)
        if distance <= 1:
            count += 1
    print(count/times*4)
    return count/times*4


#递归函数的调用
print(fun1(6))

print("---------")
get_pi(10000)
get_pi(100000)
get_pi(200000)
print(get_pi(300000))
~~~

> 运行结果：

~~~bash
PS I:\VSCODE\Python> python .\timmer.py
Func 1 running for 3.95061728395062e-07s
Func 2 running for 0.0001785679012345679s
Func 3 running for 0.0002808888888888889s
Func 4 running for 0.000351604938271605s
Func 5 running for 0.0004882962962962962s
Func 6 running for 0.0008541234567901234s
Func 7 running for 0.0012641975308641975s
720
---------
3.1656
Func 1 running for 0.009908938271604939s
3.13736
Func 2 running for 0.08166755555555555s
3.14146
Func 3 running for 0.15069866666666665s
3.13848
Func 4 running for 0.22512355555555558s
3.13848
~~~

代码说明：@timmer 这个语句使用就是在调用装饰器的功能，作用域就是@timmer下面定义的整个函数：

+ func1 :是一个递归求解阶乘的函数，递归函数不建议使用装饰器，函数的每一次递归调用都会执行装饰器的功能，所以func(6)调用了7次装饰器的功，进入调用一次，6递归六次直至减为1功六次，而总时间得把七次的时间累加起来，但是这个装饰器没有做到这一点。

+ count，get_pi（随机抛点用概率求解Pi的函数）都是正常的使用，没有什么好说的。

在Flask这个web框架中，路由机制还有用户登陆状态检测都是使用装饰器来实现的。

# switch的替代方案 #

Python中虽然没有switch ... case ...但是有几种公认的好的实现switch的方式。
我还是特别喜欢switch case的写法，感觉这种写法规整而优美……

~~~java
switch(day){
    case 1:monday();break;
    case 2:tuesday()break;
    case 3:wednesday();break;
    //...
    default:Uknow;break;
}
// 尴尬，好久没接触Java都快忘了，反正大概就是这么个意思！
~~~

但是它没有，虽然功能是可以实现的。
> if ... elif ...else.
> dict，字典映射

## py为什么没有switch ##

这个我不知道，但是官方给出了说法：[why there is no switch in python](https://docs.python.org/2/faq/design.html#why-isn-t-there-a-switch-or-case-statement-in-python)

## if ... elif ... else ##

话不多说，直接看实例：

~~~python
week = [1, 2, 3, 4, 5, 6, 7]


def monday():
    pass


def tuesday():
    pass


def wednesday():
    pass

# ...


def default():
    print("Unknow!")


for day in week:
    if day == 1:
        monday()
    elif day == 2:
        tuesday()
    elif day == 3:
        wednesday()
    # ...
    else:
        print("Uknow!")
~~~

## switcher = {...} ##

~~~python
switcher = {
    1: monday,
    2: tuesday,
    3: wednesday, #这些都是前面定义的函数名

    # ...
}

for day in week:
    switcher.get(day, default)()  # 注意当作函数调用，default同样是个函数名
~~~

与switch...case...的对比：
> case：后面可以接一些逻辑实现，同时也可以加入函数模块
> 字典映射作为值传给对应的键，值要么是特定的值，要么是一个函数的返回值，也就是说需要逻辑代码的话只能在函数中实现。
> default用if...elif...else实现时体现在else语句上，用字典映射时体现在dict.get()方法中的键以外的参数（找不到这个键时，返回的值）。

# None是什么鬼 #

** None就是None **

~~~python
>>> None == False
False
>>> type(None)
<class 'NoneType'>
>>> None != False
True
>>> not None
True
>>> def fun():
	pass
>>> a = fun()
>>> type(a)
<class 'NoneType'>
>>> a is None
True
>>> not []
True
>>> not [] == None
True
>>> not [] == True
True
~~~

使用bool()操作一个自定义对象时，返回的是True还是False由什么决定？

~~~python
>>> class A:
	pass

>>> a = A()
>>> bool(a)
True

>>> class B:
	def __len__(self):
		return 0

>>> b=B()
>>> bool(b)
False
>>> class C:
	def __bool__(self):
		return True
	def __len__(self):
		return 0

	
>>> c = C()
>>> bool(c)
~~~

当一个类的__len__返回为0，同时__bool__没有被重写时，bool()这个类就会获得False的返回值，
当一个类的__len__返回不为0，__bool__没有被重写，bool()返回值就为True，若__bool__被重写，则返回值为__bool__的返回值。

** 判断某个变量是否为None时 **

+ if a is None:
+ if a:

两种表达中，** if a的兼容性更好 **

### 都是些基础的东西，后面发现错误再更正 ###