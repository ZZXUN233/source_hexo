---
layout: post
title: LRU优化递归函数的重调用
author: zzxun
date: 2018-11-10 11:23:30
categories:
- 编程
tags:
- LRU
- lru_cache
- Python
---

# 递归调用问题 #

本文就是讲了使用python的装饰器对递归函数中重复递归（相同与之前调用的函数相同时）的一种优化。基本上是参考《流畅的Python》一书中7.8节【标准库中的装饰器】的内容。
<!--more-->
还是那个简单的例子，斐波那契数列的递归实现：

~~~python
def fabonacci(n):
    if n < 2:
        return n
    return fabonacci(n - 2) + fabonacci(n - 1)
~~~

给这个简单的递归函数一个计时作用的装饰器如下：

~~~python
def clock(func):

    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)  # 被装饰函数的执行
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs]%s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result

    return clocked
~~~

运行加入装饰器运行测试：

~~~python
@clock
def fabonacci(n):
    if n < 2:
        return n
    return fabonacci(n - 2) + fabonacci(n - 1)

if __name__ == '__main__':
    print(fabonacci(6))
~~~

{% asset_img test.png %}

调用过程，在这个递归函数中，时间消耗巨大，原因就是同参数的函数被多次调用，这种情况很容易想到一种类似动态规划算法中保留子结果的机制来优化该递归函数：

+ 使用字典存储传入的函数参数（键）和函数的返回值（值）
+ 函数调用中先判断是否已经存有该参数的返回值，有就直接return该返回值，没有就存入该返回值
+ 此时面临的问题就是如何用编程来实现这种机制，在这个递归函数中没有临时变量可以获取
+ 这个时候可以用于扩展函数功能的装饰器就派上用途了

以下以fabonacci这个递归函数定义了一个不完善的装饰器：

~~~python
def do_cache(func):
    cache = {}

    def wrapper(n):
        nonlocal  cache

        # 根据同一函数的参数情况建立返回值的字典映射
        # 根据一种传参数查询是否有存储返回值

        if n in cache:
            return cache[n]     # 如果查询到就返回该值
        else:
            cache[n] = func(n)
        return cache[n]

    return wrapper

@do_cache  ######### 使用上面的装饰器
@clock
def fabonacci(n):
    if n < 2:
        return n
    return fabonacci(n - 2) + fabonacci(n - 1)
~~~

测试结果：

{% asset_img test1.png %}

同样的函数，在用了装饰器做简单的优化后，调用次数和运行时间都得到了改善，但，这只是一个简单的实例，真实使用中，由于递归的次数可能很多，无法全部储存函数的字递归调用，这个时候就引出了LRU处理方式。

>LRU是Least Recently Used的缩写，即最近最少使用，常用于页面置换算法，是为虚拟页式存储管理服务的。

LRU并不是什么很高端的算法，在此处恰好可以作为一种调用机制来实现：以有限的存储空间存储部分递归函数的返回值，从而减少后续递归调用中的重复递归次数。

在functools模块中就有一个装饰器是利用LRU算法实现备忘功能，把耗时的函数返回值保存起来，避免传入相同的参数时重复计算，LRU限定了这个“备忘本”的长度不是无限的，一段时间后，很久没有被调用的函数存储结果会被丢弃。

# 一个重要的装饰器lru_cache #

同样是上面的例子：

~~~python
from functools import lru_cache

@lru_cache()
@clock
def fabonacci(n):
    if n < 2:
        return n
    return fabonacci(n - 2) + fabonacci(n - 1)


if __name__ == '__main__':
    print(fabonacci(6))
~~~

测试结果：
{% asset_img test2.png %}

调用次数都得到了优化，同时总的运行时间也更少了。下面来看看它这个装饰器具体做了什么事。

 **需要注意**的两点，这个装饰器在调用时 @lru_cache() 后面是更了双括号的，原因是这个装饰器可以接收配置参数，还有此处叠用了装饰器

~~~python
@lru_cache
@clock
def fabonacci(n):
    pass
~~~

这样的叠放等同于运行：lru_cache(clock(fabonacci()))

这样调用的意思是@lru_cache() 应用到 @clock返回的函数上，如果掉换顺序，打印的结果也发生了变化。从之前优化后的七次调用变成了11次调用，出现这个差异的原因我还没弄清楚，后面如果搞明白了就补以下这篇博客。。

