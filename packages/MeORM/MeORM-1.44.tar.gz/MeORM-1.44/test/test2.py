#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-04-25 16:25:52
# @Author  : Blackstone
# @to      :

import sys,os
sys.path.append("..")
from morm import context


def tt():
    print (sys._getframe().f_code.co_filename) #当前文件名，可以通过__file__获得
    print (sys._getframe(0).f_code.co_name ) #当前函数名
    print (sys._getframe(1).f_code.co_name)#调用该函数的函数的名字，如果没有被调用，则返回<module>，貌似call stack的栈底
    print (sys._getframe().f_lineno) #当前行号


def ta():
	tt()

if __name__=="__main__":

	context.init()


	#context.getService("service1")

