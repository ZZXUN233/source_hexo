---
layout: post
title: python中with的实现机制
author: zzxun
date: 2018-08-07 18:54:20
categories:
- 编程
tags:
- python
- python的print
- python的with
---
## 从一个示例开始 ##
当我们用open方法来获取文件对象时，常会用到如下的写法：
~~~python
with open("sample.txt") as f_b:
    content = f_b.read(100)
~~~
使用with的优点之一是省去了异常处理和最后手动的关闭资源对象的操作（至少我是这样认为的）
如果上面的代码不用with的写法，可以像下面这样实现：
~~~python
try:
    f_b = open("sample.txt")
    content = f_b.read(100)
except Exception as e:
    pass
finally:
    f_b.close()
~~~
虽然with不是非用不可，但是最近在学习Python的Flask框架时遇到了关于with的一个用法，刚好在课程中老师也饶有兴致地讲解了with的实现机制，我开始体会到理解一些语言内部的设计思想对一个程序员来讲是很有意义的事，我举个小例子，我们在写Python的第一行代码时，多半都是写的print("hello world!")，这看起来都是再简单不过的了，但是我们再通过一些现象看深入一些就会产生疑惑。
1. 首先我们知道Python中一切都是对象，a="hello world!"，就是以Python的标准数据类型str实例化了一个对象，这个时候print(a)，我们也知道这样会打印出“hello world！”来！
2. 之后我们可能尝试了很多中数据类型，发现都可以被print()出来对应的内容！
3. 但是，但我们自己定义一个类时（MyClass），我们希望实例化的对象my_demo = MyClass()，能通过print(my_demo)出某些的信息来，这样显然一开始是做不到的，在不了解print()的实现机制，print打印的是类的哪部分数据的情况下，我是不知道怎么用print(my_demo)来打印出内容来。
4. 我们会做得是给MyClass添加自己的方法，在方法内部通过调用print()函数来打印我们需要打印的特定内容。

## 简单的特殊方法 ##
特殊方法的存在是为了让Python的解释器调用的，当一个类继承并且实现了很多特殊方法时，对于Python的解释器来讲，这个类就正在向一个强大的类靠近。
<!--more-->
** print() **函数实质上是调用了类当中的特殊方法__repr__或是__str__，如果一个类两个特殊方法都实现了，print()函数打印出__str__这个方法返回的内容。
** with **同样是用特殊函数来实现的，它包括了两个特殊函数__enter__和__exit__，定义一个类时只需要重写这两个特殊函数就可以实现用with语句来管理这个对象的上下文。看下面这个例子：
~~~python
class Hello:
    def __repr__(self):
        return "HELLO WORLD!"

    def __enter__(self):
        print("调用__enter__方法")
        return "HELLO WORLD!"
    
    def __exit__(self,exc_type,exc_value,traceback):
        print("调用__exit__方法")
        if traceback:
            print(exc_type)
            print(exc_value)
        else:
            pass
        return True

with Hello() as hello:
    print(type(hello))
    print(hello)
    1/0
print(Hello())
~~~
以上代码的执行结果如下：
~~~bash
调用__enter__函数
<class 'str'>
HELLO WORLD!
调用__exit__
<class 'ZeroDivisionError'>
division by zero
hello world!
~~~
## 答案和拓展 ##
+ with ... as object:的语法中，as后面跟的object的类型实际上是由__enter__这个特殊方法的返回值所决定的，因为返回值为"HELLO WORLD!"所以type()为str，print(hello)得到的就是 HELLO WORLD!
+ with语句范围内的异常处理实际上是在__exit__特殊方法中实现的（其实这个方法的返回值还决定了是否再次触发异常，如果返回True则代码运行到1/0处就会再次抛出异常）
+ print(Hello()) 直接打印出的内容是由__repr__返回的，如果还写了__str__函数，str(Hello())函数返回的值就是__str__这个特殊方法返回的值，同时print()打印的内容也是优先选择__str__返回的值。

## 上下文管理器 ##
在Python中，上下文管理器对象的存在目的是管理with语句，如同迭代器的存在是为了管理for语句的，而with语句的目的是简化try/finally模式，这种模式用于保证一段代码执行完毕后执行某项操作，即使那段代码由于异常、return语句或sys.exit()调用而终止，也会执行指定的操作。finally子句中的代码通常用于释放重要的资源，或者还原变更的状态。上下文管理协议包含__enter__和__exit__两个方法。with语句开始运行时，会在上下文管理对象上调用__enter__方法。with语句运行结束后，会在上下文管理器对象上调用__exit__方法，以此来扮演finally子句的角色。（这段摘抄自《流畅的Python》一书，我听到视频中的老师讲到这个问题特地查到的内容，放在这里提醒我去了解一个语言的本身实现原理）

    