---
layout: post
title: pipenv的使用记录
author: zzxun
date: 2018-09-18 20:34:58
categories:
- 编程
tags:
- Python
- pipenv
---

# 介绍 #

## 什么是pipenv ##

我觉得没什么好废话的，pipenv就是pipenv，一个好用的命令行工具，各个开发平台都有，以前常用的类似的叫virtualevn，让我总结这类工具的作用的话，那就是：
>pipenv和virtualenv都是让开发者在操作系统上搭建一个新的独立的python运行环境的工具，用于模块（import）管理。

廖雪峰老师的官网上是这么说virtualenv的：
>在开发Python应用程序的时候，系统安装的Python3只有一个版本：3.4。所有第三方的包都会被pip安装到Python3的site-packages目录下。 如果我们要同时开发多个应用程序，那这些应用程序都会共用一个Python，就是安装在系统的Python 3。如果应用A需要jinja 2.7，而应用B需要jinja 2.6怎么办？ 这种情况下，每个应用可能需要各自拥有一套“独立”的Python运行环境。virtualenv就是用来为一个应用创建一套“隔离”的Python运行环境。

<!--more-->

## pipenv 和pip的关系 ##

我感觉这个不用想也能知道吧！python本身进行包管理的最好工具就是pip，pip+env=pipenv就这么简单，在pipenv环境下，pip就用pipenv代替，pip install flask 变成了pipenv install flask，大致了解的话就是这么个效果，pipenv安装的包就是独立于系统的python环境中的包（site-pack）的，包的版本适配就很好解决了。

## pipenv vs virtualenv| virtualenvwrapper ##

官方的文档是这么描述它们的：

+ Pipenv 是 Python 项目的** 依赖管理器 **。如果您熟悉 Node.js 的 npm 或 Ruby 的 bundler，那么它们在思路上与这些工具类似。尽管 pip 可以安装 Python 包， 但仍推荐使用 Pipenv，因为它是一种更高级的工具，可简化依赖关系管理的常见使用情况。
+ virtualenv 是一个创建** 隔绝的Python环境 **的工具。virtualenv创建一个包含所有必要的可执行文件的文件夹，用来使用Python工程所需的包。
+ virtualenvwrapper 提供了一系列命令使得和虚拟环境工作变得愉快许多。它把您所有的虚拟环境都放在一个地方。

# pipenv基本操作 #

## 安装 ##

多平台详情请咨询[pipenv原项目](https://github.com/pypa/pipenv)
最常见的做法是：

~~~bash
pip install pipenv
~~~

## 初始化环境 ##

~~~bash
cd myproject
pipenv shell
~~~

到这里，项目目录下就多了一个包管理文件（pipfile）
这个文件的内容：

~~~python
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]

[dev-packages]

[requires]
python_version = "3.6"
~~~

同时我们已经切换到了当前的“新环境”中。

## 安装包 ##

~~~bash
pipenv install requests

PS I:\VSCODE\Python> pipenv install  requests
Installing requests...
Collecting requests
  Using cached https://files.pythonhosted.org/packages/65/47/7e02164a2a3db50ed6d8a6ab1d6d60b69c4c3fdf57a284257925dfc12bda/requests-2.19.1-py2.py3-none-any.whl
Collecting idna<2.8,>=2.5 (from requests)
  Using cached https://files.pythonhosted.org/packages/4b/2a/0276479a4b3caeb8a8c1af2f8e4355746a97fab05a372e4a2c6a6b876165/idna-2.7-py2.py3-none-any.whl
Collecting certifi>=2017.4.17 (from requests)
  Using cached https://files.pythonhosted.org/packages/df/f7/04fee6ac349e915b82171f8e23cee63644d83663b34c539f7a09aed18f9e/certifi-2018.8.24-py2.py3-none-any.whl
Collecting chardet<3.1.0,>=3.0.2 (from requests)
  Using cached https://files.pythonhosted.org/packages/bc/a9/01ffebfb562e4274b6487b4bb1ddec7ca55ec7510b22e4c51f14098443b8/chardet-3.0.4-py2.py3-none-any.whl
Collecting urllib3<1.24,>=1.21.1 (from requests)
  Using cached https://files.pythonhosted.org/packages/bd/c9/6fdd990019071a4a32a5e7cb78a1d92c53851ef4f56f62a3486e6a7d8ffb/urllib3-1.23-py2.py3-none-any.whl
Installing collected packages: idna, certifi, chardet, urllib3, requests
Successfully installed certifi-2018.8.24 chardet-3.0.4 idna-2.7 requests-2.19.1 urllib3-1.23
~~~

