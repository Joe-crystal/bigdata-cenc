# -*- coding: utf-8 -*-
# @Time : 2022/6/18 14:47
# @Author : xxxxxxxxxxxxxxxxxx
# @File : book.py
import time

import requests
from mongoengine import Document, StringField, connect, disconnect
import time
import datetime
import ast

url = "http://www.ceic.ac.cn/ajax/search"

_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.3"
}

M = []
O_TIME = []
EPI_LAT = []
EPI_LON = []
EPI_DEPTH = []
LOCATION_C = []


def retrive(url, params):
    time.sleep(1)
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


def parse(texts):
    f = open('cenc.txt', 'a', encoding='utf-8')
    for text in texts:
        data_dict = ast.literal_eval(text)
        M.append(data_dict['M'])
        O_TIME.append(data_dict['O_TIME'])
        EPI_LAT.append(data_dict['EPI_LAT'])
        EPI_LON.append(data_dict['EPI_LON'])
        EPI_DEPTH.append(data_dict['EPI_DEPTH'])
        LOCATION_C.append(data_dict['LOCATION_C'])
        print((M[-1], O_TIME[-1], EPI_LAT[-1], EPI_LON[-1], EPI_DEPTH[-1], LOCATION_C[-1]))
        print(f"{M[-1]} {str(O_TIME[-1])} {EPI_LAT[-1]} {EPI_LON[-1]} {EPI_DEPTH[-1]} {LOCATION_C[-1]}", file=f)
    f.close()


def main():

    f = open('cenc.txt', 'w', encoding='utf-8')
    f.close()
    for page in range(1, 515):
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
        parse(content)


if __name__ == '__main__':
    main()
