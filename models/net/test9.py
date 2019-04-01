# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/2/25 10:16
# Description:  
# -------------------------------------------------------------------------------
import math

import pymysql
import json
from urllib.request import urlopen
import time
from urllib import request


def urls(itemy, loc):
    baidu_api = ['8ZHsSKtmEsNYMMGRneDGtle7Ognd2W5e',
                 'SqLUYy6nyGIrRzo2p3NoZ06d9G8F6Zmq',
                 '0gTtWeiV3BxSG9CFsW8qhSPnVjXDH6Dl',
                 '1daHSdZTRcUKocGae0Q1uX6e3PjatSSB',
                 'mycEE9PyvCo8aFLFnocPp2POYgacuAAP',
                 '7sFH4KOza31IUjeGM3o1b3aO',
                 'Dydtlpvoidza3BFGClf65ulPcDMHnEaN',
                 'x39uxyAjOnzyWx2sXzPPiHPLHAzcanCO',
                 'aj2dDcCWbzWTeHkM1X1yaGF9e1nBCLMu',
                 'WnM8BMNT1lcHKSPcnGY4vibgGr7BR32H'
                 ]
    urls = []
    for page in range(0, 20):
        range_i = math.ceil(float(page - 1) / 2)
        url = "http://api.map.baidu.com/place/v2/search?query=" + request.quote(itemy) + "&bounds=" + loc
        url = url + "&page_size=20&page_num=" + str(page) + "&output=json&ak=" + baidu_api[range_i]
        urls.append(url)
    return urls


def connect_mysql(host, dbname, password, port, username):
    client = pymysql.Connect(host=host, port=port, user=username, passwd=password, db=dbname, charset='utf8')
    return client


def commit_sql(client, lis):
    cursor = client.cursor()
    sql = 'insert into topl_baidu(name,address,telephone,location) VALUES (%s,%s,%s,%s)'
    cursor.execute(sql, lis)
    # 提交sql语句
    client.commit()


def baidu_search(urls, client):
    try:
        i = 0
        for url in urls:
            i = i + 1
            time.sleep(1)
            req = request.Request(url)
            json_obj = urlopen(req)
            data = json.load(json_obj)
            if data['status'] != 0:
                print(url)
                break
            results = data['results']
            if len(results) == 0:
                print('一共请求百度接口:' + str(i) + '次')
                break
            for item in data['results']:
                json_sel = []
                jname = item["name"]
                jlat = str(item["location"]["lat"]) + ',' + str(item["location"]["lng"])
                if "telephone" in item:
                    jtel = item["telephone"].replace(',', ' ')
                else:
                    jtel = ''
                j_addr = item['province']
                j_addr = j_addr + ' ' + item['city']
                j_addr = j_addr + ' ' + item['area']
                j_addr = j_addr + ' ' + item['address']
                json_sel.append(jname)
                json_sel.append(j_addr)
                json_sel.append(jtel)
                json_sel.append(jlat)
                commit_sql(client, json_sel)
        # 关闭资源
        cursor = client.cursor()
        cursor.close()
        client.close()
    except Exception as e:
        print(e)
        pass


def lat_all(loc_all):
    a = loc_all.split(',')
    lat_sw = float(loc_all.split(',')[0])
    lat_ne = float(loc_all.split(',')[2])
    lat_list = []

    for i in range(0, int((lat_ne - lat_sw) / 0.01)):  # 网格大小，可根据区域内POI数目修改
        lat_list.append(lat_sw + 0.01 * i)
    lat_list.append(lat_ne)

    return lat_list


def lng_all(loc_all):
    lng_sw = float(loc_all.split(',')[1])
    lng_ne = float(loc_all.split(',')[3])
    lng_list = []
    for i in range(0, int((lng_ne - lng_sw) / 0.01)):
        lng_list.append(lng_sw + 0.01 * i)
    lng_list.append(lng_ne)

    return lng_list


def ls_com(loc_all):
    l1 = lat_all(loc_all)
    l2 = lng_all(loc_all)
    ab_list = []
    for i1 in range(0, len(l1)):
        a = str(l1[i1])
        for i2 in range(0, len(l2)):
            b = str(l2[i2])
            ab = a + ',' + b
            ab_list.append(ab)
    return ab_list


def ls_row(loc_all):
    l1 = lat_all(loc_all)
    l2 = lng_all(loc_all)
    ls_com_v = ls_com(loc_all)
    ls = []
    for n in range(0, len(l1) - 1):
        for i in range(0 + len(l1) * n, len(l2) + (len(l2)) * n - 1):
            a = ls_com_v[i]
            b = ls_com_v[i + len(l2) + 1]
            ab = a + ',' + b
            ab_list = ab.split(',')
            if (ab_list[0] < ab_list[2] and ab_list[1] < ab_list[3]):
                ls.append(ab)

    return ls


# 获取网格点
def get_net(client):
    cursor = client.cursor()
    sql = 'select * from topl_baidu_net'
    execute = cursor.execute(sql)
    # 提交sql语句
    client.commit()
    return execute


if __name__ == '__main__':
    print("开始爬取数据，请稍等...")
    client = connect_mysql('132.121.152.60', 'tpoc', 'Ab123456', 33068, 'tpoc')
    start_time = time.time()
    #net = get_net(client)
    loc = '23.137131,113.378211,23.148048,113.393875'
    locs_to_use = ls_row(loc)
    for loc_to_use in locs_to_use:
        par = urls(u'饭店', loc_to_use)
        baidu_search(par, client)
    end_time = time.time()
    print("爬取完毕，用时%.2f秒" % (end_time - start_time))

# 23.137131,113.378211,23.148048,113.393875
# 23.137131,113.378211,23.148048,113.393875
