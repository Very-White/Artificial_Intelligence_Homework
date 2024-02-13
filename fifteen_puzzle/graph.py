from copy import deepcopy  # 导入深拷贝

graph_size = 4  # 每个图都是4*4的矩阵
goal = ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 0))
task1 = ((1, 2, 4, 8), (5, 7, 11, 10), (13, 15, 0, 3), (14, 6, 9, 12))
task2 = ((5, 1, 3, 4), (2, 7, 8, 12), (9, 6, 11, 15), (0, 13, 10, 14))
# 复杂一些:
task3 = ((14, 10, 6, 0), (4, 9, 1, 8), (2, 3, 5, 11), (12, 13, 7, 15))
task4 = ((6, 10, 3, 15), (14, 8, 7, 11), (5, 1, 0, 2), (13, 12, 9, 4))
# 挑战案例
task5 = ((11, 3, 1, 7), (4, 6, 8, 2), (15, 9, 10, 13), (14, 12, 5, 0))
task6 = ((0, 5, 15, 14), (7, 9, 6, 13), (1, 2, 12, 10), (8, 11, 4, 3))

all_task = [task1, task2, task3, task4, task5, task6]


def neighbours(current):
    """
    首先找到0（空格）的位置，然后将该空格分别和上下左右的元素交换，得到相邻的结点
    :param current: 当前的结点
    :return: 相邻的节点组成的列表
    """
    space_x = 0
    space_y = 0
    for row in range(graph_size):
        for col in range(graph_size):
            if current[row][col] == 0:
                space_x = row
                space_y = col

    adjacent_nodes = []

    for adjust in ((0, 1), (1, 0), (-1, 0), (0, -1)):
        # 如果下一个结点超出范围了就跳过
        if space_x + adjust[0] not in range(graph_size) or space_y + adjust[1] not in range(graph_size):
            continue

        # 交换
        # adjacent_node = deepcopy(current)
        # adjacent_node[space_x + adjust[0]][space_y + adjust[1]] = 0
        # adjacent_node[space_x][space_y] = current[space_x + adjust[0]][space_y + adjust[1]]

        adjacent_node = deepcopy(current)
        adjacent_node = list(adjacent_node)
        temp = list(adjacent_node[space_x + adjust[0]])
        temp[space_y + adjust[1]] = 0
        adjacent_node[space_x + adjust[0]] = tuple(temp)
        temp = list(adjacent_node[space_x])
        temp[space_y] = current[space_x + adjust[0]][space_y + adjust[1]]
        adjacent_node[space_x] = tuple(temp)
        adjacent_node = tuple(adjacent_node)

        adjacent_nodes.append(adjacent_node)

    return adjacent_nodes


def print_graph(graph_to_print):
    # 打印某个节点
    for level in graph_to_print:
        print(level)
    print()


hash_map = {
    1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3),
    5: (1, 0), 6: (1, 1), 7: (1, 2), 8: (1, 3),
    9: (2, 0), 10: (2, 1), 11: (2, 2), 12: (2, 3),
    13: (3, 0), 14: (3, 1), 15: (3, 2), 0: (3, 3),
}


def heuristic(current):
    """
    计算当前状态到目标状态的估计成本,因为目标状态是固定的[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
    :param current: 当前状态
    :return: 当前状态到目标状态的估计成本（启发函数）
    """

    # 为了加快计算速度，这里直接用哈希表存储最终状态各数字的坐标
    sum_of_all = 0
    for row in range(graph_size):
        for col in range(graph_size):
            # 计算曼哈顿距离
            num = current[row][col]
            sum_of_all += abs(row - hash_map[num][0]) + abs(col - hash_map[num][1])

            # 线性冲突，有很大的加速，以下是惩罚不同的时候案例三的运行时间
            # 当惩罚为1时：0:00:04.552661
            # 当惩罚为2时:0:00:08.159392
            # 当惩罚为3时:0:00:03.943093
            # 当惩罚为4时:0:00:02.668916
            # 当惩罚为5时:0:00:08.952399
            # 当惩罚为6时:0:00:08.137403
            # 当惩罚为7时:0:00:09.208672
            # 当惩罚为8时:0:00:04.377994
            # 当惩罚为9时:0:00:04.416050
            # 判断列上是否有线性冲突
            for k in range(row + 1, graph_size):
                if hash_map[current[k][col]][0] < row:  # 说明当前的num挡道了
                    sum_of_all += 4

            # 判断行上是否有线性冲突
            for k in range(col + 1, graph_size):
                if hash_map[current[row][k]][1] < col:  # 说明挡道了
                    sum_of_all += 4

    return sum_of_all


def to_str(graph_to_transform):
    """
    将图转化为字符串形式
    :param graph_to_transform: 待转化的图
    :return: 字符串
    """
    result = ""
    for level in graph_to_transform[:len(graph_to_transform) - 1]:
        result += str(level) + "\n"
    result += str(graph_to_transform[-1])
    return result
