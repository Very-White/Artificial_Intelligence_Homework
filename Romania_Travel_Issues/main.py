import ReadData
import City

content = ReadData.read_data('Romania.txt')  # 读取文本文件中的数据
del content[0]  # 把第一行不知道有什么用的信息给删掉了
cities = City.Cities(content)

with open('log','w') as file:
    pass
while True:
    if_inquire = input("是否需要查询y/n:")
    if if_inquire != 'y':
        break
    city1 = input("请输入您要查询的始发城市:")
    city2 = input("请输入您要查询的终点城市:")
    path, distance = cities.inquire(city1, city2)
    print(path, " ", "distance=", distance)
print("程序结束")
