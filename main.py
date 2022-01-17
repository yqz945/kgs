#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@TIME        :  2021/10/13
@Author      :  YQZ
@Version     :  1.0
@Desc        :  知识图谱初始化主程序
"""
import getopt
import sys

from kg_builder import KGBuilder

builder = KGBuilder()

# The main if needed
if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], '-c:')
    for opt, arg in opts:
        if opt == '-c':
            print("开始初始化知识图谱：%s" % arg)
            builder.create_kg(arg)
            print("初始化%s知识图谱完成！" % arg)
        else:
            print("main.py -c [course]")
