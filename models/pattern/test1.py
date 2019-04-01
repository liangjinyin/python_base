# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/1/4 17:05
# Description:  正则表达式 基础
# -------------------------------------------------------------------------------

import re

str = 'askjdfhu3iwebfid4asodh4kjcn2x5osa679ewkjfb'

# \d  匹配单个数字 ；\d+ 匹配多个或一个数字
l = re.findall('\d+', str)
l1 = re.findall('\d', str, 1)
print(l)
print(l1)

# 字符集 [] 里面的字符是或的关系 a-f a到f之内的字符

s = 'adc,abc,ahc,akc,auc'
findall = re.findall('a[a-f]c', s)
print(findall)

# 概括字符集
'''
    \d \D 数字字符 非数字字符
    \w \W 单词字符 非单词字符
    \s \S 空格字符 非空格字符
    .     匹配非\n 的任意字符
'''

# 数量词 {3,6} 贪婪模式 3到6 个字符 [a-z]{3,6}？ 非贪婪模式 匹配到3个字符就输出

a = 'python java 34786785 php #$% c '
re_findall = re.findall('[a-z]{3,6}', a)
print(re_findall)

# * 匹配 前面 的 字符 0次或者n次
# + 匹配 前面 的 字符 1次或者n次
# ？ 匹配 前面 的 字符 0次或者1次 区分非贪婪模式
b = 'pytho9987python9877pythonnnds4345'
n = re.findall('python*', b)
print(n)
# ['pytho', 'python', 'pythonnn']

# 边界匹配 ^ &  ^\d{4,8}& 以数字开头 并以4到8位结尾

qq = '375698475683'
qb = re.findall('^\d{4,8}&', qq)
print(qb)

# 组 （） [abc] 是或（|）的关系，（abc）是且（&）的关系

# 替换函数
ss = '08070df6sg67sg9gs89s0a9g8sd9g8'


def repl(value):
    group = value.group()
    if int(group) > 5:
        return '9'
    else:
        return '0'


# 每次匹配到字符就调用一次方法
sub = re.sub('\d', repl, ss)
print(sub)


# 其他函数
# match 函数从头开始匹配
# search 将搜索整个字符串并将匹配的第一个字符返回 返回的都是对象，用group函数取值 span函数取字符的位置
# 而findall是列表

# sss = 'dssdfsd435782nj46j8'
# a1 = re.match('\d', sss, re.I)
#
# a2 = re.search('\d', sss, re.I)
# print(a2.group())
# print(a2.span())
# a3 = re.findall('\d', sss)
#
# print(a1)
# print(a2)
# print(a3)

mp = 'life is too long, you must to happy'

temp1 = re.search('life(.*)happy', mp)
temp2 = re.findall('life(.*)happy', mp)
print(temp2)
print(temp1.group(1))
print(temp1.span(1))

