Variable_set = ('x', 'y', 'z', 'u', 'v', 'w')
record = {}


def preHandle(content):
    # 预处理
    for i in range(len(content)):
        clauses = content[i]
        if (clauses.startswith("(")):
            count = 0
            index = [0]
            for j in range(len(clauses)):
                if clauses[j] == "(":
                    count = count + 1
                elif clauses[j] == ")":
                    count = count - 1
                elif clauses[j] == ",":
                    if count == 1:  # 找到一个需要分割的地方
                        index.append(j)
            index.append(len(clauses))
            splited_clauses = []
            for j in range(len(index) - 1):
                splited_clauses.append(clauses[index[j]:index[j + 1]])
            clauses = splited_clauses
        else:
            clauses = [clauses]
        for j in range(len(clauses)):
            clause = clauses[j]
            clause = clause.strip(",")  # 去掉前后的逗号
            clause = clause.strip()  # 去掉前后的空格
            clause = clause.strip('(')  # 去掉前面的'('
            clause = clause.replace("))", ')')  # 将))换为')'
            clause = clause.replace(" ", "")  # 删除空格
            clauses[j] = clause
        content[i] = clauses
    return content


def getvariables(formula: str):
    """
    以一个列表的方式返回文字中的所有变量
    :param formula:文字
    :return: 返回文字中的变量
    """
    begin = formula.index('(')
    end = formula.index(')')
    variables = formula[begin + 1:end]
    variables.strip()
    variables = variables.split(',')
    return variables


def match(formula1: str, formula2: str):
    """
    判断两个文字是否满足归结推理的要求
    :param formula1:文字1
    :param formula2:文字2
    :return: 如果不满足则返回False,如果满足，在加入下一层的时候不需要操作则返回[]，如果需要操作
    则以[需要操作的子句（1/2），需要替换的变量"x",需要替换成的变量"y"]
    """
    # 如果不是只有一个式子有否定词，则不能进行归结推理
    if "¬" in formula1 and "¬" in formula2:
        return False
    if "¬" not in formula1 and "¬" not in formula2:
        return False
    # 如果前缀名称都不同，则不进行归结推理
    test1 = formula1.strip('¬')
    test2 = formula2.strip('¬')
    end = test1.index('(')
    if not test2.startswith(test1[0:end]):
        return False
    # 有以下几种情况是可以进行归结推理的
    # 第一种情况：f(a,b)和¬f(a,b)或¬f(a,b)和f(a,b)。或者是f(x,y)和¬f(x,y)或¬f(x,y)和f(x,y)
    # if '¬'.join(formula1) == formula2 or formula1 == '¬'.join(formula2):
    #     return []  # []表示加入下一层的时候不需要操作#合并到第二种
    # 第二种情况:f(a,y)和¬f(x,b)(其中x是一个变量)。那么只需要每一项其中一个式子有变量即可
    global Variable_set
    variables1: list = getvariables(formula1)
    variables2: list = getvariables(formula2)
    if len(variables1) != len(variables2):
        return False  # 不能进行归结推理
    else:
        length = len(variables1)

    operation = []
    for i in range(length):
        if variables1[i] == variables2[i]:  # 出现相同的就不管
            continue
        elif variables1[i] in Variable_set:  # 将式子1中所有的variables1 替换为variables2
            operation.append(1)
            operation.append(variables1[i])
            operation.append(variables2[i])
        elif variables2[i] in Variable_set:
            operation.append(2)
            operation.append(variables2[i])
            operation.append(variables1[i])
        else:  # 两个都不是变量，且两个都不相同，不能进行归结推理
            return False
    return operation


