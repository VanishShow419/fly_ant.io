import time
import numpy as np
from dbconn_cities import num, start
from matrix import original_matrix, points, weather_matrix


# 蚁群算法类
class ACO:
    # 初始化（包括城市数目、距离矩阵、蚂蚁数目、迭代次数、信息素因子、距离因子、挥发因子、信息素强度）
    def __init__(self, num_cities, distance_matrix, weather_matrix, num_ants, max_iter=200, alpha=2, beta=5, rho=0.5, q=100):
        # 城市数目
        self.num_cities = num_cities
        # 距离矩阵
        self.distance_matrix = distance_matrix
        #天气矩阵
        self.weather_matrix = weather_matrix
        # 信息素矩阵，其中shape属性返回数组的维度
        self.pheromone = np.ones(self.distance_matrix.shape) / num_cities
        # 蚂蚁数目
        self.num_ants = num_ants
        # 迭代次数
        self.max_iter = max_iter
        # 信息素因子
        self.alpha = alpha
        # 距离因子
        self.beta = beta
        # 挥发因子
        self.rho = rho
        # 信息素强度
        self.q = q

    # 更新信息素
    def _update_pheromone(self, ants):
        self.pheromone *= (1 - self.rho)
        epsilon = 1e-10  # 避免除以零
        for ant in ants:
            for i in range(self.num_cities - 1):
                self.pheromone[ant[i]][ant[i + 1]] += self.q / (
                            self.distance_matrix[ant[i]][ant[i + 1]] + epsilon) + self.q / (
                                                                  self.weather_matrix[ant[i]][ant[i + 1]] + epsilon)
            self.pheromone[ant[-1]][ant[0]] += self.q / (self.distance_matrix[ant[-1]][ant[0]] + epsilon) + self.q / (
                        self.weather_matrix[ant[-1]][ant[0]] + epsilon)

    # 选择下一个城市
    def _choose_next_city(self, current_city, visited):
        available_cities = [i for i in range(self.num_cities) if i not in visited]
        probabilities = np.zeros(len(available_cities))
        epsilon = 1e-10  # 避免除以零
        for i, city in enumerate(available_cities):
            probabilities[i] = self.pheromone[current_city][city] ** self.alpha * (
                    (1.0 / (self.distance_matrix[current_city][city] + epsilon)) ** self.beta +
                    (1.0 / (self.weather_matrix[current_city][city] + epsilon)) ** self.beta
            )
        if np.all(probabilities == 0):
            return np.random.choice(available_cities)  # 所有概率都是零时，随机选择一个城市
        probabilities /= np.sum(probabilities)
        chosen_city_index = np.random.choice(len(available_cities), p=probabilities)
        return available_cities[chosen_city_index]
    # 解决TSP问题
    def solve(self):
        # 初始化最好路线和距离
        best_route = None
        best_distance = float('inf')

        # 进行每一次的迭代
        for _ in range(self.max_iter):
            # 初始化蚂蚁，令他们随机分配到一个城市
            ants = [[np.random.randint(self.num_cities)] for _ in range(self.num_ants)]

            # 遍历每一只蚂蚁
            for ant in ants:
                # 生成完整的路径
                for _ in range(self.num_cities - 1):
                    # 当前路径中的最后一个城市
                    current_city = ant[-1]
                    # 调用函数，选择下一个访问的城市
                    next_city = self._choose_next_city(current_city, ant)
                    # push到蚂蚁的数组里面
                    ant.append(next_city)

            # 更新信息素
            self._update_pheromone(ants)

            # 遍历每一只蚂蚁
            for ant in ants:
                # 生成距离
                distance = sum([self.distance_matrix[ant[i]][ant[i + 1]] for i in range(-1, self.num_cities - 1)]+[self.weather_matrix[ant[i]][ant[i + 1]] for i in range(-1, self.num_cities - 1)])
                # 更新最好距离
                if distance < best_distance:
                    best_distance = distance
                    best_route = ant

        # 返回最优解
        return best_route, best_distance


# 蚂蚁的数量（城市数量的1.5倍）
num_ants = int(num * 15)

# 初始化aco类
aco = ACO(num, original_matrix, weather_matrix,num_ants)

# 利用类中的solve函数，进行TSP问题的求解
best_route, best_distance = aco.solve()

# 结束计时
end = time.time()

# 计算算法的耗时
during = end - start
print(f"Time consumption: {during}s")

# 输出最佳路线和距离
print(f"Best route: {best_route}")
print(f"Best distance: {best_distance}")

# 使用zip分离坐标
x, y = zip(*points)

# 初始化新的x和y坐标的数组
newx = []
newy = []

# 根据best-route更新newx和newy
for i in range(num):
    # 当前点的id是best-route中的编号
    id = best_route[i]
    # 新增点的坐标信息
    newx.append(x[id])
    newy.append(y[id])