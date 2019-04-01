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
    client = connect_mysql('132.121.152.60', 'tpoc', 'Ab123456', 33068, 'tpoc')
    cursor = client.cursor()
    sql = 'insert into topl_baidu(name,address,telephone,location,uid) VALUES (%s,%s,%s,%s,%s)'
    cursor.execute(sql, lis)
    # 提交sql语句
    client.commit()


def ananyse_data(data, client):
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
            commit_sql(json_sel)
    except Exception as e:
        print(e)
        pass


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
                print('url 没有返回值')
                print(url)
                break
            if len(results) == 400:
                print('url 返回值达到上限')
                print(url)
            ananyse_data(results, client)
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
    sql = 'select id,baidu_net from topl_baidu_net'
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


if __name__ == '__main__':
    print("开始爬取数据，请稍等...")
    client = connect_mysql('132.121.152.60', 'tpoc', 'Ab123456', 33068, 'tpoc')
    start_time = time.time()
    net = get_net(client)
    # lad = '113.59611883659248,22.589593465112465,113.60749299988076,22.598724201175674'
    # par = urls(u'银行', lad)
    for net_point in net:
        print(net_point[0])
        par = urls(u'银行', net_point[1])
        baidu_search(par, client)
    end_time = time.time()
    print("爬取完毕，用时%.2f秒" % (end_time - start_time))

