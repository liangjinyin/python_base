# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/4/1 14:42
# Description:  爬取小区数据
# -------------------------------------------------------------------------------
import json

import requests


class CrawlCommunity(object):

    @staticmethod
    def get_community(name):
        url_community = 'https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&c=257&da_src=searchBox.button&wd=' + name
        data = json.loads(requests.get(url_community).text)
        content = data['content']
        response_data = content[0]
        uid = response_data['uid']
        return uid

    @staticmethod
    def crawl(uid):
        url_comm = 'https://map.baidu.com/?ugc_type=3&ugc_ver=1&qt=detailConInfo&device_ratio=2&compat=1&t=1554100284590&uid=' + uid
        data = json.loads(requests.get(url_comm).text)
        content = data['content']
        name = content['name']
        address = content['addr']
        ext = content['ext']
        detail_info = ext['detail_info']
        geo_info = detail_info['guoke_geo']
        geo = geo_info['geo']
        # print(address + name + geo)
        return geo
