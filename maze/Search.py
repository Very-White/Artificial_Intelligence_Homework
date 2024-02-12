maze_map = []
final_path = []


# 判断是否超出了数组的边界
def OutOfMaze(position: list):
    global maze_map
    x = position[0]  # 代表的是行
    y = position[1]  # 代表的是列
    if x not in range(len(maze_map)) or y not in range(len(maze_map[0])):
        return True
    else:
        return False


# 四个方向
directions = [[0, 1], [1, 0], [-1, 0], [0, -1]]


def DFS(position: list, visited, path: list):
    """
    深度优先搜索
    :param position: 位置
    :param visited: 判断是否访问过
    :param path:记录路径
    :return:是否找到终点T/F
    """
    # 如果超出了范围的话就返回
    if OutOfMaze(position):
        return False  # 没有找到终点
    x = position[0]
    y = position[1]
    global maze_map
    if visited[x][y] or maze_map[x][y] == '1':  # 如果遇到路障就回去
        return False
    else:
        visited[x][y] = 1  # 记录下已经访问过了
        path.append(position)  # 记录下路径
        if maze_map[x][y] == 'E':  # 找到终点
            global final_path
            final_path = path
            return True
        # 否则递归搜索
        global directions
        for direction in directions:
            if DFS([x + direction[0], y + direction[1]], visited, path.copy()):
                return True


def IDFS(position: list, visited, path: list, limit: int, count=0):
    """
    迭代一致加深+深度优先搜索
    :param position: 位置
    :param visited: 判断是否访问过
    :param path:记录路径
    :return:是否找到终点T/F
    """
    # 如果超出了范围的话就返回
    if OutOfMaze(position):
        return False  # 没有找到终点
    x = position[0]
    y = position[1]
    global maze_map
    if visited[x][y] or maze_map[x][y] == '1':  # 如果遇到路障就回去
        return False
    else:
        # 如果超过了限制就返回,遇到路障'1'还有访问已访问的地方都不算路径长度
        count = count + 1
        if count > limit:  # 刚开始的第一次是1，随后每次加一
            return False  # 因为这里还没有访问，所以不用设置vistied
        visited[x][y] = 1  # 记录下已经访问过了
        path.append(position)  # 记录下路径
        if maze_map[x][y] == 'E':  # 找到终点
            global final_path
            final_path = path
            return True
        # 否则递归搜索
        global directions
        for direction in directions:
            if IDFS([x + direction[0], y + direction[1]], visited, path.copy(), limit, count):
                return True
        visited[x][y] = 0  # 或许还有更短的路径，还能进行下一次的搜索。否则可能一条长路径把本来短路径可以访问的地方给截断了
