 # 迷宫搜索算法

## 简介

本项目包含用于解决迷宫问题的 Python 代码。通过深度优先搜索（DFS）和迭代加深搜索（IDFS）算法，找到从起点（S）到终点（E）的路径。

## 安装

确保您已经安装了 Python 和 NumPy 库。如果尚未安装，请使用以下命令安装：

```bash
pip install numpy
```

## 使用方法

1. 将迷宫地图保存为文本文件（例如 `Labyrinth.txt`），迷宫中的通路用'0'表示，墙壁用 '1' 表示，起点用 'S' 表示，终点用 'E' 表示。

2. 运行 `main.py` 文件，程序将读取迷宫地图并尝试找到从起点到终点的路径。

## 代码结构

- `ReadData.py`：包含读取迷宫地图txt文件的函数。将每行保存为一个字符串，所有行保存到一个列表中
- `numpy`：用于创建和操作visited矩阵。
- `Search.py`：包含搜索算法的实现。

## 主要函数

### `OutOfMaze(position: list)`

判断给定位置是否超出迷宫边界。

### `DFS(position: list, visited: numpy.array, path: list)`

执行深度优先搜索算法。

### `IDFS(position: list, visited: numpy.array, path: list, limit: int, count: int)`

执行迭代加深深度优先搜索算法，限制搜索深度。count默认为0，可以不用传入这个参数


## 注意事项

- 请确保迷宫地图文件的路径和文件名正确。
- 搜索深度限制 `limit` 可以根据迷宫大小和复杂度进行调整。
