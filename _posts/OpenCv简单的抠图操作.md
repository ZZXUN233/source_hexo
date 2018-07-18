---
layout: post
title: OpenCv简单的抠图操作
author: zzxun
date: 2018-07-17 20:53:40
categories:
- 编程
tags:
- Python
- OpenCv
- 简单抠图
---

## OpenCv简单的抠图 ##
具体就是用代码实现下面的流程：最后得出一个抠图并帖在另外一张图正中间的效果。
{% asset_img step.png %}
一般的图像本身是由像素点矩阵构成的，每个像素点其实就是(B, G, R)三个颜色的组合，注意这里不是按照我们常说的RGB的顺序排列的，是按照Blue,Green,Red,这样排列的。如下：
{% asset_img BGR.png %}
这里有几个常识需要知道：
+ 灰色的图像就是B、G、R三个值相等时就显示为灰色，所以灰色在这里有0~255级{% asset_img gray.png %}
+ RBG光的三原色对应的数值可以用来做加减乘除的运算，但是在opencv中只能取[0~255]之间的整数，所以小于0算作0，大于255算作255就是opencv对图像的运算。
+ 出了基本运算外，还可以做逻辑运算(对应函数如下：){% asset_img logicOptions.png %}
>+ not 
>+ and 
>+ or   
>+ xor
具体操作后的效果以及操作的用途后面估计得花一次来细写，本次主要记录抠图并贴图的流程。
~~~python
import cv2
import numpy as np


img = cv2.imread("imgs/1.png", cv2.IMREAD_COLOR)
logo = cv2.imread("imgs/logo.jpg", cv2.IMREAD_COLOR)
imggray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)  #灰度处理 
row, col = (img.shape[0] - logo.shape[0]) // 2, (img.shape[1] - logo.shape[1]) // 2  #计算中间位置
roi = img[row:row + logo.shape[0], col:col + logo.shape[1]]
ret, mask = cv2.threshold(imggray, 220, 255, 1)     #同Photoshop软件中的阈值处理
# 低于150的置为0，高于的置为255
mash_inv = cv2.bitwise_not(mask)  # 取反，黑白颠倒
img1_bg = cv2.bitwise_and(roi, roi, mask=mash_inv)
img2_fg = cv2.bitwise_and(logo, logo, mask=mask)
dst = cv2.add(img1_bg, img2_fg)
dst2 = img1_bg + img2_fg
cv2.imshow("dst2", dst2)
img[row:row + logo.shape[0], col:col + logo.shape[1]] = dst

cv2.imshow("maked_img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
~~~
进行本次操作的实现代码如下，可以根据这个写一个批量添加水印的程序，只需要改水印的最终放置位置和替换水印的文件logo.jpg,水印的位置摆放可以根据img.shape来计算，300*200像素的图像，imread后获得的就是numpy中np.array的一个300*200*3的矩阵，x轴对应300，y轴对应200，其中每个点又是BGR的3元组(class'tuple')，所以img.shape = (300,200,3)，最后假设要将水印贴在最右下角，贴图的位置就是:需要加水印的图为imgSrc,水印为imgLogo
+ xStart = imgSrc.shape[0] - imgLogo.shape[0]
+ xEnd = imgSrc.shape[0]
+ yStart = imgSrc.shape[1] - imgLogo.shape[1]
+ yEnd = imgSrc.shape[1]
+ imgSrc[xStart:xEnd,yStart:yEnd] = imgLogo   #最后的贴图操作

## 最后的一些总结 ##
我们之前学习的线性代数在这里终于用到了，这个时候才后知后觉地发现自己之前荒废的现代课是多么可惜，开始发现矩阵在可以被映射到生活中的很多地方，它远比求解多元方程组要复杂深奥的多，但是话又说回来了，生活中可以把很多事物映射为变量，最后决解某问题也就是求解一些未知变量的过程，后面我还会持续预习线性代数，概率论，高数的知识吧！！
有时候我们人太擅长观察一些现象的整体了，忽视了太多的细节，而造成一种主观的误解。如下面的色块：
{% asset_img R+B.png %}
{% asset_img R+G.png %}
{% asset_img G+B.png %}
如果要看清它们的原貌，或许得下载下来放大了看！

