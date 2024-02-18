from ReadData import read_data  # 读取数据
from sklearn.feature_extraction.text import TfidfVectorizer  # 提取特征
from KMeans import KMeans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

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


# 得到特征矩阵x和目标向量y
X, y = get_data(data_set, ban_words)
# tf-idf提取特征
tfidf = TfidfVectorizer(use_idf=True, smooth_idf=True, norm='l2')
X = tfidf.fit_transform(X).toarray()

# 进行Kmeans聚类
cluster = KMeans(n_clusters=6).fit(X)
y_clus = cluster.labels_

# 下面的代码都是可视化:
# pca降维,降为2维
pca = PCA(n_components=2)
X_dr = pca.fit_transform(X)
# 查看总信息量，降维后基本将所有的信息都丢失了
# print(pca.explained_variance_ratio_.sum())
# 将降维后的点与原始标签画出来
classification = list(set(y.tolist()))
plt.figure()
for i in classification:
    plt.scatter(X_dr[y == i, 0], X_dr[y == i, 1], label=f'{i} group',
                alpha=0.7)
plt.legend()
plt.title('origin')
# 将聚类的结果画出来
classification = list(set(y_clus.tolist()))
plt.figure()
for i in classification:
    plt.scatter(X_dr[y_clus == i, 0], X_dr[y_clus == i, 1], label=f'{i+1} group',
                alpha=0.7)
plt.legend()
plt.title('Kmeans')
# 显示图像
plt.show()
