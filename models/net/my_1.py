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


def converter(x, y, cE):
    xTemp = cE[0] + cE[1] * abs(x)
    cC = abs(y) / cE[9]
    yTemp = cE[2] + cE[3] * cC + cE[4] * cC * cC + cE[5] * cC * cC * cC + cE[6] * cC * cC * cC * cC + \
            cE[7] * cC * cC * cC * cC * cC + cE[8] * cC * cC * cC * cC * cC * cC
    if x < 0:
        xTemp = -xTemp
    if y < 0:
        yTemp = -yTemp
    location = str(xTemp) + ',' + str(yTemp)
    return location


def mcat(x, y):
    MCBAND = [12890594.86, 8362377.87, 5591021, 3481989.83, 1678043.12, 0]
    LLBAND = [75, 60, 45, 30, 15, 0]
    MC2LL = [[1.410526172116255e-8, 0.00000898305509648872, -1.9939833816331, 200.9824383106796, -187.2403703815547,
              91.6087516669843, -23.38765649603339, 2.57121317296198, -0.03801003308653, 17337981.2],
             [-7.435856389565537e-9, 0.000008983055097726239, -0.78625201886289, 96.32687599759846, -1.85204757529826,
              -59.36935905485877, 47.40033549296737, -16.50741931063887, 2.28786674699375, 10260144.86],
             [-3.030883460898826e-8, 0.00000898305509983578, 0.30071316287616, 59.74293618442277, 7.357984074871,
              -25.38371002664745, 13.45380521110908, -3.29883767235584, 0.32710905363475, 6856817.37],
             [-1.981981304930552e-8, 0.000008983055099779535, 0.03278182852591, 40.31678527705744, 0.65659298677277,
              -4.44255534477492, 0.85341911805263, 0.12923347998204, -0.04625736007561, 4482777.06],
             [3.09191371068437e-9, 0.000008983055096812155, 0.00006995724062, 23.10934304144901, -0.00023663490511,
              -0.6321817810242, -0.00663494467273, 0.03430082397953, -0.00466043876332, 2555164.4],
             [2.890871144776878e-9, 0.000008983055095805407, -3.068298e-8, 7.47137025468032, -0.00000353937994,
              -0.02145144861037, -0.00001234426596, 0.00010322952773, -0.00000323890364, 826088.5]]
    LL2MC = [[-0.0015702102444, 111320.7020616939, 1704480524535203, -10338987376042340, 26112667856603880,
              -35149669176653700, 26595700718403920, -10725012454188240, 1800819912950474, 82.5],
             [0.0008277824516172526, 111320.7020463578, 647795574.6671607, -4082003173.641316, 10774905663.51142,
              -15171875531.51559, 12053065338.62167, -5124939663.577472, 913311935.9512032, 67.5],
             [0.00337398766765, 111320.7020202162, 4481351.045890365, -23393751.19931662, 79682215.47186455,
              -115964993.2797253, 97236711.15602145, -43661946.33752821, 8477230.501135234, 52.5],
             [0.00220636496208, 111320.7020209128, 51751.86112841131, 3796837.749470245, 992013.7397791013,
              -1221952.21711287, 1340652.697009075, -620943.6990984312, 144416.9293806241, 37.5],
             [-0.0003441963504368392, 111320.7020576856, 278.2353980772752, 2485758.690035394,
              6070.750963243378, 54821.18345352118, 9540.606633304236, -2710.55326746645, 1405.483844121726, 22.5],
             [-0.0003218135878613132, 111320.7020701615, 0.00369383431289, 823725.6402795718,
              0.46104986909093, 2351.343141331292, 1.58060784298199, 8.77738589078284, 0.37238884252424, 7.45]]
    cf = []
    x = abs(x)
    y = abs(y)
    for i in range(len(MCBAND)):
        if y >= MCBAND[i]:
            cf = MC2LL[i]
            break

    location = converter(x, y, cf)
    return location


def connect_mysql(host, dbname, password, port, username):
    client = pymysql.Connect(host=host, port=port, user=username, passwd=password, db=dbname, charset='utf8')
    return client




def baidu_sreach(key, page, client):
    try:
        url = 'https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s' \
              '&da_src=searchBox.button&wd='+key+' 投资理财'+'&c=257&src=0&wd2=&pn=0&sug=0&l=12&b=(12571912.199999997,2607450.58;12604616.199999997,2655450.58)&from=webmap&biz_forward={%22scaler%22:2,%22styles%22:%22pl%22}&sug_forward=&auth=IM7xW1028F32Bec%3D9zawUZWDDUI4zCc4uxHHxEVHLxNt1qo6DF%3D%3DCy1uVtcvY1SGpuBtGIiyRWF%3D9Q9K%3DxAwEdwKv7uGccZcuVtPWv3GuBtWykiO%3DUixAC123N5T7XwcEWe1GD8zv7u%40ZPuVteuxxtoqFmqE25524b547I1pt66F9EzeeaCK&device_ratio=2&tn=B_NORMAL_MAP' \
              '&nn='+str(page * 10)+'&u_loc=12618395,2633167&ie=utf-8&t=1551405615732'
        data = json.loads(requests.get(url).text)
        if 'content' not in data:
            print('一共爬取 ' + key + str(page * 10) + ' 条数据！')
            return False
        contents = data['content']
        if len(contents)== 11:
            contents = contents[0:-1]
        cursor = client.cursor()
        sql = 'insert into topl_baidu_temp(uid,name,address,telephone,location,data_type,area_name) VALUES (%s,%s,%s,%s,%s,%s,%s)'
        for content in contents:
            data_list = []
            xy = mcat(content['x'] / 100, content['y'] / 100)
            data_list.append(content['name'])
            data_list.append(content['addr'])
            if 'tel' in content:
                data_list.append(content['tel'])
            else:
                data_list.append('')
            data_list.append(xy)
            data_list.append(content['uid'])
            data_list.append(5)  # 4 投资理财，1 银行 ,2 ATM
            data_list.append(content['area_name'])
            cursor.execute(sql, data_list)
            # 提交sql语句
            client.commit()
        return True
    except Exception as e:
        print(e)
        pass


def main():
    try:
        # client = connect_mysql('132.121.152.60', 'tpoc', 'Ab123456', 33068, 'tpoc')
        client = connect_mysql('127.0.0.1', 'bishe', '123', 3306, 'root')
        print("开始爬取数据，请稍等...")
        start_time = time.time()
        atm_list = ['越秀区', '天河区', '海珠区', '荔湾区', '白云区', '番禺区']
        for j in range(len(atm_list)):
            i = 0
            flag = True
            while (flag):
                flag = baidu_sreach(atm_list[j], i, client)
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
