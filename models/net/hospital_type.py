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


'''
工商银行, 建设银行, 农业银行, 中国银行,招商银行,交通银行,邮政储蓄,农村信用社,
中信银行,民生银行,光大银行,广发银行,北京银行,浦发银行,平安银行,兴业银行
'''


def baidu_sreach(key, page, client):
    try:
        '''
        url_hospital = 'https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=spot' \
              '&from=webmap&c=257&wd=诊所 '+key+'&wd2=&pn=0' \
              '&nn=' + str(page * 50) + '&db=0&sug=0&addr=0&district_name=%E5%A4%A9%E6%B2%B3%E5%8C%BA&business_name=&pl_data_type=hospital&pl_sub_type=&pl_price_section=0%2C%2B&pl_sort_type=&pl_sort_rule=0&pl_discount2_section=0%2C%2B&pl_groupon_section=0%2C%2B&pl_cater_book_pc_section=0%2C%2B&pl_hotel_book_pc_section=0%2C%2B&pl_ticket_book_flag_section=0%2C%2B&pl_movie_book_section=0%2C%2B&pl_business_type=hospital&pl_business_id=&da_src=pcmappg.poi.page&src=7&rn=50&tn=B_NORMAL_MAP&auth=KOQQEJUJ7bNHNDd%3D0Gv5yxUJ9Bv5WI%3DxuxHHzVBEBzxt1qo6DF%3D%3DCy1uVt1GgvPUDZYOYIZuVt1cv3uVtGccZcuVtPWv3GuTztbGtrVh%40rFHJKNQUW9acEcEWe1GD8zv7u%40ZPuxRHtizC1Xymo1koDFOO2%3DF%3DLLFCdw8E62qvyCuquTTGIRFFkk0H48&u_loc=12618349,2631334&ie=utf-8'
        '''
        url_hospital = 'https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=spot&' \
              'from=webmap&c=257&wd=医院 '+key+'&wd2=&pn=0' \
              '&nn=' + str(page * 50) + '&db=0&sug=0&addr=0&district_name=%E8%B6%8A%E7%A7%80%E5%8C%BA&business_name=&pl_data_type=hospital&pl_sub_type=%E5%8C%BB%E9%99%A2&pl_price_section=0%2C%2B&pl_sort_type=&pl_sort_rule=0&pl_discount2_section=0%2C%2B&pl_groupon_section=0%2C%2B&pl_cater_book_pc_section=0%2C%2B&pl_hotel_book_pc_section=0%2C%2B&pl_ticket_book_flag_section=0%2C%2B&pl_movie_book_section=0%2C%2B&pl_business_type=hospital&pl_business_id=&da_src=pcmappg.poi.page&src=7&rn=50&tn=B_NORMAL_MAP&auth=KOQQEJUJ7bNHNDd%3D0Gv5yxUJ9Bv5WI%3DxuxHHzVzNEzTtxjhNwzWWvy1uVt1GgvPUDZYOYIZuVtcvY1SGpuEt2gz4yYxGccZcuVtPWv3GuHNtg3yw8mdwJL4ORUY9cf0IcEWe1GD8zv7u%40ZPuxBtqGbFmo1koDFOO2%3DF%3DLLFCfiKKv7urZZWux&u_loc=12618349,2631334&ie=utf-8'

        data = json.loads(requests.get(url_hospital).text)
        if 'content' not in data:
            print('一共爬取 ' + key + str(page * 50) + ' 条数据！')
            return False
        contents = data['content']
        cursor = client.cursor()
        sql = 'insert into topl_baidu_hospital(uid,name,address,aoi,location,tel,data_type,area_name,di_tag,alias)' \
              ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        for content in contents:
            data_list = []
            ailas_list = []
            location = mcat(content['x'] / 100, content['y'] / 100)
            uid = content['uid']
            name = content['name']
            addr = content['addr']
            if 'aoi' in content:
                aoi = content['aoi']
            else:
                aoi = ''
            area_name = content['area_name']
            if 'std_tag' in content:
                di_tag = content['std_tag']
            else:
                di_tag = content['tag']
            if 'alias' in content:
                ailas_list = content['alias']
            data_list.append(uid)
            data_list.append(name)
            data_list.append(addr)
            data_list.append(aoi)
            data_list.append(location)
            if 'tel' in content:
                data_list.append(content['tel'])
            else:
                data_list.append('')
            data_list.append(3)
            data_list.append(area_name)
            data_list.append(di_tag)
            if len(ailas_list) != 0:
                data_list.append(','.join(ailas_list))
            else:
                data_list.append('')
            cursor.execute(sql, data_list)
            # 提交sql语句
            client.commit()
        return True
    except Exception as e:
        print('出现了问题！')
        print(e)
        pass


def main():
    try:
        # client = connect_mysql('132.121.152.60', 'tpoc', 'Ab123456', 33068, 'tpoc')
        client = connect_mysql('127.0.0.1', 'bishe', '123', 3306, 'root')
        print("开始爬取数据，请稍等...")
        start_time = time.time()
        area_list = ['越秀区', '天河区', '海珠区', '荔湾区', '白云区', '番禺区']
        for j in range(len(area_list)):
            i = 0
            flag = True
            while (flag):
                flag = baidu_sreach(area_list[j], i, client)
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
