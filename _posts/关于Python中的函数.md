---
layout: post
title: 关于Python中的函数
author: zzxun
date: 2018-11-05 21:31:18
categories:
- 编程
tags:
- Python
- 函数式编程
---

>内容记录来自《流畅的Python》一书！

# 一等对象 #

Python的函数是一等对象，一等对象的特征：

+ 在运行时被创建
+ 能赋值给变量或数据结构中的元素
+ 能作为参数传给函数
+ 能作为函数的返回结果

正是因为Python中的函数具有这些属性，所以Python支持函数式编程，但是这不代表Python就是函数式编程语言。

<!--more-->

# 函数也是对象 #

这里需要知道，help() 函数作用于一个函数名时发生了什么：

~~~python
def fac(n):
    '''return n!'''
    return 1 if n<2 else n*fac(n-1)

>>>help(fac)
Help on function fac in module __main__:

fac(n)
    return n!
(END)
>>> fac.__doc__
'return n!'
>>> type(fac)  #可以看到函数属于函数类
<class 'function'>
>>>
~~~

# 高阶函数 #

** 接受函数作为参数，或者把函数作为结果返回的函数是高阶函数(higher-order function ) 。 **
前面的Python高级语法与用法中，提到了常用的几个高阶函数：

+ map
+ reduce
+ filter
+ sorted

此处还有一个概念：** 规约函数 **，像sum，reduce这类把某个操作连续应用到系列的元素上，累计之前的结果，把一系类值规约成一个值。

+ any
  > any(iterable)，如果iterable中的元素存在真值，返回True，any([])返回False。
+ all
  > all(iterable)，如果iterable中的元素都是真值，返回True，all([])返回True。

** 匿名函数，就是lambda表达式。 **

# 可调用对象 #

支持```()```（调用运算符）的对象就是可调用对象。内置函数callable() 可以判断一个对象能否被调用。Python中有7种可调用对象：

1. 用户定义的函数：使用def或lambda表达式创建
2. 内置函数：例如len()
3. 内置方法：使用C语言实现的方法，如dict.get。
4. 方法：类内定义的函数。
5. 类：调用类，会直行类的\_\_new\_\_方法，然后运行\_\_init\_\_方法，如果\_\_new\_\_没有被重写的话会返回该类的一个实例。
6. 类的实例：如果该类定义了\_\_call\_\_方法，那么该类的实例就可以作为函数调用。
7. 生成器函数：使用了yield关键字的函数或方法。

# 函数的参数问题 #

参数的种类有：

+ 普通参数```def fun(a):```
+ 带默认值的参数```def fun(a,b=2):```（带默认值的参数定义时一定放在普通参数的后面）
+ 不定数目的参数```def fun(a,*args,b=2)```（不定数目的参数和带默认值的参数跟在普通参数后，两者之间没有顺序要求）
+ 关键字参数```def fun(a,b=2,*args,**kws):```（关键字参数一定放在最后）

不定数目的参数在函数内部以tuple使用，关键字参数以字典使用。

~~~python
>>> def fun(*arg,**kws):
...     print(type(arg))
...     print(type(kws))
...
>>> fun()
<class 'tuple'>
<class 'dict'>
~~~

# 函数注解 #

~~~python
def clip(text:str,max_len:'int > 0'=80) -> str:
    '''在max_len前面或后面的第一个空格处截断文本'''
    end = None
    if len(text)>max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
    if end is None:
        end = len(text)
    return text[:end].rstrip()
~~~

原本以为函数注解可以强制规定函数参数的类型或是取值范围，可是并不能，python目前的版本没有支持这种机制，目前函数注解唯一的用处就是可以通过函数名 clip.\_\_annotations\_\_ 查看到，返回值是一个存储函数注解的字典。

~~~python
>>> def fun(a:int,b:str)->str:
...     pass
...
>>> fun.__annotations__
{'return': <class 'str'>, 'a': <class 'int'>, 'b': <class 'str'>}
~~~

# operator模块 #

这个模块中有各种运算符，可以通过dir查看，使用str.startswith('_')，看到名字多半能知道是什么运算符功能。这里有个Python比较鸡肋的地方，感觉Python中运算符重载都是基于已有的运算符的魔法方法重写实现的，那么一些特殊的运算符，比如纯粹自定义一个￥，这样的运算符没有对应的魔法方法，岂不是就不能实现重载了！

~~~python
>>> import operator
>>> [name for name in dir(operator) if not name.startswith('_')]
['abs', 'add', 'and_', 'attrgetter', 'concat', 'contains', 'countOf', 'delitem', 'eq', 'floordiv', 'ge', 'getitem', 'gt', 'iadd', 'iand', 'iconcat', 'ifloordiv', 'ilshift', 'imatmul', 'imod', 'imul', 'index', 'indexOf', 'inv', 'invert', 'ior', 'ipow', 'irshift', 'is_', 'is_not', 'isub', 'itemgetter', 'itruediv', 'ixor', 'le', 'length_hint', 'lshift', 'lt', 'matmul', 'methodcaller', 'mod', 'mul', 'ne', 'neg', 'not_', 'or_', 'pos', 'pow', 'rshift', 'setitem', 'sub', 'truediv', 'truth', 'xor']
~~~

## itemgetter ##

这两个函数能用于替代从系类中取出元素或读取对象属性的lambda表达式，所以它们能自行构建函数。示例：

~~~python
>>> students = [('s1',18),('s2',17),('s3',19),('s5',21),('s6',20)]
>>> students
[('s1', 18), ('s2', 17), ('s3', 19), ('s5', 21), ('s6', 20)]
>>> from operator import itemgetter
>>> sortd(students,key = itemgetter(1))
[('s2', 17), ('s1', 18), ('s3', 19), ('s6', 20), ('s5', 21)]
~~~

此处的key=itemgetter(1) 替代了 lambda student:student[1]
将多个值传给itemgetter，该函数则返回的是提取值构成的元组。

~~~python
>>> [itemgetter(1,0)(s) for s in students]
[(18, 's1'), (17, 's2'), (19, 's3'), (21, 's5'), (20, 's6')]
~~~

## arrtgetter ##

~~~python
>>> class Student:
...     def __init__(self,name,age):
...             self.name = name
...             self.age =age
...
>>> stu = [Student(name,age)for name,age in students]
>>> stu_sorted = sorted(stu,key = attrgetter('age'))
>>> for i in stu_sorted:
...     print(i.name,i.age)
...
s2 17
s1 18
s3 19
s6 20
s5 21
~~~

以上代码根据Student类中的age属性排序了一个包含多个Student实例的列表。

## methodcaller ##

methodcaller创建的函数会在对象上调用参数指定的方法。

~~~python
>>> from operator import methodcaller
>>> s= 'good night!'
>>> upcase = methodcaller('upper')
>>> upcase(s)
'GOOD NIGHT!'
>>> replace = methodcaller('replace',' ','-')
>>> replace(s)
'good-night!'
>>>
~~~

# functools.partial模块 #

主要用于冻结参数（自动填补某些特定参数），基于一个函数创建一个新的可调用对象，把原函数的某些参数固定。

~~~python
>>> from functools import partial
>>> from operator import mul
>>> double
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'double' is not defined
>>> double = partial(mul,2)
>>> double(4)
8
>>> double(3)
6
>>>
~~~

** 好了，今天抄书就抄这么多了 **
关于Python中的函数式编程 [Functional Programming HOWTO](https://docs.python.org/3/howto/functional.html)