import numpy as np
import folium
from folium import plugins
from folium.plugins import HeatMap
from pyecharts.charts import Bar
from pyecharts import options as opts


def read_data():
    f = open("cenc.txt", "r", encoding='utf-8')
    m = []
    date = []
    lat = []
    lon = []
    while True:
        line = f.readline()
        if not line:
            break
        line = line.split(' ')
        m.append(float(line[0]))
        date.append(line[1])
        lat.append(float(line[3]))
        lon.append(float(line[4]))
    return m, date, lat, lon


'''
同时画所有点
'''
def draw_pot_1(lat, lon):     # 纬度和经度
    lat = np.array(lat)
    lon = np.array(lon)
    world_map = folium.Map(zoom_start=10, control_scale=True,)
    incidents = folium.map.FeatureGroup()
    for i in range(len(lat)):
        incidents.add_child(
            folium.CircleMarker(        # 画圈
                (lat[i], lon[i]),       # 地震源经纬度坐标
                radius=3,               # 圆圈半径
                color='#FF1493',        # 标志的外圈颜色
                fill=True,              # 是否填充
                fill_color='#00FF00',   # 填充颜色
                fill_opacity=0.4        # 填充透明度
            )
        )
    world_map.add_child(incidents)
    world_map.save('world_map1.html')


''' 
一个区域类的点会合成一个点，点上数字表示这个区域有多少点
'''
def draw_pot_2(lat, lon):     # 纬度和经度
    lat = np.array(lat)
    lon = np.array(lon)
    world_map = folium.Map(zoom_start=10, control_scale=True,)
    marker_cluster = plugins.MarkerCluster().add_to(world_map)
    for i in range(len(lat)):
        folium.Marker(location=[lat[i], lon[i]]).add_to(marker_cluster)
    world_map.save('world_map2.html')


'''
静态热力图
'''
def draw_heat_map_1(m, lat, lon):
    data = []
    for i in range(len(m)):
        data.append([lat[i], lon[i], m[i]])
    world_map = folium.Map(zoom_start=10, control_scale=True,)
    HeatMap(data).add_to(world_map)
    world_map.save("HeatMap1.html")


'''
动态热力图
t = y 按年划分
t = m 按月划分（默认）
t = d 按日划分
'''
def draw_heat_map_2(m, date, lat, lon, t='m'):
    data = []       # 总数据
    data_m = []     # 一个时间划分的数据
    date_m = []
    lim = 7
    if t == 'd':
        lim = 10
    elif t == 'y':
        lim = 4
    for i in range(len(m)-1, -1, -1):
        data_m.append([lat[i], lon[i], m[i]])
        if date[i][:lim] != date[i-1][:lim]:
            data.append(data_m)
            data_m = []
            date_m.append(date[i][:lim])

    world_map = folium.Map(zoom_start=10, control_scale=True, )
    plugins.HeatMapWithTime(data, index=date_m).add_to(world_map)
    world_map.save("HeatMap2.html")


'''
柱状图 震级-次数
'''
def draw_bar_1(m):
    bar = Bar()
    count = {}
    for i in m:
        if i not in count:
            count[i] = 0
        count[i] += 1
    m = list(set(m))
    m.sort()
    bar.add_xaxis(m)
    y = []
    for x in m:
        y.append(count[x])
    bar.add_yaxis("地震次数", y)
    bar.set_global_opts(title_opts=opts.TitleOpts(title="震级-次数", subtitle="四川大学"))
    bar.render("bar1.html")


if __name__ == "__main__":      # 用已经爬的全部数据演示
    m, date, lat, lon = read_data()
    #draw_pot_1(lat, lon)
    #draw_pot_2(lat, lon)
    #draw_heat_map_1(m, lat, lon)
    #draw_heat_map_2(m, date, lat, lon, t='m')
    #draw_bar_1(m)

