# 1.首先对对子句集S0
# 2.对每对子句进行判断，如果可以进行归结推理，则将进行归结推理的两个文字删掉
# 然后将这两个子句的其他文字作为一个子句放入下一层的子句集中，并需要记录其的两个母式
# 3.得到第一层子句集S1,对S1内部子句和S1和S0的子句执行同样的操作得到S2
# 4.以此类推，将Sn中的子句和Sn...S0的子句进行比较得到Sn+1.直到出现NIL为止

# 变量集：

import ReadData
import reasoning

levels = [ReadData.read_data('Block World')]
levels[0] = reasoning.preHandle(levels[0])

# 用初始条件初始化
for clause in levels[0]:
    reasoning.record[','.join(clause)] = "初始条件"
print(reasoning.record)

# 计算第二层
count = 1
while [] not in levels[-1] and levels[-1]:
    levels.append(reasoning.next_level(levels))
    print(f'第{count}次:')
    count = count + 1
    for index, level in enumerate(levels, start=1):
        print(f'第{index}层:\n{level}')
    print()
# 回溯推理过程
record = reasoning.record


def look_back(word: str, record: dict):
    if (word not in record):
        return
    if word == "":
        print(f'"NIL":{record[word]}')
    else:
        print(f'[{word}]:{record[word]}')
    father = record[word].split("+")
    for each_father in father:  # 递归回溯
        each_father = each_father.strip('[')  # 因为列表转字符串的时候会多了列表的符号，去掉
        each_father = each_father.strip(']')
        each_father = each_father.replace("'", "")  # 把所有'换掉，列表转字符串的时候出现的
        each_father = each_father.replace(" ", "")  # 把所有空格换掉，列表转字符串的时候出现的
        # print(each_father)
        look_back(each_father, record)


look_back("", record)
