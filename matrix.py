import numpy as np
from dbconn_cities import cities, num, cities_weather

# 将城市坐标转换为points
points = list(cities.values())
weather_points = list(cities_weather.values())
print("检查初代点坐标：")
print(points)
print(weather_points)


# 计算初代点symmetric matrix的函数
def distance_matrix(points):
    # 初始化一个0 matrix
    matrix = np.zeros((num, num))

    # 开始计算各点之间的距离
    for i in range(num):
        for j in range(num):
            # 如果当前点=>当前点，则认为是infinite distance
            if i == j:
                matrix[i, j] = np.inf
            # 否则，计算两个点之间的欧式距离
            else:
                matrix[i, j] = np.sqrt((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)

    # 返回计算后的matrix
    return matrix


def weather_conditions_matrix(weather_points):
    # 初始化一个0 matrix
    matrix = np.zeros((num, num))

    # 开始计算各点之间的距离
    for i in range(num):
        for j in range(num):
            # 如果当前点=>当前点，则认为是infinite distance
            if i == j:
                matrix[i, j] = np.inf
            # 否则，计算两个点之间的欧式距离
            else:
                matrix[i, j] = np.sqrt((weather_points[i][0] - weather_points[j][0]) ** 2 + (weather_points[i][1] - weather_points[j][1]) ** 2)
    # 返回计算后的matrix
    return matrix


# 进行天气矩阵生成
weather_matrix = weather_conditions_matrix(weather_points)
# 检查天气矩阵
print(weather_matrix)
# 进行初代矩阵生成
original_matrix = distance_matrix(points)
# 检查初代矩阵
print(original_matrix)
