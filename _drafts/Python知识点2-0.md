---
layout: post
title: Python知识点2.0
author: zzxun
date: 2018-08-11 15:52:18
categories:
- 编程
tags:
- python知识点
---
## 正则表达式

** 正则表达式时一个特殊的字符系列，用于判断另一个字符串是否与我们所设定的这样的字符系列相匹配，快速检索文本功能...**

1. Python 字符串内置的一些字符检索功能：
~~~python
a = "C|C++|Java|Perl|Lisp|Ruby|swift|Python"
a.index("Python")
32
a.find("python")
-1
a.find("Python")
32
"Python" in a
True
~~~
2. 正则表达式的方式实现
~~~python
a = "C|C++|Java|Perl|Lisp|Ruby|swift|Python"
import re
re.findall("Python",a)
['Python']
#"Python"本身是一个常量表达式，实际中的表达式是一种匹配规则
~~~
正则表达式有普通字符+元字符构成。普通字符就是没有特殊含义的字符，元字符如：\d表示数字[0-9],\n表示换行符，\S表示任何不可见字符。** 忘记相关元字符后直接百度百科就可以查到一堆 **



