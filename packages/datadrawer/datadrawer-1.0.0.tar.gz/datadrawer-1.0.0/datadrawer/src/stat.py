#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   stat.py
@Version :   1.0.0
@Author  :   xiaxianba
@License :   (C) Copyright 2006-2019
@Contact :   xiaxianba@qq.com
@Software:   PyCharm
@Time    :   2019/5/6 14:11
@Desc    :
"""


def get_maxdown(list_net):

    """
    函数说明：计算最大回撤率，首先要清楚的是最大回撤率的定义，以下是百度上的解释。
    最大回撤率：在选定周期内任一历史时点往后推，产品净值走到最低点时的收益率回撤幅度的最大值。测试数据由网友提供。
    """

    maxdown = 0.0
    if type(list_net) != list:
        return 0

    for index in range(len(list_net)):
        for sub_index in range(index):
            max_net = max(list_net[:index])

            if float(max_net - list_net[index])/float(max_net) > maxdown:
                maxdown = float(max_net - list_net[index])/float(max_net)

    return maxdown
