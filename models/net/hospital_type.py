# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/2/27 14:47
# Description:  
# -------------------------------------------------------------------------------
import json
import time

import pymysql
import requests
from models.xiaoqu.minqu import Converter


def connect_mysql(host, dbname, password, port, username):
    client = pymysql.Connect(host=host, port=port, user=username, passwd=password, db=dbname, charset='utf8')
    return client

def anasisy_data(contents, client, cid):
    sql = 'insert into topl_baidu_temp(uid,name,address,telephone,location,data_type,area_name,city_code,std_tag) ' \
          'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor = client.cursor()
    for content in contents:
        data_list = []
        xy = Converter.mcat(content['x'] / 100, content['y'] / 100)
        data_list.append(content['uid'])
        data_list.append(content['name'])
        data_list.append(content['addr'])
        if 'tel' in content:
            data_list.append(content['tel'])
        else:
            data_list.append('')
        data_list.append(xy)
        data_list.append(1)  # 4 投资理财，1 银行 ,2 ATM
        data_list.append(content['area_name'])
        data_list.append(cid)  # tag std_tag di_tag
        if 'std_tag' in content:
            di_tag = content['std_tag']
        elif 'di_tag' in content:
            di_tag = content['di_tag']
        else:
            di_tag = content['tag']
        data_list.append(di_tag)
        cursor.execute(sql, data_list)
        # 提交sql语句
        client.commit()


def baidu_sreach(key, page, client, cid):
    try:
        url_bank = 'https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1' \
                   '&qt=spot&from=webmap&c=' + str(cid) + '&wd= ' + key + '&wd2=&pn=0&nn=' + str(page * 50) + '&rn=50'
        data = json.loads(requests.get(url_bank).text)
        if 'content' not in data:
            print('一共爬取 ' + key + str(page * 50) + ' 条数据！')
            return False
        contents = data['content']
        anasisy_data(contents, client, cid)
        return True
    except Exception as e:
        print(e)
        pass


def main():
    try:
        client = connect_mysql('127.0.0.1', 'bishe', '123', 3306, 'root')
        print("开始爬取数据，请稍等...")
        start_time = time.time()
        area_list = ['越秀区', '天河区', '海珠区', '荔湾区', '白云区', '番禺区']
        hotel_list = ['综合医院', '中医院', '妇幼保健院', '儿童医院', '口腔医院', '骨科医院', '诊所', '眼科医院', '妇科医院', '肿瘤医院']
        for j in range(len(hotel_list)):
            i = 0
            flag = True
            while (flag):
                flag = baidu_sreach(hotel_list[j], i, client)
                i += 1
        # 关闭资源
        cursor = client.cursor()
        cursor.close()
        client.close()
        end_time = time.time()
        print("爬取完毕，用时%.2f秒" % (end_time - start_time))
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    main()
