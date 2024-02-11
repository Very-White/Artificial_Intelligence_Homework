def read_data(file_name):
    """
    读取txt文件中的每行的信息
    :param file_name: 文件名
    :return: 一个包含了文件中每行信息的列表
    """
    with open(file_name, 'r') as file:
        content = file.readlines()
    for i in range(0, len(content)):
        content[i] = content[i].strip()
    return content