## lru_cache的底层原理 ##

functools.py 的源码在此处{% asset_link functools.py %}，很多别的功能代码已经被我删除，保留了与lru_cache装饰器相关的代码。

lru_cache实现中涉及的几个主要问题：

1. cache缓存区的主要数据结构就是**字典**
2. 根据参数**构建字典的键**，使用了一个_make_key的私有函数，使用不定数目参数和关键字参数（如果存在的话），一同
3. 记录缓存区的信息，使用namedtuple("CacheInfo", ["hits", "misses", "maxsize", "currsize"]) 记录了【命中次数】，【未命中次数】，【缓存区最大空间】，【当前占用缓存区的大小】，四个属性
4. LRU功能，只有在用户传入该装饰器的关键字参数maxsize，且maxsize不为0时才会使用LRU机制，默认情况下视作缓存区大小无限。

lru_cache的完整签名是 functools.lru_cache(maxsize=128,typed=False)，maxsize的值应设为2的幂，typed如果为True，该装饰器会把被装饰函数的不同类型参数分开保存，另外lru_cache作用的函数参数必须是可散列的。

## LRU的代码实现： ##

我在源码注释的基础上做讲解（翻译。。），如下：

~~~python
##在这段代码之前的部分很容易理解，此处才涉及LRU机制的实现，而主要用的数据结构是双向循环链表
#双向循环链表的定义
root = []
root[:] = [root,root,None,None]  #对应的四个元素分别是PREV（上一状态，自己的一个引用）, NEXT（下一状态，同样是自己的引用）, KEY函数参数的键, RESULT函数对应返回值，

## ------如果该装饰器在被调用时传入关键字参数maxsize且不为0，则进入到此处调用：
 def wrapper(*args, **kwds):
            nonlocal root, hits, misses, full
            key = make_key(args, kwds, typed)  # 根据函数的参数做hash获取键
            with lock:                  #使用上下文管理器将对于链表的操作封装成线程安全的
                link = cache_get(key)  # 查找该键在缓存中是否存有值，注意此处的从字典获取的值为list或为None
                if link is not None:   # 查询到的情况，link就是参数键为key时的返回值
                    # 将指针移动到循环队列的前面
                    ## PREV, NEXT, KEY, RESULT = 0, 1, 2, 3  # 这是函数闭包外定义的变量
                    link_prev, link_next, _key, result = link
                    link_prev[NEXT] = link_next #更新链表的状态，查询之后就是下一状态
                    link_next[PREV] = link_prev
                    last = root[PREV]
                    last[NEXT] = root[PREV] = link
                    link[PREV] = last
                    link[NEXT] = root
                    hits += 1   # 找到则命中次数加1
                    return result
            result = user_function(*args, **kwds)
            with lock:
                if key in cache:    # 键找到的情况不做处理，因为上面已经处理了
                    pass
                elif full:  #缓存区满了的情况
                    oldroot = root
                    oldroot[KEY] = key
                    oldroot[RESULT] = result
                    # 清空旧的指针并使其指向新的链表。 保持对旧key和旧结果的引用，以防止它们的引用计数在更新期间变为零。
                    # 防止被内存回收机制所清理掉。
                    root = oldroot[NEXT]
                    oldkey = root[KEY]
                    oldresult = root[RESULT]
                    root[KEY] = root[RESULT] = None
                    # 更新缓存字典
                    del cache[oldkey]
                    # 保存该键和对应函数的返回结果在新的缓存区中，此时缓存区刚好有一个空位
                    cache[key] = oldroot
                else:  #缓存区没有对应参数的返回值
                    last = root[PREV]
                    link = [last, root, key, result]            #初始化一个新的状态，记录新状态，
                    last[NEXT] = root[PREV] = cache[key] = link     # 存入缓存中
                    full = (cache_len() >= maxsize) # 判断缓存区是否满了，cache_len()是绑定了cache.__len__的方法
                misses += 1 #未命中+1
            return result   #返回函数的结果
~~~

# LRU详情以及其它的缓存策略 #

以下这个链接中写得很好，我就不搬运了。
[Cache replacement policies](https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_Recently_Used)
