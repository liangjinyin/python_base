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

# 连接到一个给定的数据库
conn = psycopg2.connect(database="spaDB", user="postgres",
                        password="postgres", host="132.97.8.62", port="5432")
# 建立游标，用来执行数据库操作
cursor = conn.cursor()
# 执行SQL SELECT命令
cursor.execute("select count(gid) mun_count from prj_yzf_station  ")
mun_count = cursor.fetchall()[0][0]
mun_count = math.ceil(float(mun_count) / 100)
for i in range(mun_count):
    if i == 0:
        end_i = i
    elif i != 0:
        end_i = 100 * i + 1
    # 执行SQL SELECT命令
    cursor.execute("select area_name,ST_AsGeoJSON(geom),gid from prj_yzf_station  limit 100 offset "+str(end_i))

    # 获取SELECT返回的元组
    rows = cursor.fetchall()
    sum = ''
    gid_list = []
    for row in rows:
        # print( 'id = ',row[0], 'map = ', row[1], '\n')
        g_id = row[2]
        gid_list.append(g_id)
        # 重构 用正则表达式
        data = json.loads(row[1])
        point = data["coordinates"]
        temp = []
        str_list = map(str, point)
        i = ",".join(str_list)
        sum = sum + i + ";"
    sum = sum[:-1]
    url = 'http://api.map.baidu.com/geoconv/v1/?coords=%s&from=1&to=5&ak=1daHSdZTRcUKocGae0Q1uX6e3PjatSSB' % sum
    data1 = json.loads(requests.get(url).text)
    cc = data1['result']
    for u in range(len(cc)):
        pp = cc[u]
        x = pp['x']
        y = pp['y']
        d = []
        d.append(x)
        d.append(y)
        b_point = {"type": "Point", "coordinates": d}
        ll = str(b_point)
        ll = ll.replace("'", "\"")
        psql = "update prj_yzf_station_baidu set geom_baidu = st_geomfromgeojson('" + ll + "')where gid = " + str(gid_list[u])
        cursor.execute(psql)
        # 提交SQL命令
        conn.commit()

# 关闭游标
cursor.close()

# 关闭数据库连接
conn.close()
'''
"{"type":"Point","coordinates":[114.925739,24.4537051]}"
"0101000020E6100000A8085F4E3FBB5C4010A1200426743840"
'''
