from ReadData import read_data  # 读取数据
from sklearn.feature_extraction.text import TfidfVectorizer  # 提取特征
from sklearn.naive_bayes import ComplementNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import numpy as np

# 读取文件
ban_words = read_data('ban.txt')

train_dataset = read_data('train.txt')
test_dataset = read_data('test.txt')
# 删掉第一行的注释
del train_dataset[0]
del test_dataset[0]
ban_words = set(ban_words)  # 转化为集合方便查找


def get_data(data_set, ban_words: set):
    """
    切分句子为词语，将emotion的类别单独提取出来,并在过程中去掉停用词
    :param data_set: 数据集
    :param ban_words: 禁用词
    :return: 训练特征X，训练标签Y
    """
    x = []
    y = []
    # 得到数据集的x和y
    for line in data_set:
        line = line.split()  # 按空格划分
        del line[0]  # 删掉行ID
        y.append(int(line[0]))  # 标签
        del line[0]  # 删掉标签
        words = []  # 该行有效的单词
        for word in line:
            if word not in ban_words:
                words.append(word)
        x.append(' '.join(words))  # 为了给tf-idf提取特征，所以还需要将其连成一句
    return x, y


# 得到测试集和训练集的x和y
train_x, train_y = get_data(train_dataset, ban_words)
test_x, test_y = get_data(test_dataset, ban_words)

# 用sklearn提供的tf-idf提取特征
tfidf = TfidfVectorizer(use_idf=True, smooth_idf=True, norm='l2')
# 提取特征
train_x_feature = tfidf.fit_transform(train_x).toarray()
test_x_feature = tfidf.transform(test_x).toarray()

# 下面用了sklearn中提供的贝叶斯分布
# 高斯朴素贝叶斯,准确率：0.537
# gnb = GaussianNB().fit(train_x_feature, train_y)

# 补充普通贝叶斯，准确率0.98
gnb = ComplementNB().fit(train_x_feature, train_y)

# 多项式补充贝叶斯，准确率0.791
# gnb = MultinomialNB().fit(train_x_feature, train_y)

# 查看对测试集的准确度
acc_score = gnb.score(test_x_feature, test_y)
print("acc_score=", acc_score)

# 得到预测的结果
y_pred = gnb.predict(test_x_feature)

# 作个表格
table = pd.DataFrame(
    {
        "sentence": test_x,
        "predict": y_pred,
        "actual": test_y,
        "Same": y_pred == test_y
    }
)
# table.to_excel("result.xlsx", index=False)
print(table)
