# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/2/27 14:47
# Description:  爬取医院数据
# -------------------------------------------------------------------------------
import json
import time

import pymysql
import requests
from models.net.mk_to_bd import MKTOBD


def connect_mysql(host, dbname, password, port, username):
    client = pymysql.Connect(host=host, port=port, user=username, passwd=password, db=dbname, charset='utf8')
    return client


def anasisy_data(contents, client, cid):
    sql = 'insert into topl_baidu_hospital_temp(uid,name,address,telephone,location,data_type,area_name,city_code,std_tag) ' \
          'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor = client.cursor()
    for content in contents:
        data_list = []
        xy = MKTOBD.mcat(content['x'] / 100, content['y'] / 100)
        data_list.append(content['uid'])
        data_list.append(content['name'])
        data_list.append(content['addr'])
        if 'tel' in content:
            data_list.append(content['tel'])
        else:
            data_list.append('')
        data_list.append(xy)
        data_list.append(8)  # 4 投资理财，1 银行 ,2 ATM 8医院
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


'''
工商银行, 建设银行, 农业银行, 中国银行,招商银行,交通银行,邮政储蓄,农村信用社,
中信银行,民生银行,光大银行,广发银行,北京银行,浦发银行,平安银行,兴业银行
https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=spot&from=webmap&c=201&wd=%E5%8C%BB%E9%99%A2&wd2=&pn=0&nn=0&rn=50
'''


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


def baidu_sreach_one(page, client, cid):
    try:
        url_bank = 'https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1' \
                   '&qt=spot&from=webmap&c=' + str(cid) + '&wd= 医院 &wd2=&pn=0&nn=' + str(page * 50) + '&rn=50'
        data = json.loads(requests.get(url_bank).text)
        if 'content' not in data:
            print('一共爬取 ' + str(page * 50) + ' 条数据！')
            return
        contents = data['content']
        anasisy_data(contents, client, cid)
    except Exception as e:
        print(e)
        pass


def main():
    try:
        cid = 340
        client = connect_mysql('127.0.0.1', 'bishe', '123', 3306, 'root')
        print("开始爬取数据，请稍等...")
        start_time = time.time()
        hotel_list = ['综合医院', '中医院', '妇幼保健院', '儿童医院', '口腔医院', '骨科医院', '诊所', '眼科医院', '妇科医院', '肿瘤医院']
        for j in range(len(hotel_list)):
            i = 0
            flag = True
            while (flag):
                flag = baidu_sreach(hotel_list[j], i, client, cid)
                i += 1
        for k in range(8):
            baidu_sreach_one(k, client, cid)
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
