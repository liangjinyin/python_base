# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/2/14 16:47
# Description:  
# -------------------------------------------------------------------------------
import json
import math

import psycopg2
import requests
import re


# 封装正则表达式接口
def my_pattern(str_pattern, pattern_data):
    regex = re.compile(str_pattern)
    findall = regex.findall(pattern_data)
    return findall


# 从百度地图获取转换坐标的数据 select stname,ST_AsGeoJSON(geom),gid,geom_baidu from prj_yzf_sector_baidu where gid>32425 and geom_baidu is not null order by gid desc
def my_shuju(sum, d):
    try:
        url = 'http://api.map.baidu.com/geoconv/v1/?coords=%s&from=1&to=5&ak=1daHSdZTRcUKocGae0Q1uX6e3PjatSSB' % sum
        data1 = json.loads(requests.get(url).text)
        if data1['status'] != 0:
            return []
        cc = data1['result']
        for u in range(len(cc)):
            f = []
            pp = cc[u]
            x = pp['x']
            y = pp['y']
            f.append(x)
            f.append(y)
            d.append(f)
    except TimeoutError as e:
        print(e)
    return d


# 封装指定的面数据格式
def my_shujubaozhuan(d):
    temp = []
    temp.append(d)
    t = []
    t.append(temp)
    b_point = {"type": "MultiPolygon", "coordinates": t, "crs": {"type": "name", "properties": {"name": "EPSG:4326"}}}
    ll = str(b_point)
    ll = ll.replace("'", "\"")
    return ll


## 连接到一个给定的数据库
conn = psycopg2.connect(database="spaDB", user="postgres",
                        password="postgres", host="132.97.8.62", port="5432")
## 建立游标，用来执行数据库操作
cursor = conn.cursor()

## 执行SQL SELECT命令
cursor.execute("select stname,ST_AsGeoJSON(geom),gid from prj_yzf_sector where gid>62675")

## 获取SELECT返回的元组
rows = cursor.fetchall()
for row in rows:
    #  用正则表达式取数据
    data_srt = row[1]
    g_id = str(row[2])
    str_pattern = "\[\[\[(.*)\]\]\]"
    pattern1 = my_pattern(str_pattern, data_srt)

    findall_list = pattern1[0]
    str_pattern1 = "\[(.*?)\]"
    pattern2 = my_pattern(str_pattern1, findall_list)
    sum = ''
    d = []
    len_data = len(pattern2)
    if len_data < 100:
        sum = ";".join(pattern2)
        # 数据处理
        d = my_shuju(sum, d)
    else:
        mun_count = math.ceil(float(len_data) / 100)
        for i in range(mun_count):
            if i * 100 + 100 > len_data:
                sum = ";".join(pattern2[i * 100: len_data])
            else:
                sum = ";".join(pattern2[i * 100: i * 100 + 100])
            d = my_shuju(sum, d)
    # 数据包装
    if len(d) == 0:
        aaa = 0
    else:
        ll = my_shujubaozhuan(d)
        psql = "update prj_yzf_sector_baidu set geom_baidu =st_geomfromgeojson('" + ll + "')where gid = " + g_id
        cursor.execute(psql)
        # 提交SQL命令
        conn.commit()

## 关闭游标
cursor.close()

## 关闭数据库连接
conn.close()

'''
"coordinates":[[[  ]]]}
'''
