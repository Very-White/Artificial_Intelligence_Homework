import pandas as pd
import numpy as np


class KNN:
    def __init__(self):
        self.__k = None
        self.__Xtrain = None
        self.__y_train = None

    def fit(self, X_train: np.ndarray, y_train: np.ndarray, k: int):
        """
        训练模型
        :param X_train: 训练集的特征矩阵
        :param y_train: 训练集的目标向量
        :param k: 超参数k
        :return: 
        """
        self.__Xtrain = X_train
        self.__y_train = y_train
        self.__k = k
        return self

    def predict(self, X_predict: np.ndarray):
        """
        根据训练好的模型做预测
        :param X_predict: 需要预测的特征矩阵
        :return: 预测完的目标向量
        """
        # 对每个需要预测的特征向量计算曼哈顿距离
        # 存储预测的变量
        y_predict = []
        for x_predict in X_predict:
            # 计算每个点的曼哈顿距离
            manhattan_distance = np.abs(self.__Xtrain - x_predict)
            # 求和，得到跟每个样本的距离
            manhattan_distance = np.sum(manhattan_distance, axis=1)
            data_train = pd.DataFrame({
                "distance": manhattan_distance,
                "label": self.__y_train
            })
            data_train = data_train.sort_values(by='distance', ascending=True)
            # 获取前k个最相邻元素的label
            head_k_label = data_train['label'].head(self.__k)
            # 取最多的第一个标签（众数）
            y_predict.append(head_k_label.mode()[0])

        return np.array(y_predict)

    def score(self, X_test: np.ndarray, y_test: np.ndarray):
        """
        计算正确率
        :param X_predict: 需要预测的特征矩阵
        :return: 正确率
        """
        y_predict = self.predict(X_test)
        return np.sum(y_test == y_predict) / y_test.size
