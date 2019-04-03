# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/4/1 15:35
# Description:  小区爬取主类
# -------------------------------------------------------------------------------

from models.xiaoqu.trans_to import community_info
from models.xiaoqu.crawl_community import CrawlCommunity
from models.xiaoqu.minqu import Converter
import pandas as pd


def main():
    # 解析输入源
    # excel_ori = pd.read_excel(io='data.xlsx')
    # a = excel_ori.values
    # 爬取小区数据
    uid = CrawlCommunity.get_community('恒大绿洲')
    geo = CrawlCommunity.crawl(uid)
    # 将小区的摩卡坐标换为百度坐标
    geom_temp = Converter.my_geom(geo)
    print("数据百度坐标：" + geom_temp)
    # 将百度坐标换为w84坐标
    temp_split = geom_temp.split(';')
    str_geom = ''
    for coordinates in temp_split:
        split = coordinates.split(',')
        hx_list = community_info.bd_to_hx(split[0], split[1])
        list_84 = community_info.hx_to_84(hx_list[0], hx_list[1])
        str_geom = str_geom + list_84
        if len(str_geom) != 0:
            str_geom = str_geom + ';'
    print("数据84坐标：" + str_geom)
    # 导出excel
    # result = {"标识ID": '', "数据类型": '', "地市分公司": '', "区县": '', '目标名称': '', '类型': '', '百度坐标': '', 'w84坐标': ''}
    # df = pd.DataFrame.from_dict(result)
    # df.to_excel("G://百度信息点.xlsx")


if __name__ == '__main__':
    main()
