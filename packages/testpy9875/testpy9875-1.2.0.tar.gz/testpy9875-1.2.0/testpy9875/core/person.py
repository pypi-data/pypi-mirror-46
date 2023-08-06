#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Person.py
@Time    :   2019/05/15 09:08:44
@Author  :   Liuyuqi
@Version :   1.0
@Contact :   liuyuqi.gov@msn.cn
@License :   (C)Copyright 2019
@Desc    :   Person 类
'''


class Person:
    def __init__(self):
        self.name = "张二麻子"
        self.sex = 0
        self.age = 18

    def setAge(self,age:int):
        self.age = age

    def printPerson(self):
        print("姓名：",self.name,"年龄：",self.age,"性别：",self.sex)