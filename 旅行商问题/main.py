import pandas as pd
import numpy as np
from math import sqrt
import ReadData
import SA_search
import genetic_algorithm
import random

# 读取数据
cities_position = ReadData.read_data('cities_position.txt')
# 预处理
for index, line in enumerate(cities_position, start=0):
    line = line.split()
    position = [float(line[1]), float(line[2])]
    cities_position[index] = position
# 将城市的坐标保存成表格
cities_position = pd.DataFrame(cities_position, columns=['x坐标', 'y坐标'])
cities_position.to_excel('cities_position.xlsx', index=True, sheet_name='cities_position')
# 创建距离矩阵
cities_amount = cities_position.shape[0]
distance_matrix = np.zeros((cities_amount, cities_amount))


# 计算城市间的距离矩阵i,j元表示城市i到城市j的距离
# 计算欧几里得距离
def calculate_distance(city1: pd.Series, city2: pd.Series):
    return sqrt((city1.iloc[0] - city2.iloc[0]) ** 2 + (city1.iloc[1] - city2.iloc[1]) ** 2)


# 计算距离
for i in range(cities_amount):
    for j in range(cities_amount):
        distance_matrix[i][j] = calculate_distance(cities_position.iloc[i, :], cities_position.iloc[j, :])

# 寻找路径,在这里可以修改算法
history_path, history_length = SA_search.local_search(distance_matrix,
                                                      random.sample(range(0, cities_amount),
                                                                    cities_amount), 10000)

column_index = []
for i in range(cities_amount):
    column_index.append(f'第{i + 1}个访问的城市')
# 转化为表格
result = pd.DataFrame(history_path, columns=column_index)
result['路径长度'] = history_length
with pd.ExcelWriter('经典爬山算法.xlsx', mode='w') as writer:
    result.to_excel(writer, index=False)
print(result)
print(result.sort_values(by='路径长度'))