def next_level(clause_set: list):
    """
    根据当前已有的子句集，计算下一层的子句集
    :param clause_set: 当前已有的多个子句集
    :return: 下一层的子句集
    """
    global record  # 记录
    next_level_clause = []
    for i, sentence1 in enumerate(clause_set[-1], start=0):  # 对最后一层的每个子句
        sentence1 = sentence1.copy()  # 避免修改原始列表
        for level in clause_set[0:len(clause_set) - 1]:  # 对之前的每一层的子句集
            for j, sentence2 in enumerate(level, start=0):
                sentence2 = sentence2.copy()
                for word1 in sentence1:
                    for word2 in sentence2:
                        if_match = match(word1, word2)
                        if if_match != False:  # []也是假值
                            # print(f'{sentence1}:{word1}  {sentence2}:{word2}  {if_match}')
                            new_sentence1 = sentence1.copy()
                            new_sentence1.remove(word1)
                            new_sentence2 = sentence2.copy()  # 归结推理，消去元素
                            new_sentence2.remove(word2)
                            new_sentence1, new_sentence2 = change_variable(new_sentence1, new_sentence2, if_match)
                            new_sentence1.extend(new_sentence2)
                            # 查重并加入下一层
                            # 消重
                            new_sentence1 = list(set(new_sentence1))
                            if new_sentence1 not in next_level_clause and ','.join(new_sentence1) not in record:
                                next_level_clause.append(new_sentence1)
                                record[','.join(new_sentence1)] = f'{sentence1}+{sentence2}'
                                # print(sentence1,sentence2,next_level_clause)
        for j, sentence2 in enumerate(clause_set[-1][i + 1:], start=i + 1):  # 对最后一层的子句集
            sentence2 = sentence2.copy()
            for word1 in sentence1:
                for word2 in sentence2:
                    if_match = match(word1, word2)
                    if if_match != False:
                        # print(f'{sentence1}:{word1}  {sentence2}:{word2}  {if_match}')
                        new_sentence1 = sentence1.copy()
                        new_sentence1.remove(word1)
                        new_sentence2 = sentence2.copy()  # 归结推理，消去元素
                        new_sentence2.remove(word2)
                        new_sentence1, new_sentence2 = change_variable(new_sentence1, new_sentence2, if_match)
                        new_sentence1.extend(new_sentence2)
                        # 消重
                        new_sentence1 = list(set(new_sentence1))
                        # 查重并加入下一层
                        if new_sentence1 not in next_level_clause and ','.join(new_sentence1) not in record:
                            new_sentence1 = list(set(new_sentence1))
                            next_level_clause.append(new_sentence1)
                            record[','.join(new_sentence1)] = f'{sentence1}+{sentence2}'
                            # print(sentence1,sentence2,next_level_clause)
    return next_level_clause


def change_variable(sentence1: list, sentence2: list, operation):
    """

    :param sentence1: 第一个子句
    :param sentence2: 第二个子句
    :param operation: 执行的替换，格式为：[1/2(子句1或2)，要替换的变量:str，替换为的变量：str]
    :return:替换完的两个句子
    """
    replace_for_sentence1: dict = {}
    replace_for_sentence2: dict = {}  # 用字典存储替换操作
    for i in range(0, len(operation), 3):
        if operation[i] == 1:
            replace_for_sentence1[operation[i + 1]] = operation[i + 2]
        else:
            replace_for_sentence2[operation[i + 1]] = operation[i + 2]
    for index, word1 in enumerate(sentence1, start=0):
        word1 = list(word1)  # 方便接下来进行的替换
        for i in range(word1.index('(') + 1, word1.index(')')):  # 在这个范围进行替换
            if word1[i] in replace_for_sentence1:  # 如果需要替换则进行替换，这里不用考虑xx这样的变量，因为规定的变量就是单个字符的
                word1[i] = replace_for_sentence1[word1[i]]  # 替换
        word1 = ''.join(word1)  # 再转化为字符串
        sentence1[index] = word1
    for index, word2 in enumerate(sentence2):  # 同样的操作
        word2 = list(word2)  # 方便接下来进行的替换
        for i in range(word2.index('(') + 1, word2.index(')')):  # 在这个范围进行替换
            if word2[i] in replace_for_sentence2 and not word2[i - 1].isalpha() and not word2[
                i + 1].isalpha():  # 如果需要替换则进行替换，并且前后都不是字母（单个变量）
                word2[i] = replace_for_sentence2[word2[i]]  # 替换
        word2 = ''.join(word2)  # 再转化为字符串
        sentence2[index] = word2
    return sentence1, sentence2
