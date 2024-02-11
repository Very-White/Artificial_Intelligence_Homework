# 罗马尼亚旅行问题实现

这个项目是关于罗马尼亚旅行问题的实现，其主要功能是计算任意两个城市之间的最短路径以及最短距离。

## 使用说明

1. **创建 Cities 对象**

在创建 `Cities` 对象时，你需要传入一个列表，列表中的每个元素是一个字符串，格式为 "城市A 城市B 距离"，例如 `["Arad Timisoara 118", "Arad Zerind 75"]`。


```python
cities = Cities(["Arad Timisoara 118", "Arad Zerind 75", ...])
```
2. **查询两个城市之间的距离和路径**

使用 `inquire` 方法查询两个城市之间的最短路径和距离。该方法接受两个字符串参数，分别为城市A和城市B的名称（不区分大小写，也可以用首字母缩写代替）。


```python
path, distance = cities.inquire("Arad", "Timisoara")
print(f"最短路径: {path}, 最短距离: {distance}")
```
3. **获取距离矩阵和路径矩阵**

你还可以使用 `GetDistanceMatrix` 和 `GetPathMatrix` 方法获取整个距离矩阵和路径矩阵。


```python
distance_matrix = cities.GetDistanceMatrix()
path_matrix = cities.GetPathMatrix()
```
## 注意事项

* 输入的城市名称列表中的元素必须是字符串，并且格式正确。
* 如果查询的城市不存在，或者两个城市之间没有路径，程序会记录相应的日志信息，并返回特定的结果。
* 本实现使用了弗洛伊德算法来计算最短路径和距离。

## 日志文件

程序在运行过程中会生成一个名为 `log` 的日志文件，记录查询结果和错误信息。你可以查看该文件以获取更多详细信息。
