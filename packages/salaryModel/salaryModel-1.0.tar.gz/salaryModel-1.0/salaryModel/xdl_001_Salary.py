#!/usr/bin/env python  #add this to make sure ***.py run in terminal
# -*- coding: utf-8 -*- #add this to make sure ***.py read by utf-8

'【模块简介】用于计算公司员工的薪资'
__author__ = 'egret'

company = '飞鸿雪科技'

def yearSalary(monthSalary):
    '''根据传入的月薪 计算年薪'''
    return monthSalary*12

def daySalary(monthSalary):
    '''根据传入的月薪 计算1天薪资'''
    return monthSalary/22

#用于模块测试 不会在模块导入时自动运行
# if __name__ == "__main__":
#     print(yearSalary(5000))
#     print(daySalary(5000))
