# -*- coding: utf-8 -*-#

# -------------------------------------------------------------------------------
# Author:       liangjinyin
# Date:         2019/4/4 15:35
# Description:  Excel数据解析
# -------------------------------------------------------------------------------

import pandas as pd
import threading


class Analysis_Excel(object):

    @staticmethod
    def read_excel():
        # 解析输入源
        excel_ori = pd.read_excel('haizhu.xlsx', sheet_name='zh')
        data_list = excel_ori.values
        print('数据有' + str(len(data_list)) + '条！')
        temp_list = []
        # Analysis_Excel.analysis_data(data_list, temp_list)
        # 多线程调用提高速度
        t = threading.Thread(target=Analysis_Excel.analysis_data, args=(data_list, temp_list))
        t.start()
        return temp_list

    @staticmethod
    def export_excel(result):
        df = pd.DataFrame.from_dict(result)
        df.to_excel("G://百度信息点.xlsx")

    @staticmethod
    def analysis_name(name, build_type):
        if build_type == '地址':
            build_name = name.split('小区')
            name = build_name[0]
        else:
            name_list = str(name).split('-')
            if len(name_list) - 1 >= 0:
                name = name_list[len(name_list) - 1]
            else:
                name = name
        return name

    @staticmethod
    def analysis_data(data_list, temp_list):
        for data in data_list:
            build_type = data[0].strip()
            build_id = data[1]
            city = data[2]
            city = city[0:2]
            sub = data[3]
            sub = sub.replace('分公司', '')
            build_name = data[4]
            # l = re.findall('\D*', '珠海市斗门区五山荔山村榕苑小区二巷13号')
            # build_name='珠海市斗门区五山荔山村榕苑小区二巷13号'
            # build_name = build_name.split('小区')       # l = re.findall('\D*', '珠海市斗门区五山荔山村榕苑小区二巷13号')
            # build_name='珠海市斗门区五山荔山村榕苑小区二巷13号'
            # build_name = build_name.split('小区')
            name = Analysis_Excel.analysis_name(build_name, build_type)
            data_map = {'build_id': build_id, 'city': city, 'sub': sub, 'name': name}
            temp_list.append(data_map)
