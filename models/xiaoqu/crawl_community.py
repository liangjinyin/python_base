# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/4/1 14:42
# Description:  爬取小区数据
# -------------------------------------------------------------------------------
import json
from models.xiaoqu.trans_to import community_info
from models.xiaoqu.minqu import Converter
import requests


class CrawlCommunity(object):

    @staticmethod
    def get_community(name, sub):
        url_community = 'https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=' + name + '&c=140'
        data = json.loads(requests.get(url_community).text)
        if 'content' not in data:
            return None
        content = data['content']
        response_data = content[0]
        # if 'admin_info' in response_data:
        #     admin_info = response_data['admin_info']
        #     area_name = admin_info['area_name']
        #     area_name = area_name[0:-1]
        #     if area_name != sub:
        #         return None
        uid = response_data['uid']
        return uid

    @staticmethod
    def crawl(uid):
        data_list = []
        show_tag = ''
        url_comm = 'https://map.baidu.com/?ugc_type=3&ugc_ver=1&qt=detailConInfo&device_ratio=2&compat=1&t=1554100284590&uid=' + uid
        data = json.loads(requests.get(url_comm).text)
        if 'content' not in data:
            return None
        content = data['content']
        if 'showtag' in content:
            show_tag = content['showtag']
        if 'x' not in content:
            return None
        x = content['x']
        y = content['y']
        ext = content['ext']
        if ('ext' not in content) | (ext is None):
            return None
        detail_info = ext['detail_info']
        data_list.append(show_tag)
        if 'guoke_geo' not in detail_info:
            data_list.append(x)
            data_list.append(y)
        else:
            geo_info = detail_info['guoke_geo']
            geo = geo_info['geo']
            data_list.append(geo)
        # print(address + name + geo)
        return data_list

    @staticmethod
    def data_trans(excel_list):
        data_id_list = []
        show_tag_list = []
        data_city_list = []
        data_sub_list = []
        data_name_list = []
        geom_temp_list = []
        str_geom_list = []
        message_list = []
        for data_temp in excel_list:
            # 爬取小区数据
            message = ''
            show_tag = ''
            uid = CrawlCommunity.get_community(data_temp['name'], data_temp['sub'])
            if uid is None:
                geom_temp = None
                str_geom = None
                message = '百度搜索不到，数据为空！'
            else:
                data_list = CrawlCommunity.crawl(uid)
                # 将小区的摩卡坐标换为百度坐标
                if data_list is None:
                    geom_temp = None
                    str_geom = None
                    message = '百度搜索不到，数据为空！'
                elif len(data_list) == 2:
                    geom_temp = Converter.my_geom(data_list[1])
                    # 将百度坐标换为w84坐标
                    str_geom = community_info.bd_to_84(geom_temp)
                    show_tag = data_list[0]
                else:
                    geom_temp = Converter.mcat(data_list[1], data_list[2])
                    str_geom = community_info.bd_to_841(geom_temp)
                    show_tag = data_list[0]
            data_id_list.append(data_temp['build_id'])
            data_city_list.append(data_temp['city'])
            show_tag_list.append(show_tag)
            geom_temp_list.append(geom_temp)
            message_list.append(message)
            str_geom_list.append(str_geom)
            data_name_list.append(data_temp['name'])
            data_sub_list.append(data_temp['sub'])
        result = {"标识ID": data_id_list, "数据类型": show_tag_list, "地市分公司": data_city_list,
                  "区县": data_sub_list, '目标名称': data_name_list, '类型': '1', '百度坐标': geom_temp_list,
                  'w84坐标': str_geom_list, '备注': message_list}
        return result
