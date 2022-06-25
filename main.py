# -*- coding: utf-8 -*-
# @Time : 2022/6/18 14:47
# @Author : xxxxxxxxxxxxxxxxxx
# @File : book.py
import time

import mongoengine
import requests
from mongoengine import Document, StringField, FloatField, DateTimeField, IntField, connect, disconnect
import time
import datetime
import ast

url = "http://www.ceic.ac.cn/ajax/search"

_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.3"
}

EPS = 1e-6          # 用于浮点数比较

M = []              # 震级
O_TIME = []         # 发震时刻(UTC+8)
EPI_LAT = []        # 纬度(°)
EPI_LON = []        # 经度(°)
EPI_DEPTH = []      # 深度(千米)
LOCATION_C = []     # 参考位置
'''
M_OLD = []
O_TIME_OLD = []
EPI_LAT_OLD = []
EPI_LON_OLD = []
EPI_DEPTH_OLD = []
LOCATION_C_OLD = []


def read_data():
    f = open("cenc.txt", "r", encoding='utf-8')
    while True:
        line = f.readline()
        if not line:
            break
        line.rstrip()
        line = line[:-1]
        line = line.split(' ')
        M_OLD.append(line[0])
        O_TIME_OLD.append(line[1] + " " + line[2])
        EPI_LAT_OLD.append(line[3])
        EPI_LON_OLD.append(line[4])
        EPI_DEPTH_OLD.append(line[5])
        LOCATION_C_OLD.append(line[6])
    f.close()
'''


def retrive(url, params):
    response = requests.get(url, headers=_header, params=params)
    text = response.content.decode()
    x = text.find('[')
    y = text.find(']')
    text = "," + text
    texts = text[x+1:y].split("}")
    for i in range(len(texts)):
        texts[i] = texts[i][1:]
        texts[i] += '}'
    return texts


def parse(texts, data_lastest):
    # f = open('cenc.txt', 'w', encoding='utf-8')
    for text in texts:
        data_dict = ast.literal_eval(text)
        sub_keys = ['M', 'O_TIME', 'EPI_LAT', 'EPI_LON', 'EPI_DEPTH', 'LOCATION_C']
        data_dict = dict([(key, data_dict[key]) for key in sub_keys])
        print(data_dict)
        if data_dict['M'] == str(data_lastest.M) and data_dict['O_TIME'] == str(data_lastest.O_TIME) and float(data_dict['EPI_LAT']) - data_lastest.EPI_LAT < EPS and float(data_dict['EPI_LON']) - data_lastest.EPI_LON < EPS and data_dict['EPI_DEPTH'] == data_lastest.EPI_DEPTH and data_dict['LOCATION_C'] == str(data_lastest.LOCATION_C):
            print("该数据已在数据库中！停止爬虫！")
            return True
        EPI(**data_dict).save()
        '''
        M.append(data_dict['M'])
        O_TIME.append(data_dict['O_TIME'])
        EPI_LAT.append(data_dict['EPI_LAT'])
        EPI_LON.append(data_dict['EPI_LON'])
        EPI_DEPTH.append(data_dict['EPI_DEPTH'])
        LOCATION_C.append(data_dict['LOCATION_C'])
        print((M[-1], O_TIME[-1], EPI_LAT[-1], EPI_LON[-1], EPI_DEPTH[-1], LOCATION_C[-1]))
        msg = f"{M[-1]} {str(O_TIME[-1])} {EPI_LAT[-1]} {EPI_LON[-1]} {EPI_DEPTH[-1]} {LOCATION_C[-1]}"
        if msg == f"{M_OLD[0]} {str(O_TIME_OLD[0])} {EPI_LAT_OLD[0]} {EPI_LON_OLD[0]} {EPI_DEPTH_OLD[0]} {LOCATION_C_OLD[0]}":
            print("该信息已在库内，停止爬取！")
            return True
        print(f"{M[-1]} {str(O_TIME[-1])} {EPI_LAT[-1]} {EPI_LON[-1]} {EPI_DEPTH[-1]} {LOCATION_C[-1]}", file=f)
        '''
    # f.close()
    return False


class EPI(Document):
    M = FloatField()
    O_TIME = DateTimeField()
    EPI_LAT = FloatField()
    EPI_LON = FloatField()
    EPI_DEPTH = IntField()
    LOCATION_C = StringField()


def main():
    # read_data()
    try:
        num = len(EPI.objects().order_by('O_TIME'))
        data_lastest = EPI.objects().order_by('O_TIME')[num-1]
        print(EPI.objects().order_by('O_TIME')[num-1])
    except IndexError:
        data_lastest = EPI()
    for page in range(1, 517):
        print(f"第{page}页")
        params = {
            "start": "",
            "end": "",
            "jingdu1": "",
            "jingdu2": "",
            "weidu1": "",
            "weidu2": "",
            "height1": "",
            "height2": "",
            "zhenji1": "",
            "zhenji2": "",
        }
        times = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time_array = time.strptime(times, "%Y-%m-%d %H:%M:%S")
        time_stamp = int(time.mktime(time_array))  # 转换时间戳
        time.sleep(5)
        params["callback"] = f"jQuery180031232585725055584_1607253668377&_={time_stamp}"
        params["page"] = page
        content = retrive(url, params)
        end = parse(content, data_lastest)
        if end:
            break
    '''
    f = open('cenc.txt', 'a', encoding='utf-8')
    for i in range(len(M_OLD)):
        print(f"{M_OLD[i]} {str(O_TIME_OLD[i])} {EPI_LAT_OLD[i]} {EPI_LON_OLD[i]} {EPI_DEPTH_OLD[i]} {LOCATION_C_OLD[i]}", file=f)
    f.close()
    '''

if __name__ == '__main__':
    connect(host="mongodb://localhost/cenc")
    main()
    disconnect()