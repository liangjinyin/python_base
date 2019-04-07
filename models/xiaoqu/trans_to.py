# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/4/1 14:03
# Description:  百度坐标转为84
# -------------------------------------------------------------------------------
import math


class community_info(object):

    @staticmethod
    def trans_form_lon(x, y, pi):
        ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(math.fabs(x))
        ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(x * pi) + 40.0 * math.sin(x / 3.0 * pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(x / 12.0 * pi) + 300.0 * math.sin(x / 30.0 * pi)) * 2.0 / 3.0
        return ret

    @staticmethod
    def trans_form_lat(x, y, pi):
        ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(math.fabs(x))
        ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(y * pi) + 40.0 * math.sin(y / 3.0 * pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(y / 12.0 * pi) + 320 * math.sin(y * pi / 30.0)) * 2.0 / 3.0
        return ret

    @staticmethod
    def hx_to_84(lon, lat):
        pi = 3.1415926535897932384626
        a = 6378245.0
        ee = 0.00669342162296594323
        dLat = community_info.trans_form_lat(lon - 105.0, lat - 35.0, pi)

        dLon = community_info.trans_form_lon(lon - 105.0, lat - 35.0, pi)

        radLat = lat / 180.0 * pi

        magic = math.sin(radLat)
        magic = 1 - ee * magic * magic

        sqrtMagic = math.sqrt(magic)
        dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * pi)
        dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * pi)
        mgLat = lat + dLat
        mgLon = lon + dLon
        list_84 = str(mgLon) + ',' + str(mgLat)
        return list_84

    @staticmethod
    def bd_to_hx(ba_lon, ba_lat):
        pi = 3.1415926535897932384626
        x = float(ba_lon) - 0.0065
        y = float(ba_lat) - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * pi)
        gg_lon = z * math.cos(theta)
        gg_lat = z * math.sin(theta)
        list_hx = []
        list_hx.append(gg_lon)
        list_hx.append(gg_lat)
        return list_hx

    @staticmethod
    def bd_to_84(geom_temp):
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
        return str_geom

    @staticmethod
    def bd_to_841(geom_temp):
        hx_list = community_info.bd_to_hx(geom_temp[0], geom_temp[1])
        str_geom = community_info.hx_to_84(hx_list[0], hx_list[1])
        print("数据84坐标：" + str_geom)
        return str_geom