调试信息能看出什么？
此时目录中多了另一个文件pipfile.lock
pipfile的内容不变，之后的每次包管理都更新pipfile.lock中的内容！
pipfile.lock的内容：

~~~json
{
    "_meta": {
        "hash": {
            "sha256": "8739d581819011fea34feca8cc077062d6bdfee39c7b37a8ed48c5e0a8b14837"
        },
        "pipfile-spec": 6,
        "requires": {
            "python_version": "3.6"
        },
        "sources": [
            {
                "name": "pypi",
                "url": "https://pypi.org/simple",
                "verify_ssl": true
            }
        ]
    },
    "default": {
        "certifi": {
            "hashes": [
                "sha256:376690d6f16d32f9d1fe8932551d80b23e9d393a8578c5633a2ed39a64861638",
                "sha256:456048c7e371c089d0a77a5212fb37a2c2dce1e24146e3b7e0261736aaeaa22a"
            ],
            "version": "==2018.8.24"
        },
        "chardet": {
            "hashes": [
                "sha256:84ab92ed1c4d4f16916e05906b6b75a6c0fb5db821cc65e70cbd64a3e2a5eaae",
                "sha256:fc323ffcaeaed0e0a02bf4d117757b98aed530d9ed4531e3e15460124c106691"
            ],
            "version": "==3.0.4"
        },
        "idna": {
            "hashes": [
                "sha256:156a6814fb5ac1fc6850fb002e0852d56c0c8d2531923a51032d1b70760e186e",
                "sha256:684a38a6f903c1d71d6d5fac066b58d7768af4de2b832e426ec79c30daa94a16"
            ],
            "version": "==2.7"
        },
        "requests": {
            "hashes": [
                "sha256:63b52e3c866428a224f97cab011de738c36aec0185aa91cfacd418b5d58911d1",
                "sha256:ec22d826a36ed72a7358ff3fe56cbd4ba69dd7a6718ffd450ff0e9df7a47ce6a"
            ],
            "index": "pypi",
            "version": "==2.19.1"
        },
        "urllib3": {
            "hashes": [
                "sha256:a68ac5e15e76e7e5dd2b8f94007233e01effe3e50e8daddf69acfd81cb686baf",
                "sha256:b5725a0bd4ba422ab0e66e89e030c806576753ea3ee08554382c14e685d117b5"
            ],
            "markers": "python_version != '3.1.*' and python_version < '4' and python_version != '3.2.*' and python_version != '3.0.*' and python_version >= '2.6' and python_version != '3.3.*'",
            "version": "==1.23"
        }
    },
    "develop": {}
}
~~~

## 包迁移 ##

将当前项目和依赖的包迁移到其它的地方运行，其它的环境中只需要有pipenv就能很快的根据当前项目的pipfile.lock安装所需要的依赖。执行命令：

~~~bash
pipenv install --dev
~~~

打印信息如下：

~~~bash
Pipfile found at /Users/kennethreitz/repos/kr/pip2/test/Pipfile. Considering this to be the project home.
Pipfile.lock out of date, updating...
Assuring all dependencies from Pipfile are installed...
Locking [dev-packages] dependencies...
Locking [packages] dependencies...
~~~

## 包管理 ##

### 查看包 ###

~~~bash
pipenv graph
~~~

打印信息：

~~~bash
requests==2.19.1
  - certifi [required: >=2017.4.17, installed: 2018.8.24]
  - chardet [required: >=3.0.2,<3.1.0, installed: 3.0.4]
  - idna [required: >=2.5,<2.8, installed: 2.7]
  - urllib3 [required: >=1.21.1,<1.24, installed: 1.23]
~~~

### 移除包 ###

移除特定包：

~~~bash
pipenv uninstall requests
~~~

移除所有包:

~~~bash
pipenv uninstall --all
~~~

## pipenv运行脚本 ##

~~~bash
pipenv run test.py
~~~

pipenv会自动使用自己的python环境执行脚本。

** 突然发现记录了一堆废话，还不知不觉写（搬）了这么长的内容！主要还是无聊了！ **

细节全部在文档中！

# 相关资料链接 #

[廖雪峰老师讲的virtualenv](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432712108300322c61f256c74803b43bfd65c6f8d0d0000)

[Python最佳实践指南pipenv](https://pythonguidecn.readthedocs.io/zh/latest/dev/virtualenvs.html)

[Github上的pipenv原项目](https://github.com/pypa/pipenv)
