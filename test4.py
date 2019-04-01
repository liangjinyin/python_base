# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/2/14 16:47
# Description:  
# -------------------------------------------------------------------------------
import json
import time

import psycopg2
import requests

## 连接到一个给定的数据库
conn = psycopg2.connect(database="spaDB", user="postgres",
                        password="postgres", host="132.97.8.62", port="5432")
## 建立游标，用来执行数据库操作
cursor = conn.cursor()

## 执行SQL SELECT命令
cursor.execute("select geom, st_AsGeoJSON(geom),org_id from guangdong_sj_baidu ")

## 获取SELECT返回的元组
rows = cursor.fetchall()
for row in rows:
    # 重构 用正则表达式
    data = json.loads(row[1])
    point = data["coordinates"]
    g_id = str(row[2])
    temp = []
    time.sleep(1)
    for list in point[0][0]:
        # print(list)
        a = list[0]
        b = list[1]
        url = 'http://api.map.baidu.com/geoconv/v1/?coords=%s,%s&from=1&to=5&ak=1daHSdZTRcUKocGae0Q1uX6e3PjatSSB' % (
        a, b)
        data1 = json.loads(requests.get(url).text)
        cc = data1['result']
        cc = cc[0]
        x = cc['x']
        y = cc['y']
        d = []
        d.append(x)
        d.append(y)
        temp.append(d)
    t = []
    p = []
    t.append(temp)
    p.append(t)
    b_point = {"type": "MultiPolygon", "coordinates": p}
    ll = str(b_point)
    ll = ll.replace("'" , "\"")

    psql = "update guangdong_sj_baidu set geom_baidu ='" +ll + "'where org_id = "+g_id
    cursor.execute(psql)
    # 提交SQL命令
    conn.commit()

# 关闭游标
cursor.close()

# 关闭数据库连接
conn.close()
