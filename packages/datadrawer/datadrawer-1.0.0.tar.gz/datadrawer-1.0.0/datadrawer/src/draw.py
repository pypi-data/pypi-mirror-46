#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   draw.py
@Version :   1.0.0
@Author  :   xiaxianba
@License :   (C) Copyright 2006-2019
@Contact :   xiaxianba@qq.com
@Software:   PyCharm
@Time    :   2019/5/6 15:14
@Desc    :
"""

from matplotlib import pyplot as plt


def draw_bar(list_x, list_y, label_x="X", label_y="Y", label_title="Title"):

    plt.bar(list_x, list_y, align='center')
    plt.title(label_title)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.show()
