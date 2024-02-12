import ReadData  # 读取数据
import numpy  # 用于创建矩阵
import Search  # 用于搜索

# 预处理一下这个迷宫地图，变成二维数组
maze_map = ReadData.read_data('Labyrinth.txt')
for index, row in enumerate(maze_map):
    maze_map[index] = list(row)

# 找到这个迷宫的起点
start_point = []
for row in range(len(maze_map)):
    for col in range(len(maze_map[0])):
        if maze_map[row][col] == 'S':
            start_point = (row, col)

limit = 0
while True:
    limit = limit + 1  # 迭代加深
    # 初始化搜索条件
    visited = numpy.zeros((len(maze_map), len(maze_map[0])), dtype=numpy.int64)
    Search.maze_map = maze_map

    # 搜索
    Search.IDFS(start_point, visited, [], limit)
    final_path = Search.final_path

    # 如果有路径：
    if final_path:
        # 显示路径
        Path_Display = [[' ' for _ in range(len(maze_map[0]))] for _ in range(len(maze_map))]

        for path in final_path[1:len(final_path) - 1]:
            Path_Display[path[0]][path[1]] = "o"
        Path_Display[final_path[0][0]][final_path[0][1]] = "S"
        Path_Display[final_path[-1][0]][final_path[-1][1]] = "E"

        for row in Path_Display:
            print(''.join(row))
        print(f'路径长度:{limit}')
        break
