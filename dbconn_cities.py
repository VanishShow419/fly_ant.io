import time
import pandas as pd
import mysql.connector
# print("""
#                ,----------------,              ,---------,
#           ,-----------------------,          ,"        ,"|
#         ,"                      ,"|        ,"        ,"  |
#        +-----------------------+  |      ,"        ,"    |
#        |  .-----------------.  |  |     +---------+      |
#        |  |                 |  |  |     | -==----'|      |
#        |  |  I LOVE PyThon! |  |  |     |         |      |
#        |  |  Bad command or |  |  |/----|`---=    |      |
#        |  |  C:\>_          |  |  |   ,/|==== ooo |      ;
#        |  |                 |  |  |  // |(((( [33]|    ,"
#        |  `-----------------'  |," .;'| |((((     |  ,"
#        +-----------------------+  ;;  | |         |,"
#           /_)______________(_/  //'   | +---------+
#      ___________________________/___  `,
#     /  oooooooooooooooo  .o.  oooo /,   \,"-----------
#    / ==ooooooooooooooo==.o.  ooo= //   ,`\--{)B     ,"
#   /_==__==========__==_ooo__ooo=_/'   /___________,"
#
# """)
# MySQL数据库连接信息
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',  # 或者你的数据库服务器地址
    'database': 'aoc_data',
    'raise_on_warnings': True
}

# 创建数据库连接
cnx = mysql.connector.connect(**config)

# 使用pandas的read_sql_query函数从数据库中读取数据
query = "SELECT * FROM cities"

# 城市和它们的经纬度
city_names = pd.read_sql_query(query, cnx)

print("\033[36m{:=^50s}\033[0m".format("Split Line"))
print("""    天气因子：
    \033[32m0  晴天
    10  阴天\033[0m
    \033[33m30  暴雨
    40  雪\033[0m
    \033[31m50  雷雨
    60  冰雹
    100  极端天气\033[0m""")
print("\033[36m{:=^50s}\033[0m".format("Split Line"))
print("""    风向因子：
    \033[32m0  顺风\033[0m
    \033[33m20  无风\033[0m
    \033[31m40  逆风\033[0m""")
print("\033[36m{:=^50s}\033[0m".format("Split Line"))


# 城市数目
num = int(input("\033[34m请输入安排航班的城市数量：\033[0m"))
# 开始计时
start = time.time()

city_names = city_names.set_index('城市')

cities = {}
cities_weather = {}
for x in range(1, num + 1):  # 循环从1开始，但确保结束条件是num + 1来包含所有城市
    name_num = input("\033[34m请输入第{}城市名称：\033[0m".format(x))  # 不需要转换为str，因为input已经返回str
    weather_num = input("\033[34m请输入第{}城市的天气\033[0m：".format(x))
    wind_num = input("\033[34m请输入第{}城市的风向：\033[0m".format(x))
    try:
        # 使用.at[]访问器，它更快且适用于单个值的查找
        latitude = city_names.at[name_num, '北纬']
        longitude = city_names.at[name_num, '东经']
        cities[name_num] = (longitude, latitude)
        cities_weather[name_num] = (int(weather_num),int(wind_num))
    except KeyError:
        print("找不到城市名称：'{}'。请重试。".format(name_num))
        # 在这里可以添加逻辑来处理找不到城市名称的情况，比如重新请求输入或退出循环

# 当你完成所有操作后，关闭数据库连接
cnx.close()


