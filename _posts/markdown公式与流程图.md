---
layout: post
title: markdown的一系列扩展支持
author: zzxun
date: 2018-12-16 14:57:21
categories:
- 测试
tags:
- hexo流程图、时序图、UML图、甘特图支持
---

>什么是Markdown
>Markdown 是一种方便记忆、书写的纯文本标记语言，用户可以使用这些标记符号以最小的输入代价生成极富表现力的文档：譬如您正在阅读的这份文档。它使用简单的符号标记不同的标题，分割不同的段落，**粗体**或者*斜体*某些文字，更棒的是，它还可以:

<!--more-->

# 基本功能 #

参考[hexo markdown简明语法手册](https://hyxxsfwy.github.io/2016/01/15/Hexo-Markdown-%E7%AE%80%E6%98%8E%E8%AF%AD%E6%B3%95%E6%89%8B%E5%86%8C/)

# 数学公式的插入 #

打开hexo配置文件_config.yml中mathjs的支持：

~~~yml
mathjax:
  enable: true
  per_page: true
  cdn: //cdn.bootcss.com/mathjax/2.7.1/latest.js?config=TeX-AMS-MML_HTMLorMML
~~~

[参考网站](https://www.zybuluo.com/codeep/note/163962)
> Cmd Markdown 编辑阅读器支持 $\LaTeX$ 编辑显示支持，例如：$\sum_{i=1}^n a_i=0$，访问 [MathJax](http://meta.math.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference) 以参考更多使用方法。

$\LaTeX$ 的数学公式有两种：行中公式和独立公式。行中公式放在文中与其它文字混编，独立公式单独成行。

**自动编号后的公式可在全文任意处使用 `\eqref{eq:公式名}` 语句引用。**

- 例子：

行内公式实例：$ x^{y^z}=(1+{\rm e}^x)^{-2xy^w} {, 行内公式}$

- 例子：

$$ J_\alpha(x) = \sum_{m=0}^\infty \frac{(-1)^m}{m! \Gamma (m + \alpha + 1)} {\left({ \frac{x}{2} }\right)}^{2m + \alpha} \text {，独立公式示例} $$

# todo 列表 #

**hexo默认支持**

- [ ] 支持以 PDF 格式导出文稿
- [ ] 改进 Cmd 渲染算法，使用局部渲染技术提高渲染效率
- [x] 新增 Todo 列表功能
- [x] 修复 LaTex 公式渲染问题
- [x] 新增 LaTex 公式编号功能

# 流程图示例 #

~~安装插件：**hexo-filter-flowchart**~~
~~npm install --save hexo-filter-flowchart~~

安装插件： **hexo-tag-mermaid**

~~~bash
npm install --save hexo-tag-mermaid
~~~

注意在Next主题下使用这个插件，需要在 **themes\next\layout\_custom\header.swig** 文件中添加

~~~html
<script  type="text/javascript" src="https://cdn.bootcss.com/mermaid/6.0.0/mermaid.min.js"></script> 
<link rel="stylesheet" href="https://cdn.bootcss.com/mermaid/6.0.0/mermaid.min.css" type="text/css"/>
~~~


{% mermaid %}
graph TD
    A[Christmas] -->|Get money| B(Go shopping)
    B --> C{Let me think}
    C -->|One| D[Laptop]
    C -->|Two| E[iPhone]
    C -->|Three| F[Car]
{% endmermaid %}

# 时序图示例 #

~~安装插件：**hexo-filter-sequence** 部署出问题~~
~~npm install --save hexo-filter-sequence~~
安装插件： **hexo-tag-mermaid**

{% mermaid %}
sequenceDiagram
    participant John
    participant Alice
    Alice->>John: Hello John, how are you?
    John-->>Alice: Great!
{% endmermaid %}


# 甘特图示例 #

安装插件： **hexo-tag-mermaid**

[语法参考](https://mermaidjs.github.io/)

{% mermaid %}
gantt
    dateFormat  YYYY-MM-DD
    title Adding GANTT diagram functionality to mermaid

    section A section
    Completed task            :done,    des1, 2014-01-06,2014-01-08
    Active task               :active,  des2, 2014-01-09, 3d
    Future task               :         des3, after des2, 5d
    Future task2               :         des4, after des3, 5d

    section Critical tasks
    Completed task in the critical line :crit, done, 2014-01-06,24h
    Implement parser and jison          :crit, done, after des1, 2d
    Create tests for parser             :crit, active, 3d
    Future task in critical line        :crit, 5d
    Create tests for renderer           :2d
    Add to mermaid                      :1d

    section Documentation
    Describe gantt syntax               :active, a1, after des1, 3d
    Add gantt diagram to demo page      :after a1  , 20h
    Add another diagram to demo page    :doc1, after a1  , 48h

    section Last section
    Describe gantt syntax               :after doc1, 3d
    Add gantt diagram to demo page      : 20h
    Add another diagram to demo page    : 48h
{% endmermaid %}

# UML示例 #

安装插件： **hexo-tag-plantuml**

~~~bash
npm install hexo-tag-plantuml --save
~~~

[**在线调试网站**](https://www.planttext.com/)

{% plantuml %}

title Relationships - Class Diagram


class Dwelling {
  +Int Windows
  +void LockTheDoor()
}

class Apartment
class House
class Commune
class Window
class Door

Dwelling <|-down- Apartment: Inheritance
Dwelling <|-down- Commune: Inheritance
Dwelling <|-down- House: Inheritance
Dwelling "1" *-up- "many" Window: Composition
Dwelling "1" *-up- "many" Door: Composition

{% endplantuml %}

最后希望自己以后少写点废话，多学点和多写点有用的东西！