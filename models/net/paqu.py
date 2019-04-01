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
                 '0gTtWeiV3BxSG9CFsW8qhSPnVjXDH6Dl',
                 '1daHSdZTRcUKocGae0Q1uX6e3PjatSSB',
                 'mycEE9PyvCo8aFLFnocPp2POYgacuAAP',
                 '7sFH4KOza31IUjeGM3o1b3aO',
                 'Dydtlpvoidza3BFGClf65ulPcDMHnEaN',
                 'x39uxyAjOnzyWx2sXzPPiHPLHAzcanCO',
                 '8ZHsSKtmEsNYMMGRneDGtle7Ognd2W5e',
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
    sql = 'insert into topl_baidu(name,address,telephone,location,uid,data_type) VALUES (%s,%s,%s,%s,%s,%s)'
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
            json_sel.append(4)
            client = commit_sql(json_sel)
    except Exception as e:
        print(e)
        pass
    return client


def baidu_search(point, ak, num):
    try:
        time.sleep(0.5)
        url = 'http://api.map.baidu.com/place/v2/search?query=' + '投资理财' + '&bounds=' + point \
              + '&page_size=20&page_num=' + str(num) + '&output=json&ak=' + ak
        data = json.loads(requests.get(url).text)
        total = data['total']
        if data['status'] != 0:
            print('url 状态码不符合！')
            zt_ak_list.append(point)
        results = data['results']
        if len(results) == 0:
            print('url 没有返回值！')
            wf_ak_list.append(point)
        if total > 20 and total < 40 and len(results) == 20:
            print('url 返回值达到上限20！')
            digui(point, 1)
        if total > 40 and total < 60 and len(results) == 20:
            print('url 返回值达到上限40！')
            sx_ak_list.append(point)
            digui(point, 2)
        if total > 60 and total < 80 and len(results) == 20:
            print('url 返回值达到上限60！')
            digui(point, 3)
        client = ananyse_data(results)
        # 关闭资源
        cursor = client.cursor()
        cursor.close()
        client.close()
    except Exception as e:
        print(e)
        pass


# 获取网格点
def get_net(client):
    cursor = client.cursor()
    sql = 'select id,baidu_net from topl_baidu_net_temp'
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


def digui(point, num):
    baidu_api_tmp = '7sFH4KOza31IUjeGM3o1b3aO'
    # par = urls(u'银行', net_point[1])
    baidu_search(point, baidu_api_tmp, num)


if __name__ == '__main__':
    print("开始爬取数据，请稍等...")
    zt_ak_list = []
    wf_ak_list = []
    sx_ak_list = []
    client = connect_mysql('132.121.152.60', 'tpoc', 'Ab123456', 33068, 'tpoc')
    start_time = time.time()
    net = get_net(client)
    baidu_api = ['pyzp608kChxWYS7esmYlmwO0',
                 'SqLUYy6nyGIrRzo2p3NoZ06d9G8F6Zmq',
                 '0gTtWeiV3BxSG9CFsW8qhSPnVjXDH6Dl',
                 'mycEE9PyvCo8aFLFnocPp2POYgacuAAP',
                 '7sFH4KOza31IUjeGM3o1b3aO',
                 '8ZHsSKtmEsNYMMGRneDGtle7Ognd2W5e',
                 '81BoGwGahjHHwUv11wq9uFot5RTNx5G3',
                 '1daHSdZTRcUKocGae0Q1uX6e3PjatSSB',
                 'Dydtlpvoidza3BFGClf65ulPcDMHnEaN',
                 'x39uxyAjOnzyWx2sXzPPiHPLHAzcanCO'
                 ]
    '''
    # lad = '22.788083,113.539061,22.805653,113.561905'
    lad = '22.698161,113.539083,22.715729,113.561919'
    baidu_search(lad, 'aj2dDcCWbzWTeHkM1X1yaGF9e1nBCLMu', 0)
    '''
    i = 10
    for net_point in net:
        i += 1
        range_i = i % 10
        print(net_point[0])
        baidu_search(net_point[1], baidu_api[range_i], 0)

    end_time = time.time()
    print("爬取完毕，用时%.2f秒" % (end_time - start_time))
    print('=========================================================================================')
    print('                       没有返回值的点有' + str(len(wf_ak_list)) + '条')
    print('=========================================================================================')
    print('=========================================================================================')
    print('                       状态码不对点有' + str(len(zt_ak_list)) + '条')
    print(str(zt_ak_list))
    print('=========================================================================================')
    print('=========================================================================================')
    print('                       上限的点有' + str(len(sx_ak_list)) + '条')
    print(str(sx_ak_list))
    print('=========================================================================================')
