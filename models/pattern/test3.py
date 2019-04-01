# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/2/13 10:05
# Description:  
# -------------------------------------------------------------------------------
import requests

headers = {'Content-Type': 'application/json;charset=UTF-8'}
req = requests.get('http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt'
                    '=s&da_src=searchBox.button&wd=%E4%BA%BA%E6%B0%91%E5%B9%BF%E5%9C%BA&c=289&pn=0', headers=headers)
print(req.encoding)
req.encoding = 'UTF-8'
#req.encoding = 'ascii'
print(req.encoding)
print(req.apparent_encoding)

print(req.content)
