import numpy
import numpy as np
import random  # 抽样


class KMeans:
    def __init__(self, n_clusters):
        self.labels_ = None
        self.__n_clusters = n_clusters

    def fit(self, X: np.ndarray):
        """
        训练模型
        1.挑出随机点作为初始的中心点
        2.依据中心点进行分类
        3.对每一类计算新的中心点
        4.如果中心点没有变化，则保存结果，否则用新的中心点代替之前的中心点转2
        :param X: 特征矩阵
        :return: 对象自身
        """
        # 挑选出随机点
        row_length = X.shape[0]
        col_length = X.shape[1]
        centrals_index: list = random.sample(range(row_length), self.__n_clusters)
        centrals = X[centrals_index, :]
        labels = []
        # 2,3步
        while True:
            for point in X:
                # 通过计算欧几里得距离来分类
                distance = np.linalg.norm(centrals - point, axis=1)
                labels.append(np.argmin(distance))
            labels = np.array(labels)
            # 计算中心点,用每一类点的特征均值作为新的中心点
            new_centrals = np.zeros((self.__n_clusters, col_length))
            for label in numpy.unique(labels):
                new_centrals[label] = np.mean(X[labels == label, :],
                                              axis=0)  # 在列方向上求均值,这里label刚好是从0到np.__n_clusters-1
            # 如果中心点发生了改变就重复上述步骤，否则保存标签
            if (np.sort(new_centrals, axis=0) != np.sort(centrals, axis=0)).any():
                centrals = new_centrals
                # 重新分类
                labels = []
            else:
                break
        self.labels_ = np.array(labels)
        return self
