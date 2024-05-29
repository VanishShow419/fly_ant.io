import matplotlib.pyplot as plt
from matplotlib import font_manager
from aoc import newx, newy, best_route
from dbconn_cities import num, city_names, cities

font_path = 'C:/Windows/Fonts/msyh.ttc'  # 请确保路径是正确的
prop = font_manager.FontProperties(fname=font_path)

# 设置matplotlib的全局字体为SimHei
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

plt.figure()
plt.scatter(newx, newy, color='blue', s=2)
for i in range(num):
    # 下一个点需要对num进行取余
    next_i = (i + 1) % num
    plt.plot([newx[i], newx[next_i]], [newy[i], newy[next_i]], color='red')

# 绘制图形并添加标签、标题等
plt.xlabel("经度", fontproperties=prop)  # 使用支持中文的字体
plt.ylabel("纬度", fontproperties=prop)
plt.title("蚁群算法路径", fontproperties=prop)

# 背景含网格
plt.grid(True)

# 假设您已经有了best_route和对应的城市坐标newx, newy
city_names = list(cities.keys())
for i in range(num):
    plt.text(newx[i], newy[i], city_names[best_route[i]], fontsize=10, ha='center', va='center', fontproperties=prop)

# 展示图片
plt.show()
