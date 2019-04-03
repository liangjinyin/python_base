# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/4/2 15:14
# Description:  
# -------------------------------------------------------------------------------
import json

import requests
import pandas as pd
import re


def main():
    excel_ori = pd.read_excel('zhuhai1.xlsx', sheet_name='zh')
    data_list = excel_ori.values
    print('数据有' + str(len(data_list)) + '条！')
    fail_list = []
    i = 0
    for data in data_list:
        i = i + 1
        print(str(i))
        build_type = data[0]
        build_id = data[1]
        city = data[2]
        city = city[0:2]
        sub = data[3]
        sub = sub.replace('分公司', '')
        build_name = data[4]
        # l = re.findall('\D*', '珠海市斗门区五山荔山村榕苑小区二巷13号')
        # build_name='珠海市斗门区五山荔山村榕苑小区二巷13号'
        # build_name = build_name.split('小区')
        if build_type == '地址':
            name = build_name
        else:
            name = city + ' ' + sub + ' ' + build_name
        url_community = 'https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&c=140&da_src=searchBox.button&wd=' + name
        data = json.loads(requests.get(url_community).text)
        if 'content' not in data:
            fail_list.append(build_name)
        else:
            content = data['content']
            if len(content) > 0:
                for temp in content:
                    if 'area_name' in temp:
                        area_name = temp['area_name']
                        if area_name == city + sub:
                            print(build_id)
    print('没有数据有' + str(len(fail_list)) + '条！')


if __name__ == '__main__':
    main()
