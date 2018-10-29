---
layout: post
title: SQLAlchemy以及SqlSoup
author: zzxun
date: 2018-10-01 10:31:06
categories:
- 编程
tags:
- 快速ORM
- sqlsoup
- sqlalchemy
---

# ORM #

wiki说：
>Object-relational mapping (ORM, O/RM, and O/R mapping tool) in computer science is a programming technique for converting data between incompatible type systems using object-oriented programming languages. This creates, in effect, a "virtual object database" that can be used from within the programming language. There are both free and commercial packages available that perform object-relational mapping, although some programmers opt to construct their own ORM tools.

我发现高手都是直接用的Sql语句操作数据库（高效直接），不过我讨厌的点在于以string的形式在一个程序中嵌入一些sql语句，看着好别扭啊！同时修改起来很不方便，总是会定义一堆乱七八糟的变量名来标识数据库中的字段！烦得很！所以我是这么说服我自己使用ORM（成为菜鸟）的！用多了这个sql语句就基本忘记了！

<!--more-->

# SQLAlchemy #

这玩样的官网在这：
[sqlalchemy的 官网](https://www.sqlalchemy.org/)

名词解释：
 > Alchemy: 炼金术，炼丹术（炼金术士：The Alchemist）

SQLAlchemy 是 Python SQL 工具包和对象关系映射器，它为应用程序开发人员提供了SQL的全部功能和灵活性。
它提供了一整套众所周知的企业级持久性模式，旨在实现高效，高性能的数据库访问，并采用简单的Pythonic域语言。

它确实很好用：

+ 高度封装
+ 适配多种数据库
+ 成熟，高性能
+ 可模块拓展
+ [详情点这里](https://www.sqlalchemy.org/features.html)

使用经验：真正使用这个是在做一个flask项目中用到的flask-sqlalchemy，举几个小例子：

## 定义一张存放书籍的表（一个书籍的类） ##

~~~python
from sqlalchemy import Column, String
from sqlalchemy import Integer
from app.models.base import Base



class Book(Base):
    """
        一些属性定义重复性比较大，元类可以解决这个问题
    """
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    _author = Column('author', String(30), default='未名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))
~~~

## 实现数据的假删除 ##

~~~python
from sqlalchemy import Column, Integer, SmallInteger
from flask import current_app
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0

    def set_attrs(self, attrs):
        for key, value in attrs.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
~~~

所有的表都要有假删除对应的标志，如果每个表都去添加这么个标志字段就会做很多重复的工作，这个时候可以发现前面写的Book类是继承于一个Base父类的，上面我给出了Base类的实现，Base类中status字段就是用来标志假删除用的，为1就是存在状态，为0就是删除状态。
set_attrs方法是用作批量赋值使用的，delete方法就是假删除的功能实现。

## 定义自己的查找 ##

### 考虑到假删除后的查找 ###

我们前面定义了自己的数据假删除规范，现在每次查找数据自然就要避开被假删除后的数据，对于Book的查找中，我们可以进行多个字段的筛选，相当于在sql语句中WHERE后添加一个判断条件status等于1。
SqlAlchemy中调用Query类中的filter_by()方法进行查找。

~~~python
books = Book.query.filter_by(title='追风筝的人',status=1).all()
~~~

每次查询都要加入status的判断，很无聊，注意此处的query是个类，而filter_by是query下的方法，具体的实现可以自己查看源码。
默认情况下query这个类会调用SqlAlchemy提供的BaseQuery这个类，而BaseQuery又是继承于orm.Query这个类的，orm就是SqlAlchemy的两大组件之一的ORM。

SQLAlchemy的两大组件：

+ Core
  >Core本身就是一个功能齐全的SQL抽象工具包，它为各种DBAPI实现和行为提供了一个平滑的抽象层，以及一个允许通过生成Python表达式表达SQL语言的SQL表达式语言。 可以发出DDL语句以及内省现有模式的模式表示系统，以及允许将Python类型映射到数据库类型的类型系统，使系统更加完善。
+ ORM
  >对象关系映射器是一个基于Core构建的可选包。 许多应用程序都是严格在Core上构建的，使用SQL表达式系统提供对数据库交互的简洁和精确控制。

### 自定义的Query继承类 ###

**我们只能在原有的BaseQuery继承类上做些手脚**
在下面这个继承于BaseQuery类的自定义类中，我们对它的filter_by方法做了一些手脚，手脚的内容很简单，就是在查找中如果没有指明是否是假删除的数据，我们默认查找status=1就是没有被假删除的数据，这样就省去了每次查找都要再次筛选没有被假删除的数据！

~~~Python
from flask_sqlalchemy import BaseQuery

class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)

~~~

## 用上下文管理器来自动递交事务 ##

记得在使用SQLAlchemy的过程中，每次修改数据后总是要做事务的手动提交。
下面是一部分示例代码：

~~~Python
form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():    # 表单校验通过后
        user = User()                                   # 创建对象
        user.set_attrs(form.data)                       # 从表单向对象传参数
        db.session.add(user)                            # 添加对数据库操作的事务
        db.session.commit()                             # 提交事务
~~~

事务在数据库中很重要，我就不说了，总之用户一次事务如果提交失败要直接回到数据修改前的状态才是正确的做法。

怎么简写db.session这几句代码呢？要能想到Python的上下文管理器，简单说就是with。

~~~python
from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self, throw=True):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            current_app.logger.exception('%r' % e)
            if throw:
                raise e
~~~

注意这里使用了contextlib提供的上下文管理器装饰器，而不是按照之前的方式去重新实现SQLAlchemy这个类的__enter__和__exit__这两个魔法方法，因为后者是直接将这个类变成了可以被上下文管理器处理的一个类，而我们实际上只希望这个类中自动递交事务这个方法被上下文管理器所管理。沃日，感觉写到这里又要去讲这个上下文管理器了甚至要讲这个yield关键字的使用了。。。
auto_commit的使用。

~~~Python
form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():        # 表单校验通过后
        with db.auto_commit():                              # 使用上下文管理器来管理数据库操作
            user = User()                                   # 创建对象
            user.set_attrs(form.data)                       # 从表单向对象传参数
~~~

虽然代码没有多少改变和优化，不过我觉得上下文管理器用在在这里确实是一个很好的选择。就像操作文件用with open这样可以省去关闭文件对象的操作，而此处就是省去了手动提交事务的操作。

本来下面的内容才是今天想写的，但是前面提了这么多。

## 一个小问题 ##

有没有更高效的创建数据库的方法，同时操作这些数据库又能以Object(对象)来操作，而不是用各种字符串的sql语句。这就引出了下面这个库的使用！

>我们现在要创建ORM映射后的数据库，必须先定义一个对象类，再根据这个类去生成一个表。尽管在MVC中model包括了数据模型和与模型相关的一系列操作，这样封装在一个类中刚好。但仍然存在某些情况我们仅仅做一些简单的数据存储操作，而又定义一堆的类真的有些多余，我认为，实际上我们定义类只是希望在程序中操作起数据库来更方便。我认为创建数据最快的方式还是设计好数据库后，直接在可视化工具比如 Navicat 上操作，不过可能创建很多时需要人为去点也不好。不考虑建库效率这个因素，假如我们连接了一个没有进行ORM映射的已有数据库，要对其进行Object操作怎么办呢！

# SqlSoup #

>SQLSoup是一个基于SQLAlchemy对象关系映射器构建的一步式数据库访问工具。

[sqlsoup的官方文档](https://sqlsoup.readthedocs.io/en/latest/)

## 使用示例 ##

我所操作的数据库如下：
{% asset_img sqlite_db.png %}

### 借助SQLAlchemy连接本地sqlite数据库 ###

~~~python
import sqlalchemy
import sqlsoup
import create_engine


create_engine('sqlite:///test.db')
db = sqlsoup.SQLSoup(engine)

books = db.book.all()       # 获取所有的书籍记录
print(books[2])
#MappedBook(id=3,title='Python学习手册',price='89.0',isbn='9787111267768 ')

def findPythonBooks(book):
    if hasattr(book,'title'):
        return True if 'python' in book.title.lower() else False
    else:
        return False
pythonBooks = filter(findPythonBooks,books)
print(list(pythonBooks))    # 可以看到书名中带python关键字的记录都被查出来了
#[MappedBook(id=2,title='Python for Unix and Linux System Administration',price='49.99',isbn='9780596515829'), MappedBook(id=3,title='Python学习 手册',price='89.0',isbn='9787111267768 '), MappedBook(id=4,title='Python源码剖析',price='69.8',isbn='9787121068744 ')]

# orm了同样可以进行一些特定的orm查询操作
net_book = db.book.filter_by(title='计算机网络').one()
print(net_book)
# MappedBook(id=1,title='计算机网络',price='66',isbn='9787111165057 ')
~~~