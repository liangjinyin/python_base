# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/1/8 16:24
# Description:  函数式编程
# -------------------------------------------------------------------------------
import time
from functools import reduce

# 函数式编程 map的用法

list_x = [1, 23, 4, 54, 5, 6, 6, 67]
list_y = [3, 54, 6, 7, 8, 89, 99, 545]

r = map(lambda x, y: x + y, list_x, list_y)
print(tuple(r))
print(list(r))

# 函数式编程 reduce的用法 一定要用两个参数
# 第一次执行时 取list_x 的前两个元素 ，之后就将结果和第三个元素进行表达式的计算

m = reduce(lambda x, y: x + y, list_x)
print(m)

# 函数式编程 filter的用法

f = filter(lambda x: True if x > 8 else False, list_x)
# f = filter(lambda x: x, list_x)
print(list(f))


# 装饰器 不改变原来的函数内容，装饰原来的函数  **kw 关键字参数

def decorator(func):
    def war(*args):
        print(time.time())
        func(*args)

    return war()


@decorator
def func1(name1):
    print('haha')


@decorator
def func2(name1, name2):
    print('haha')


func1(name1=1)
func2(name1=1, name2=2)
