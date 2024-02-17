from ReadData import read_data  # 读取数据
from sklearn.feature_extraction.text import TfidfVectorizer  # 提取特征
from sklearn.model_selection import train_test_split  # 划分训练集和测试集
import pandas as pd
import numpy as np
from KNN import KNN

# 读取文件
ban_words = read_data('ban.txt')
data_set = read_data('data')
# 删掉第一行的注释
del data_set[0]
ban_words = set(ban_words)  # 转化为集合方便查找


def get_data(data, ban_words: set):
    """
    切分句子为词语，将emotion的类别单独提取出来,并在过程中去掉停用词
    :param data: 数据集
    :param ban_words: 禁用词
    :return: 训练特征X，训练标签Y
    """
    x = []
    y = []
    # 得到数据集的x和y
    for line in data:
        line = line.split()  # 按空格划分
        del line[0]  # 删掉行ID
        y.append(int(line[0]))  # 标签
        del line[0]  # 删掉标签
        words = []  # 该行有效的单词
        for word in line:
            if word not in ban_words:
                words.append(word)
        x.append(' '.join(words))  # 为了给tf-idf提取特征，所以还需要将其连成一句
    return np.array(x), np.array(y)


# 得到原始的的特征矩阵x和目标向量y
origin_x, origin_y = get_data(data_set, ban_words)
# 划分数据集，划分为训练集：测试集=8:2
X_train, X_test, y_train, y_test = train_test_split(origin_x, origin_y, test_size=0.2, random_state=420)

# 用sklearn提供的tf-idf提取特征
tfidf = TfidfVectorizer(use_idf=True, smooth_idf=True, norm='l2')
# 提取特征
X_train_fit = tfidf.fit_transform(X_train).toarray()
X_test_fit = tfidf.transform(X_test).toarray()

diff_k = []
diff_score = []
for k in range(1, 200):
    knn = KNN().fit(X_train_fit, y_train, k)
    # 计算对测试集的准确率
    score = knn.score(X_test_fit, y_test)
    diff_k.append(k)
    diff_score.append(score)

df = pd.DataFrame({
    '超参数': diff_k,
    '分数': diff_score
})
df.to_excel('result.xlsx', index=False)
