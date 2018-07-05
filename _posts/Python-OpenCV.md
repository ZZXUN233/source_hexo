---
layout: post
title: Python-OpenCV
date: 2018-04-14 14:19:03
categories:
- programming
tags: [Python, OpenCV]
---


# 安装
最方便的当然是使用pip安装了
~~~bash
sudo pip3 install opencv-python
~~~
其它平台的可以自己查看[官网文档](https://docs.opencv.org/3.1.0/)
# opencv初次使用
+ 预览图片
> 使用opencv预览图片
imread方法
~~~python
import cv2

img = cv2.imread('img/1.jpg', cv2.IMREAD_GRAYSCALE)
cv2.imshow(img)
cv2.waitKey(0)
cv2.destoryAllWindows()
~~~
## 图片颜色模式
cv2.IMREAD_GRAYSCALE是opencv支持的一种读入颜色模式，使用该模式是将原图片以灰度形式读入。
>常用的颜色模式有：
>+ IMREAD_COLOR   #RGB颜色
>+ IMREAD_GRAYSCALE  #灰度
>+ IMREAD_UNCHANGED  #原图 
## 图片写入
~~~python
cv2.imwrite('img/2.jpg', img)
~~~
>以上代码就是将读出来的图片数据重新写入一个新的图片，这时会在img/目录下生成一个新图片。
## 摄像头调用
捕捉实时画面的代码实现
~~~python
cap = cv2.VideoCapture(1)
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #将捕获的图片进行灰度处理
    out.write(frame)
    cv2.imshow('frame', frame)  #显示为原画
    cv2.imshow('gray',gray)  #显示为灰度模式
    if cv2.waitKey(1) & 0xFF == ord('q'):  #必须写这个，按下q键时退出死循环
        break

cap.release()  # 释放摄像头资源
cv2.destroyAllWindows()  #关闭所有opencv打开的窗口
~~~
## 视频录制
~~~python
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
cap = cv2.VideoCapture(1)
while True:
    ret, frame = cap.read()
    out.write(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
~~~
>+ VideoWrite_fourcc(*'XVID')
>+ VideoWriter
>此处我们创建了一个VideoWrite对象，它可以实现将获取的帧图像拼接为视频，参数中依次指定了输出视频的文件名，编码方式，fps（每秒多少帧，此处设置为20），压缩帧大小为640*480，最后还有一个可选参数为是否着色，如果为True编码器会强制彩色帧，False则可以保存为灰度帧。
> FourCC是用于指定视频编解码器的4字节代码。可用代码列表可以在fourcc.org中找到。它依赖于平台。
>>+ 在Fedora中：DIVX，XVID，MJPG，X264，WMV1，WMV2。（XVID是更可取的，MJPG产生高分辨率视频，X264分辨率非常小）
>>+ 在Windows中：DIVX
>>+ 在OSX中：*

## 最近接着学习如何用opencv在图片上绘制内容
