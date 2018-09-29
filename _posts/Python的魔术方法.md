---
layout: post
title: Python的魔术方法
author: zzxun
date: 2018-09-25 13:15:07
categories:
- 编程
tags:
- Python魔术方法
- Python
---

# 什么是魔术方法 #

## 定义 ##

在《流畅的Python》书中第一节就讲到了魔法方法：

>不管在哪种框架下写程序，都会花费大量时间去实现那些会被框架本身调用的方法，Python也不例外。Python的解释器碰到特殊句法时，会使用特殊的方法去激活一些基本的对象操作，这些特殊方法的名字以两个下划线开头，以两个下划线结尾（例如\_\_getitem\_\_），例如obj[key]的背后就是\_\_getitem\_\_方法，为了能求得my_collection[key]的值，解释器实际上会调用my_collection.\_\_getitem\_\_(key)。

<!--more-->

## 功能描述 ##

这些特殊方法能让你自己的对象实现和支持以下的语言架构，并与之交互：

+ 迭代
+ 集合类
+ 属性访问
+ 运算符重载
+ 函数和方法的调用
+ 对象的创建和销毁
+ 字符表示形式和格式化
+ 管理上下文（with块的实现）

## 命名规范 ##

> 魔术方法 (magic method) 是特殊方法的昵称。形如\_\_getitem\_\_的普遍说法是读作“双下-getitem”（dunder-getitem）这样称呼，因此特殊方法也被叫做双下方法。

# 常用的魔术方法和其调用规则 #

** 首先明确一点，魔法方法的存在是为了让解释器调用的，你自己并不需要调用它们。 **

## \_\_len\_\_ ##

~~~python
mylist = [1,2,3,4,5]
print(len(mylist))
print(mylist.__len__())
~~~

刚接触python时会发现获取一个系列对象（列表，元组，字典）的元素个数时可以有两种选择len(x)或x.\_\_len\_\_() ，看书后才知道，我们在对一个对象使用len()这个内置函数时，其实上就是在调用这个对象的\_\_len\_\_魔法方法，如果这个对象内部没有继承或是实现\_\_len\_\_这个魔法方法，那么直接调用len()就会报错。

~~~python
class A:
    pass


class B:
    def __len__(self):
        print("你竟然对我使用len()方法!")
        return 0    #注意在重写__len__方法时一定要有int类型的返回值

a = A()
b = B()
len(a)
len(B)
~~~

如果还知道一些其它的语言，比如lua语言，lua中获取一个表的元素个数时会用到#table_name，此处#号运算符和python中的len()函数作用就是一样的。

## \_\_init\_\_ ##

** 这被默认为Python中类的构造函数，但其实它并不是，它只能说是一个初始化方法！ **

Python中真正的构造函数是** \_\_new\_\_ **，\_\_new\_\_是个类方法，因为作为魔法方法被定义，所以不用使用@classmethod装饰器。而且在\_\_new\_\_方法中必须返回一个实例。它返回的实例会作为第一个参数self，传到\_\_init\_\_(self,*args,**kw)中再进行对象的初始化，\_\_init\_\_中默认返回一个类的实例对象。

书中关于Python构建对象的过程给出了下面很有Python风格的** 伪代码 **概括：

~~~python
def object_maker(the_class,some_arg):
    new_object = the_class.__new__(some_arg)
    if isinstance(new_object,the_class):
        the_class.__init__(new_object,some_arg)
    return new_object

# 有了上面的方法实现，我们创建一个对象的时候，下面的两种方式效果一样

x = Foo('bar')
x = object_maker(Foo,'bar')
~~~

## \_\_getitem\_\_ ##

直接上示例吧！如果我写了一个类Cards表示一落牌，实例化为cards后我希望通过cards[3]来获取第位置为3的这张牌，这个怎么实现，很显然我的Card类不是列表也不是字典，怎么才能做到这一点呢？

答案就是重写\_\_getitem\_\_这个魔法方法！

此处我引用书中的一个很好的示例，一摞Python风格的纸牌

~~~python
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


my_card = Card('7', 'diamonds')
~~~

类的使用：

~~~bash
my_cards = FrenchDeck()
len(my_cards)
52
my_cards[2]
Card(rank='4', suit='spades')
my_cards[50]
Card(rank='K', suit='hearts')
my_cards[:3]
[Card(rank='2', suit='spades'), Card(rank='3', suit='spades'), Card(rank='4', suit='spades')]
for card in my_cards:
    print(card)

Card(rank='2', suit='spades')
Card(rank='3', suit='spades')
Card(rank='4', suit='spades')
Card(rank='5', suit='spades')
Card(rank='6', suit='spades')
Card(rank='7', suit='spades')
Card(rank='8', suit='spades')
...
~~~

