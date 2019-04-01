# -*- coding: utf-8 -*-#

# -------------------------------------------------------------------------------
# Author:       liangjinyin
# Date:         2019/3/21 10:51
# Description:  处理分析poi点数据， 过滤一些杂质数据
# -------------------------------------------------------------------------------
import pymysql


def connect_mysql(host, dbname, password, port, username):
    client = pymysql.Connect(host=host, port=port, user=username, passwd=password, db=dbname, charset='utf8')
    return client


def main(city_code, std_tag):
    client = connect_mysql('127.0.0.1', 'bishe', '123', 3306, 'root')
    cursor = client.cursor()
    # 删除没有标签的数据
    '''
    sql = 'DELETE FROM topl_baidu_temp where data_type=%s AND city_code=%s and std_tag =""' % (data_type, city_code)
    cursor.execute(sql)
    client.commit()
    '''
    # 查询不是指定类型的数据 并删除
    sql = 'SELECT id FROM topl_baidu_temp where city_code=%s and std_tag not LIKE \'%s\'' % (city_code, std_tag)
    cursor.execute(sql)
    client.commit()
    data = cursor.fetchall()
    list_id = []
    for list_data in data:
        list_id.append(list_data[0])
    s = str(list_id)
    s = s[1:-1]
    sql = 'DELETE FROM topl_baidu_temp WHERE id IN(%s)' % s
    cursor.execute(sql)
    client.commit()

    # 删除重复的数据
    '''
    sql = 'SELECT min(id) as temp_id FROM topl_baidu_temp GROUP BY uid '
    cursor.execute(sql)
    client.commit()
    data = cursor.fetchall()
    '''
    # 关闭资源
    cursor = client.cursor()
    cursor.close()
    client.close()


'''
SELECT * FROM topl_baidu_temp WHERE id not in (
	SELECT t.temp_id FROM (SELECT MIN(id) as temp_id FROM topl_baidu_temp GROUP BY uid ) t) and city_code=140;
'''

if __name__ == '__main__':
    # 输入数据类型，城市编码，标签类型
    main(140, '%金融%')
