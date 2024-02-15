import numpy as np
import copy
import random


def evaluate(distance: np.ndarray, path: list):
    """
    计算从第一个城市开始到最后一个城市的总距离
    :param distance: distance是城市间距离矩阵
    :param path: 包含了以城市编号序列作为的路径
    :return: 计算这条路径的总距离
    """
    total_length = 0
    for i in range(len(path) - 1):
        total_length += distance[path[i]][path[i + 1]]
    return total_length


# 某个父本变异得到孩子
def mutate(path: list):
    """
    将原始路径随机交换两个城市得到新路径
    :param path: 原始的路径
    :return: 随机交换两个城市后的路径
    """
    new_path = copy.deepcopy(path)
    first_city = random.randint(0, len(path) - 1)
    second_city = random.randint(0, len(path) - 1)
    # 交换两个城市
    temp = new_path[first_city]
    new_path[first_city] = new_path[second_city]
    new_path[second_city] = temp

    return new_path


def reverse_list(list_to_reverse: list, begin, end):
    if begin >= end:
        return
    for i in range(begin, (begin + end) // 2 + 1):
        temp = list_to_reverse[i]
        list_to_reverse[i] = list_to_reverse[end + begin - i]
        list_to_reverse[end + begin - i] = temp


# 父本交叉（部分逆序）得到孩子:
def inversion_twice(path: list):
    """
    父本交叉重组得到孩子，这里用的是翻转:
    :param path: 原始的路径
    :return: 基因重组后得到的路径
    """
    # 创建三个随机的索引
    city_list = []
    while len(city_list) != 3:
        city_list = [random.randint(0, len(path) - 1) for _ in range(3)]  # 生成三个元素
        city_list = set(city_list)  # 去重
    city_list = list(city_list)  # 变回列表
    city_list = sorted(city_list)  # 给索引排序
    new_path = copy.deepcopy(path)
    reverse_list(new_path, city_list[0], city_list[1])  # 逆序
    reverse_list(new_path, city_list[1], city_list[2])
    return new_path  # 返回


def inversion_once(path: list):
    """
    父本交叉重组得到孩子，这里用的是翻转:
    :param path: 原始的路径
    :return: 基因重组后得到的路径
    """
    # 创建三个随机的索引
    city_list = []
    while len(city_list) != 2:
        city_list = [random.randint(0, len(path) - 1) for _ in range(2)]  # 生成三个元素
        city_list = set(city_list)  # 去重
    city_list = list(city_list)  # 变回列表
    city_list = sorted(city_list)  # 给索引排序
    new_path = copy.deepcopy(path)
    reverse_list(new_path, city_list[0], city_list[1])  # 逆序
    return new_path  # 返回

def compete(population, children, scores: dict):
    compete_population = len(children)//10
    children_left = []
    while len(children_left) < population:
        children_chose = random.sample(range(0, len(children)), k=compete_population)
        min_length_index = children_chose[0]
        min_length = scores[str(children[min_length_index])]
        # 找到分数最高（距离最短的那个孩子）
        for index in children_chose:
            if scores[str(children[index])] < min_length:
                min_length = scores[str(children[index])]
                min_length_index = index
        children_left.append(children[min_length_index])
        del children[min_length_index]
    return children_left


def genetic_algorithm(distance: np.ndarray, init_path: list, upper_limit=1000):
    """
    遗传算法求解：
    1.生成初始聚落
    2.通过交叉，变异操作得到子聚落
    3.记录该子聚落中得分最好的孩子
    4.用两两竞争法得到下一种群
    5.重复2-3步直到迭代上限
    :param distance:距离矩阵
    :param init_path:初始路径
    :param upper_limit:迭代上限
    :return:历史最优子代，还有历史最优子代的分数
    """
    population = 40
    # 用随机的父代初始化种群
    fathers = []
    for i in range(population):
        fathers.append(inversion_twice(init_path))
    iteration_time = 0

    history_path = []
    history_length = []
    while iteration_time < upper_limit:
        print(iteration_time)
        children = []
        # 变异,交叉操作（还保留一个原来的父本）:
        for father in fathers:
            children.append(mutate(father))
            children.append(inversion_twice(father))
            children.append(inversion_once(father))
            children.append(father)
        # 计算并记录最大分数
        paths_length = {}
        min_length_path = children[0]
        min_length = evaluate(distance, min_length_path)
        for child in children:
            path_length = evaluate(distance, child)
            # 记录该代最短路径
            if min_length > path_length:
                min_length = path_length
                min_length_path = child
            paths_length[str(child)] = path_length
        children_left = compete(population, children, paths_length)

        fathers = children_left
        history_path.append(min_length_path)
        history_length.append(min_length)
        iteration_time += 1
    return history_path, history_length
