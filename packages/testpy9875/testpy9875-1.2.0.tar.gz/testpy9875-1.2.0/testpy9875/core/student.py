#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Student.py
@Time    :   2019/05/15 09:08:23
@Author  :   Liuyuqi 
@Version :   1.0
@Contact :   liuyuqi.gov@msn.cn
@License :   (C)Copyright 2019
@Desc    :   学生类
'''
from person import Person

class Student(Person):
    def __init__(self):
        super(Student,self).__init__()

    def getStudent(self):
        print("我是学生。")