## \_\_repr\_\_ ##

使用repr()函数就会调用类中的\_\_repr\_\_方法。

~~~bash
>>> repr('s')
"'s'"
>>> repr([1,2,3,4])
'[1, 2, 3, 4]'
>>> repr(int)
"<class 'int'>"
>>> repr(len)
'<built-in function len>'
>>>
~~~

repr()这个内置函数的作用的时将一个对象用字符串的形式表达出来。

~~~bash
>>> class A:
...     def __repr__(self):
...             return "你没事打印我干啥！"
...
>>> print(A)
<class '__main__.A'>
>>> a=A()
>>> print(a)
你没事打印我干啥！
>>> repr(A)
"<class '__main__.A'>"
>>> repr(a)
'你没事打印我干啥！'
>>>
~~~

## \_\_str\_\_ ##

还记得str()这个方法吧！没错str(a)就是在调用a对象的\_\_str\_\_这个方法，前提就是a对象的类中实现了这个魔法方法！print(a)时也会优先调用这个魔法方法，如果这个方法没有实现就会去调用\_\_repr\_\_这个魔法方法！

~~~python
class A:
    def __repr__(self):
        print('A你还是调用repr了！')
        return "A你没事直接打印我干啥！"

    def __str__(self):
        return "A你看我和repr谁理你！"


class B:
    def __repr__(self):
        return "B你这下只有我了！"


a = A()
repr(a)
print(str(a))
print(a)

b = B()
repr(b)
print(str(b))
print(b)
~~~

~~~bash
A你还是调用repr了！
A你看我和repr谁理你！
A你看我和repr谁理你！
B你这下只有我了！
B你这下只有我了！
~~~

## \_\_bool\_\_ ##

这个魔法方法就比较重要了，我拿到一个变量x（一切都是对象）时，时常要判断其真假（if、while、not、or、and），实际上每次判断x真假时都是在调用bool(x)，而这个方法又是调用x.\_\_bool\_\_()的结果，重写这个方法时只能返回True或False。

此处注意几点：

+ 默认情况下我们自定义的类的实例都是被认为为True的，除非这个类的\_\_len\_\_或\_\_bool\_\_有自己的实现；
+ 如果类有自己的\_\_len\_\_或\_\_bool\_\_实现，bool()会优先调用\_\_bool\_\_；
+ 如果不存在\_\_bool\_\_时，bool()会去调用\_\_len\_\_，若返回长度为0则bool()结果为False，否则为True。

# 魔术方法一览 #

## 运算符无关的特殊方法 ##

 字符串 /字节序列表示形式

```__repr__```、```__str__```、```__format__```、```__bytes__```
数值转换

```__abs__```、```__bool__```、```__complex__```、```__int__```、```__float__```、```__hash__```、```__index__```

集合模拟

```__len__```、```__getitem__```、```__setitem__```、```__delitem__```、```__contains__```

迭代枚举

```__iter__```、```__reversed__```、```__next__```

可调用模拟

```__call__```

上下文管理

```__enter__```、```__exit__```

实例创建和销毁

```__new__```、```__init__```、```__del__```

属性管理

```__getattr__```、```__getattribute__```、```__setattr__```、```__delattr__```、```__dir__```

属性描述符

```__get__```、```__set__```、```__delete__```

跟类相关的服务
```__prepare__```、```__instancecheck__```、```__subclasscheck__```

## 运算符相关的特殊方法 ##

~~~bash
类别 方法名和对应的运算符
一元运算符
__neg__ -、__pos__ +、__abs__ abs()
众多比较运算符
__lt__ <、__le__ <=、__eq__ ==、__ne__ !=、__gt__ >、__ge__ >=
算术运算符
__add__ +、__sub__ -、__mul__ *、__truediv__ /、__floordiv__ //、__mod__ %、__divmod__
divmod()、__pow__ ** 或pow()、__round__ round()
反向算术运算符
__radd__、__rsub__、__rmul__、__rtruediv__、__rfloordiv__、__rmod__、__rdivmod__、__rpow__
增量赋值算术运算符
__iadd__、__isub__、__imul__、__itruediv__、__ifloordiv__、__imod__、__ipow__
位运算符
__invert__ ~、__lshift__ <<、__rshift__ >>、__and__ &、__or__ |、__xor__ ^
反向位运算符
__rlshift__、__rrshift__、__rand__、__rxor__、__ror__
增量赋值位运算符
__ilshift__、__irshift__、__iand__、__ixor__、__ior__
~~~

内容都来自《流畅的Python》一书中的学习笔记和一丢丢自己的理解，放在这里方便日后查看。