from queue import PriorityQueue  # 优先队列
from graph import heuristic, neighbours, to_str, goal  # 对图进行计算


def a_star_search(start):
    frontier = PriorityQueue()
    frontier.put((0, start))  # 初始化优先队列
    come_from = {}
    cost_so_far = {}
    come_from[to_str(start)] = None
    cost_so_far[to_str(start)] = 0

    # 当优先队列非空的时候
    while not frontier.empty():
        # 得到f(x)最小的节点
        min_cost_node = frontier.get()[1]
        # 如果是目标节点则结束
        if min_cost_node == goal:
            break
        min_cost_node_s = to_str(min_cost_node)
        # 否则对该节点的相邻节点进行遍历
        for neighbour in neighbours(min_cost_node):
            new_cost = cost_so_far[min_cost_node_s] + 1  # 实际成本加一
            # 如果还没遍历，或者得到了更小的实际成本
            neighbour_s = to_str(neighbour)
            if neighbour_s not in cost_so_far or new_cost < cost_so_far[neighbour_s]:
                # 更新路径矩阵和实际成本矩阵
                come_from[neighbour_s] = min_cost_node_s
                cost_so_far[neighbour_s] = new_cost
                # 计算f(x)，实际成本+估计成本
                priority = new_cost + heuristic(neighbour)
                # 加入优先队列
                frontier.put((priority, neighbour))
    return cost_so_far, come_from


def iterative_deepening_a_star_search(start):
    limit = 0
    cost_so_far = None
    come_from = None

    while True:
        # 初始化:
        cost_so_far = {}
        come_from = {}
        if IDA_star_helper("", start, 0, limit, cost_so_far, come_from):
            break
        limit = limit + 1
    return cost_so_far, come_from


def IDA_star_helper(prior: str, node, cost_now, limit, cost_so_far, come_from):
    priority = cost_now + heuristic(node)
    # 超出深度限制了就返回False
    if priority > limit:
        return False
    # 如果已经有了，并且其的实际花费更小则返回
    node_s = to_str(node)
    if node_s in cost_so_far and cost_so_far[node_s] <= cost_now:
        return False
    # 递归的查找
    cost_so_far[node_s] = cost_now
    come_from[node_s] = prior
    # 找到了就返回True
    if node == goal:
        return True
    for neighbour in neighbours(node):
        if IDA_star_helper(node_s, neighbour, cost_now + 1, limit, cost_so_far, come_from):
            return True

    return False


def trace_back(come_from: dict):
    prior = come_from[to_str(goal)]
    path = [to_str(goal)]
    # 如果prior不为None就继续向前找
    while prior:
        path.append(prior)
        prior = come_from[prior]
    path.reverse()
    return path
