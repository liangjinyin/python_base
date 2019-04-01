# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/2/14 16:47
# Description:  Args 坐标转换为百度坐标
# -------------------------------------------------------------------------------
import json
import math

import pymysql
import requests

# 连接到一个给定的数据库
conn = pymysql.Connect(host='132.121.152.60', port=33068, user='tpoc', passwd='Ab123456', db='tpoc', charset='utf8')
# 建立游标，用来执行数据库操作
cursor = conn.cursor()
# 执行SQL SELECT命令
cursor.execute("select count(id) mun_count from topl_baidu_net_temp  ")
mun_count = cursor.fetchall()[0][0]
mun_count = math.ceil(float(mun_count) / 50)
xy_i = 1
id_i = 0
for i in range(mun_count):
    # 执行SQL SELECT命令
    cursor.execute(
        "select EXT_MIN_X x1,',',EXT_MIN_Y y1,';' r,EXT_MAX_X x2,',',EXT_MAX_Y y2  from topl_baidu_net_temp  limit " + str(
            i * 50) + ",50")

    # 获取SELECT返回的元组
    rows = cursor.fetchall()
    sum = ''
    for r in rows:
        sum = sum + "".join(r) + ";"
    sum = sum[:-1]
    url = 'http://api.map.baidu.com/geoconv/v1/?coords=%s&from=1&to=5&ak=1daHSdZTRcUKocGae0Q1uX6e3PjatSSB' % sum
    data1 = json.loads(requests.get(url).text)
    cc = data1['result']
    xy = ''
    for u in range(len(cc)):
        xy_i = xy_i + 1
        pp = cc[u]
        x = str(round(pp['x'], 6))
        y = str(round(pp['y'], 6))
        xy = xy + y + ',' + x + ','
        if xy_i % 2 == 0:
            continue
        id_i = id_i + 1
        xy = xy[:-1]
        psql = "update topl_baidu_net_temp set baidu_net =\'" + xy + "\' where id = " + str(id_i)
        cursor.execute(psql)
        # 提交SQL命令
        conn.commit()
        xy = ''
# 关闭游标
cursor.close()

# 关闭数据库连接
conn.close()
'''
"{"type":"Point","coordinates":[114.925739,24.4537051]}"
"0101000020E6100000A8085F4E3FBB5C4010A1200426743840"
'''
