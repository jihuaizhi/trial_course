#！/usr/bin/env python
# -*- coding:utf-8 -*-
# __Author__ = "Ma Qing"
# __date__ = "2017/03/31"
# __Desc__ = 一个最简单的类似于Java的MessageBox的小窗口

import easygui as g
#对于大部分的EasyGui函数都有默认参数，几乎所有的组件都会显示一个消息和标题。
#标题默认是空字符串，信息通畅有一个简单的默认值
#比如msgbox()函数标题部分的参数就是可选的，所以你调用msgbox的时候可以指定一个消息参数，例如：
msg = g.msgbox("Hello Easy GUI")
#当然你也可以指定信息参数和标题参数
title = g.msgbox(msg="我一定要学会编程！",title="标题部分",ok_button="加油")

g.egdemo()