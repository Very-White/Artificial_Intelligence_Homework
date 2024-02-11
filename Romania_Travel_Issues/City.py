import numpy


class Cities:
    """
    Cities初始化的时候需要传入一个列表，列表中的元素的形式为“城市A 城市B 距离”
    Cities的方法有
        查询两个城市之间的距离和路径：inquire
        获得距离矩阵：GetDistanceMatrix
        获得路径矩阵:GetPathMatrix

    """
    __cities = None
    __cities_amount = None
    __Distance = None
    __Path = None

    def inquire(self, city1: str, city2: str):
        """
        获得两个城市之间的最短路径长度和最短路径
        :param city1:城市一的名称（不区分大小写，也可以用首字母缩写代替）
        :param city2:城市二的名称 （不区分大小写，也可以用首字母缩写代替）
        :return:城市间路径（list），城市间的距离
        """
        # 得到城市的下标索引
        index1 = None  # 第一个城市的索引
        index2 = None  # 第二个城市的索引
        for i in range(self.__cities_amount):
            if self.__cities[i].title().startswith(city1.title()):
                index1 = i
            if self.__cities[i].title().startswith(city2.title()):
                index2 = i

        if index1 is None or index2 is None:
            with open('log', 'a') as file:
                file.write(f'{city1} to {city2}: Not valid city!\n')  # 写入日志文件
            return ["Not valid city"], 0
        # 判断是否有路径
        if self.__Distance[index1][index2] == numpy.iinfo(numpy.int64).max:
            with open('log', 'a') as file:
                file.write(f'{self.__cities[index1]} to {self.__cities[index2]}: Can\'t reach!\n')  # 写入日志文件
            return ["None"], numpy.iinfo(numpy.int64).max

        # 得到路径
        path: list = [self.__cities[index1]]
        index = index1
        while index != index2:
            path.append(self.__cities[self.__Path[index][index2]])
            index = self.__Path[index][index2]  # 更新下一个起点城市
        with open('log', 'a') as file:
            file.write(f'{self.__cities[index1]} to {self.__cities[index2]}: {path} '
                       f'distance:{self.__Distance[index1][index2]}\n')  # 写入日志文件
        return path, self.__Distance[index1][index2]

    def GetPathMatrix(self):
        return self.__Path.copy()

    def GetDistanceMatrix(self):
        return self.__Distance.copy()

    def __init__(self, content: list):
        # 获取城市的数据
        if type(content) is not list or type(content[0]) is not str:
            raise "您传入的列表中的元素类型不是字符串"
        self.__cities = set()
        for line in content:
            cities_and_distance = line.split()  # 拆开字符串
            self.__cities.add(cities_and_distance[0])
            self.__cities.add(cities_and_distance[1])
        cities_amount = len(self.__cities)
        self.__cities_amount = cities_amount
        # 初始化
        max_int = numpy.iinfo(numpy.int64).max
        self.__Distance = numpy.full((cities_amount, cities_amount), max_int, dtype=numpy.int64)
        self.__Path = numpy.zeros((cities_amount, cities_amount), dtype=numpy.int64)
        # 根据给定的各个城市之间的距离初始化路径矩阵和距离矩阵
        # 将无序的集合转为有序的列表
        self.__cities = list(self.__cities)

        for line in content:
            cities_and_distance = line.split()
            IndexOfCity1 = self.__cities.index(cities_and_distance[0])
            IndexOfCity2 = self.__cities.index(cities_and_distance[1])
            distance = int(cities_and_distance[2])
            self.__Distance[IndexOfCity1][IndexOfCity2] = distance
            self.__Distance[IndexOfCity2][IndexOfCity1] = distance
            self.__Path[IndexOfCity1][IndexOfCity2] = IndexOfCity2
            self.__Path[IndexOfCity2][IndexOfCity1] = IndexOfCity1

        # 再重新设置Path矩阵中对角线上的元素
        for i in range(cities_amount):
            self.__Path[i][i] = i

        # 弗洛伊德算法计算路径矩阵和距离矩阵
        for k in range(cities_amount):
            for row in range(cities_amount):
                for col in range(cities_amount):
                    if (int(self.__Distance[row][k]) + int(self.__Distance[k][col])) < int(self.__Distance[row][col]):
                        self.__Distance[row][col] = self.__Distance[row][k] + self.__Distance[k][col]
                        self.__Path[row][col] = k
