# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/2/25 10:16
# Description:  
# -------------------------------------------------------------------------------
import math

import pymysql
import json
import time
from urllib import request

import requests


def urls(itemy, loc):
    baidu_api = ['WnM8BMNT1lcHKSPcnGY4vibgGr7BR32H',
                 'SqLUYy6nyGIrRzo2p3NoZ06d9G8F6Zmq',
                 'x39uxyAjOnzyWx2sXzPPiHPLHAzcanCO',
                 '0gTtWeiV3BxSG9CFsW8qhSPnVjXDH6Dl',
                 '8ZHsSKtmEsNYMMGRneDGtle7Ognd2W5e',
                 'mycEE9PyvCo8aFLFnocPp2POYgacuAAP',
                 '1daHSdZTRcUKocGae0Q1uX6e3PjatSSB',
                 'Dydtlpvoidza3BFGClf65ulPcDMHnEaN',
                 '7sFH4KOza31IUjeGM3o1b3aO',
                 'aj2dDcCWbzWTeHkM1X1yaGF9e1nBCLMu'
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


def commit_sql(lis):
    # client = connect_mysql('132.121.152.60', 'tpoc', 'Ab123456', 33068, 'tpoc')
    client = connect_mysql('132.121.152.60', 'tpoc', 'Ab123456', 33068, 'tpoc')
    cursor = client.cursor()
    sql = 'insert into topl_baidu(name,address,telephone,location,uid) VALUES (%s,%s,%s,%s,%s)'
    cursor.execute(sql, lis)
    # 提交sql语句
    client.commit()
    return client


def ananyse_data(data):
    try:
        for item in data:
            json_sel = []
            jname = item["name"]
            jlat = str(item["location"]["lat"]) + ',' + str(item["location"]["lng"])
            juid = item['uid']
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
            json_sel.append(juid)
            client = commit_sql(json_sel)
    except Exception as e:
        print(e)
        pass
    return client


def baidu_search(point, ak, zt_ak_list, sx_ak_list):
    try:
        time.sleep(0.5)
        url = 'http://api.map.baidu.com/place/v2/search?query=%E9%93%B6%E8%A1%8C&bounds=' + point \
              + '&page_size=20&page_num=1&output=json&ak=' + ak
        data = json.loads(requests.get(url).text)

        if data['status'] != 0:
            print('url 状态码不符合！')
            zt_ak_list.append(point)
        results = data['results']
        if len(results) == 0:
            print('url 没有返回值！')
        if data['total'] > 40:
            print('url 返回值达到上限！')
            sx_ak_list.append(point)
        client = ananyse_data(results)
        # 关闭资源
        cursor = client.cursor()
        cursor.close()
        client.close()
    except Exception as e:
        print(e)
        pass


def my_main(point_list):
    print("开始爬取数据，请稍等...")
    zt_ak_list = []
    sx_ak_list = []
    start_time = time.time()
    baidu_api = ['WnM8BMNT1lcHKSPcnGY4vibgGr7BR32H',
                 'SqLUYy6nyGIrRzo2p3NoZ06d9G8F6Zmq',
                 '0gTtWeiV3BxSG9CFsW8qhSPnVjXDH6Dl',
                 '1daHSdZTRcUKocGae0Q1uX6e3PjatSSB',
                 'mycEE9PyvCo8aFLFnocPp2POYgacuAAP',
                 '7sFH4KOza31IUjeGM3o1b3aO',
                 'Dydtlpvoidza3BFGClf65ulPcDMHnEaN',
                 'x39uxyAjOnzyWx2sXzPPiHPLHAzcanCO',
                 '8ZHsSKtmEsNYMMGRneDGtle7Ognd2W5e',
                 'aj2dDcCWbzWTeHkM1X1yaGF9e1nBCLMu'
                 ]
    i = 10
    for net_point in point_list:
        i += 1
        range_i = i % 10
        print(net_point[0])
        # par = urls(u'银行', net_point[1])
        baidu_search(net_point[1], baidu_api[range_i], zt_ak_list, sx_ak_list)
    end_time = time.time()
    print("爬取完毕，用时%.2f秒" % (end_time - start_time))
    print('=========================================================================================')
    print('                       状态码不对点有' + str(len(zt_ak_list)) + '条')
    print(str(zt_ak_list))
    print('=========================================================================================')
    print('=========================================================================================')
    print('                       上限的点有' + str(len(sx_ak_list)) + '条')
    print(str(sx_ak_list))
    print('=========================================================================================')
