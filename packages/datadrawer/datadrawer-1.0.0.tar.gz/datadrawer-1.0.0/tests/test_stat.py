#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_stat.py.py
@Version :   1.0.0
@Author  :   xiaxianba
@License :   (C) Copyright 2006-2019
@Contact :   xiaxianba@qq.com
@Software:   PyCharm
@Time    :   2019/5/6 14:22
@Desc    :
'''

import unittest
from datadrawer.datadrawer.src.stat import *


class TestStat(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print "This setUpClass() method only called once."

    @classmethod
    def tearDownClass(cls):
        print "This tearDownClass() method only called once too."

    def setUp(self):
        print "do something before test.Prepare environment."

    def tearDown(self):
        print "do something after test.Clean up."

    def test_get_maxdown(self):

        """
        Test method get_maxdown(list)
        根据测试数据，最终的结果为0.75，即3/4.
        """

        list_test = [100, 200, 50, 300, 150, 100, 200]
        self.assertEqual(0.75, get_maxdown(list_test))


if __name__ == "__main__":
    unittest.main()

