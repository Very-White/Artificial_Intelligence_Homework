import math
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


def reverse_list(list_to_reverse: list, begin, end):
    if begin >= end:
        return
    for i in range(begin, (begin + end) // 2 + 1):
        temp = list_to_reverse[i]
        list_to_reverse[i] = list_to_reverse[end + begin - i]
        list_to_reverse[end + begin - i] = temp


def swap_two(path: list):
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


def inversion_twice(path: list):
    """
    将原始路径随机交换三个城市得到新路径
    :param path: 原始的路径
    :return: 随机交换三个城市后的路径
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


def local_search(distance: np.ndarray, init_path: list, upper_limit=1000):
    """
    使用局部搜索的传统爬山算法：
        1.计算初始路径的长度
        2.改变初始路径：随机交换两个城市的位置,或取两端逆序
        3.计算新路径的长度
            如果没有更低，则进行下一个循环
            否则接受新的路径
        4.重复2-3步直到迭代次数上限
    :param upper_limit: 迭代次数上限
    :param distance: 各城市之间的距离矩阵
    :param init_path: 初始的路径
    :return: 历史搜索路径,总路径长度
    """
    path = copy.deepcopy(init_path)
    history_path = [path]
    history_length = [evaluate(distance, path)]
    for i in range(upper_limit):
        # 计算路径长度
        total_length = evaluate(distance, path)
        # 扰动
        choice = random.random()
        if choice < 0.3:
            new_path = swap_two(path)
        elif choice < 0.6:
            new_path = inversion_twice(path)
        else:
            new_path = inversion_once(path)
        new_total_length = evaluate(distance, new_path)
        if new_total_length < total_length:
            path = new_path
            history_path.append(path)
            history_length.append(new_total_length)
    return history_path, history_length


# 模拟退火算法
def SA(distance: np.ndarray, init_path: list, upper_limit=1000):
    """
    使用模拟退火算法：
        1.计算初始路径的长度，设置初始温度，设置当前循环次数
        2.改变初始路径：随机交换两个城市的位置，或取两端逆序
        3.计算新路径的长度
        4.根据模拟退火函数计算是否接受新路径
            如果接受，则变更路径，并且对温度进行衰减，循环次数加一
            如果不接受，则不改变任何参数
        4.重复2-3步直到迭代次数上限
    :param distance: 各城市之间的距离矩阵
    :param init_path: 初始的路径
    :param upper_limit: 迭代次数上限
    :return: 历史搜索路径,总路径长度
    """
    iteration_time = 0
    temperature = upper_limit * 100
    path = copy.deepcopy(init_path)

    # 返回参数
    history_path = []
    history_length = []
    while iteration_time < upper_limit:
        print(iteration_time)
        total_length = evaluate(distance, path)
        # 扰动
        choice = random.random()
        if choice < 0.3:
            new_path = swap_two(path)
        elif choice < 0.6:
            new_path = inversion_twice(path)
        else:
            new_path=inversion_once(path)

        new_total_length = evaluate(distance, new_path)
        # 得到一个随机数
        X = random.random()
        # 通过模拟退火函数判断接不接受
        delta_length = new_total_length - total_length
        Y = None
        if delta_length < 0:
            Y = 1
        else:
            Y = 1 / math.exp(min(delta_length / temperature, 10))  # 防止溢出了
        # 不接受就不做任何事，接受就变更路径，并且对温度进行衰减，循环次数加一
        if Y <= X:
            continue
        else:
            path = new_path
            history_path.append(path)
            history_length.append(new_total_length)
            temperature = temperature * 0.99
            iteration_time += 1

    return history_path, history_length
