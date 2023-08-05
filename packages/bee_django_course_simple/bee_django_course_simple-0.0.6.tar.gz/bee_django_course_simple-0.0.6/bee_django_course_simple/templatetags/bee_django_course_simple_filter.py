#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhangyue'

from django import template

register = template.Library()




# 求两个值的差的绝对值
@register.filter
def get_difference_abs(a, b):
    return abs(a - b)
