import difflib
# import jieba
# import Levenshtein

str1 = "我的骨骼雪白 也长不出青稞"
str2 = "雪的日子 我只想到雪中去si"

# 1. difflib
seq = difflib.SequenceMatcher(None, str1, str2)
ratio = seq.ratio()
print('difflib similarity1: ', ratio)


# difflib 去掉列表中不需要比较的字符
seq = difflib.SequenceMatcher(lambda x: x in ' 我的雪', str1, str2)
ratio = seq.ratio()
print('difflib similarity2: ', ratio)


# 2. hamming距离，str1和str2长度必须一致，描述两个等长字串之间对应位置上不同字符的个数
# sim = Levenshtein.hamming(str1, str2)
# print 'hamming similarity: ', sim

# 3. 编辑距离，描述由一个字串转化成另一个字串最少的操作次数，在其中的操作包括 插入、删除、替换
# sim = Levenshtein.distance(str1, str2)
# print
# 'Levenshtein similarity: ', sim
#
# # 4.计算莱文斯坦比
# sim = Levenshtein.ratio(str1, str2)
# print
# 'Levenshtein.ratio similarity: ', sim
#
# # 5.计算jaro距离
# sim = Levenshtein.jaro(str1, str2)
# print
# 'Levenshtein.jaro similarity: ', sim
#
# # 6. Jaro–Winkler距离
# sim = Levenshtein.jaro_winkler(str1, str2)
# print
# 'Levenshtein.jaro_winkler similarity: ', sim
