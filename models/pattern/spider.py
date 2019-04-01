# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/1/9 11:10
# Description:  原声爬虫实例
# -------------------------------------------------------------------------------

"""
1、访问网页获取html
2、分析html并爬取目标数据
3、整理数据
4、业务处理
"""

import re
import requests
from bs4 import BeautifulSoup


class Spider():
    url = 'https://www.lagou.com/jobs/list_java?city=%E5%B9%BF%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput='
    root_pattern = '<li.*?data-index="(.*?)".*?data-company="(.*?)" data-positionname="(.*?)" .*?>'
    zy_name = '< h3 style = "max-width: 180px;" >([\s\S]*?)< / h3 >'
    addr_name = '<em>([\s\S]*?)</em>'

    @staticmethod
    def __get_html():
        htmls = requests.get(Spider.url).text
        return htmls

    @staticmethod
    def __analysis(html):
        datas = re.findall(Spider.root_pattern, html, re.S)
        for data in datas:
            zy_name = re.findall(Spider.zy_name, data)
            cp_name = re.findall(Spider.cm_name, data)
            zy_name[0]
            a = 1

    def my_main(self):
        html = self.__get_html()
        datas = self.__analysis(html)


spider = Spider()
spider.my_main()
