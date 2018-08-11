---
layout: post
title: Python的高级语法和用法1.0
author: zzxun
date: 2018-08-11 20:21:14
categories:
- 编程
tags:
- Python
- Python枚举
- Enum
---

## 枚举类型 ##
Python中一切皆是类。
~~~python 
from enum import Enum

# 枚举的实质作用是给一组变量编号
class BookType(Enum):
    English = 1
    English_plus = 1
    Chinese = 2
    Physics = 3
    Chemistry = 4

    def __init__(self, num):
        self.num = num


# 这样Book就是一个枚举
book_type = BookType(1)
print(BookType.English)
print(BookType.English.value)
print(BookType.English.name)
print(BookType["English"])
print(BookType["English_plus"] == BookType["English"])
print("----------------------")
print(book_type.English)
print("----------------------")
for b in BookType:
    print(b)

# 打印的结果如下
# BookType.English
# 1
# English
# BookType.English
# True
# ----------------------
# BookType.English
# ----------------------
# BookType.English
# BookType.Math
# BookType.Chinese
# BookType.Physics
# BookType.Chemistry
~~~
假如我们要判断一本书的类型是什么书，用枚举就可以避免去判断书名Book.Name是否为"English"，而是判断其BookType的属性值。

如果我们不用枚举，也可用用字典来表示种类。BookType = {"English":1,"Chinese":2,...}，同样可以用一个普通类来表示。
但是问题出在：这两种方式定义的类型对应的类型值是可以被改变的，而且可能出现重复定义类型。
### 枚举的特点 ###
在枚举类中:
>1. ** 标签是唯一存在的。** 就是指:[English,Chinese,Physics,Chemistry]相当于是集合，不允许有重复的元素出现。
>2. ** 同时，枚举类定义后，其中的类型不可以在外部被更改**（不能通过BookType.English = 2来修改）。
>3. 枚举变量的访问方式有多种，BookType.English、BookType["English"]都可以获取。
>4. 值得注意的是，。添加构造函数后同样可以被实例化为对象，但这样操作意义不大，使用到枚举类时对半需要用其来充当一种类似全局变量的作用，用来分类某些数据或是对象
>5. 同个枚举类之间可以进行等值比较，BookType.English==BookType.English，返回True，但是BookType.English==1 返回False，甚至枚举变量的value也不可以进行大小比较，只能在同个枚举类之间进行等值比较。
>6. 枚举类中可以存在类型名不同，但是类型值相同的变量，比如English_Plus = 1可以被定义在BookType中，但是它只能充当一个English的别名。在遍历中别名不会被遍历到，优先视第一个作为原版。如果遍历的语句改为 for b in BookType.__members__时就可以遍历到别名。

### 一些补充 ###
1. 当存储枚举类型到数据库中时，优先存储枚举类型对应的特定数值，而不是存储类型的名称字段，这样做更加简洁，占用空间也小。同时也会遇到一些问题，当我们从数据库中取到对应的类型的value，怎么和类型对应起来？
> 这个很简单，我们可以直接用枚举类来作为类型转换使用，比如查询到一个数据的类型value为number，要知道它对应哪个类，我们只需要用BookType(number)，这样就可以知道它对应得类，** 所以前面给BookType添加构造方法的做法是无效的。**Python默认继承Enum的枚举类构造函数只能有一个参数。
2. 继承Enum的枚举类中，类型的value是可以为str类型的，如果需要使用只能为Int类型的枚举类，就需要引入新的继承类IntEnum，同样是from enum import IntEnum来引入，继承于这个类，数据项的value必须为Int类型。

** 明天继续：函数式编程、闭包，看一次能写多少就写多少，留在这里自己忘了可以及时查询**
