# 对中国地震台网进行大数据分析

##  爬虫$（main.py）$

### 数据格式

与中国地震台网相同，共6列

1. $M$	震级
2. $O\_TIME$      发震时刻$(UTC+8)$ $xxxx-xx-xx xx:xx:xx$(年-月-日 时:分:秒)
3. $EPI\_LAT$    纬度(°) $[-90, 90]$
4. $EPI\_LON$    经度(°) $[-180, 180]$
5. $EPI\_DEPTH$    深度(千米)
6. $LOCATION\_C$    参考位置

数据存于$cenc.txt$中



## 数据可视化$（draw.py）$

### 总说明

虽然main函数中读取了$cenc.txt$中所有数据，但所有画图函数都可以传你筛选好的数据，就只画筛选好的数据。

画的每张图都单独存在一个$html$中

### 接口

```python
'''
m: 震级
date: 发震时刻(UTC+8)xxxx-xx-xx(年-月-日）
lat: 纬度(°) [-90, 90]
lon: 经度(°) [-180, 180]

'''
def draw_pot_1(lat, lon) 						  # 同时画所有点
def draw_pot_2(lat, lon)						  # 一个区域类的点会合成一个点，点上数字表示这个区域有多少点
def draw_heat_map_1(m, lat, lon)				   # 静态热力图
def draw_heat_map_2(m, date, lat, lon, t='m')  		# 动态热力图 (t=y 按年划分)(t=m 按月划分（默认）)(t = d 按日划分)
def draw_bar_1(m)								  # 柱状图 震级-次数
```

#### draw_pot_1

在世界地图上把每一次地震都画了一个点，点数多时会比较卡

#### draw_pot_2

还是画点，但一定区域的点会聚成一个，点上有数字表示这个点代表的区域有多少次地震

![draw_pot_2_1](E:\class\bigdata-cenc\imgs\draw_pot_2_1.png)

鼠标放到点上会显示这个点代表的区域

放大地图点会变多

<img src="E:\class\bigdata-cenc\imgs\draw_pot_2_2_.gif" alt="draw_pot_2_2_" style="zoom:50%;" />

#### draw_heat_map_1

静态的热力图，也可以放大

<img src="E:\class\bigdata-cenc\imgs\draw_heat_map_1_1.png" alt="draw_heat_map_1_1" style="zoom:75%;" />

#### draw_heat_map_2

动态的热力图，可放大，按时间（年|月|日）变化

默认按月变化，可通过参数$t= y \ or \ m \ or \ d$改变

以下为默认的按月变化：

![draw_heat_map_2_1_](E:\class\bigdata-cenc\imgs\draw_heat_map_2_1_.gif)

可自动变化、或手动下一个月的，自动的情况下可调节fps



#### draw_bar_1

震级-次数的柱状图，展示不同震级地震出现次数的分布情况

![draw_bar_1_1](E:\class\bigdata-cenc\imgs\draw_bar_1_1.png)