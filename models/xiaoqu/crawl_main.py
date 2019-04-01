# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/4/1 15:35
# Description:  小区爬取主类
# -------------------------------------------------------------------------------

from models.xiaoqu.trans_to import community_info
from models.xiaoqu.crawl_community import CrawlCommunity
from models.xiaoqu.minqu import Converter


def main():
    # 爬取小区数据
    uid = CrawlCommunity.get_community('和平新村')
    geo = CrawlCommunity.crawl(uid)
    # 将小区的摩卡坐标换为百度坐标
    geom_temp = Converter.my_geom(geo)
    # 将百度坐标换为84坐标
    temp_split = geom_temp.split(';')
    str_geom = ''
    for coordinates in temp_split:
        split = coordinates.split(',')
        hx_list = community_info.bd_to_hx(split[0], split[1])
        list_84 = community_info.hx_to_84(hx_list[0], hx_list[1])
        str_geom = str_geom + list_84
        if len(str_geom) != 0:
            str_geom = str_geom + ';'
    print(str_geom)


if __name__ == '__main__':
    main()
