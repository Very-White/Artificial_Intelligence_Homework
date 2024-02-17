# 项目说明

该项目是一个基于K近邻算法（KNN）的情感分类任务。它使用了自定义的KNN实现以及scikit-learn库提供的TF-IDF特征提取器。项目的目的是通过调整KNN算法中的超参数k来找到最佳的情感分类模型。

## 数据集

数据集包含两个文件：`ban.txt`和`data`。`ban.txt`包含停用词列表，用于在预处理阶段去除文本中的停用词。`data`文件包含情感分类的训练数据，其中每一行包含一个句子和其对应的情感标签。

## 代码流程

1. **数据预处理**：读取停用词列表和数据集，将数据集分为特征矩阵和目标向量，并在处理过程中去除停用词。
2. **特征提取**：使用scikit-learn的TF-IDF特征提取器将文本数据转换为数值特征向量。
3. **数据集划分**：将特征矩阵和目标向量划分为训练集和测试集，其中训练集用于训练模型，测试集用于评估模型性能。
4. **模型训练与评估**：使用自定义的KNN算法实现，在训练集上训练模型，并在测试集上评估模型的准确率。通过遍历不同的k值来找到最佳的模型。
5. **结果保存**：将不同k值对应的准确率保存到一个Excel文件中，方便后续分析和可视化。

## 自定义KNN实现

自定义的KNN类包含以下方法：

- `fit`：用于训练模型，实际上只是保存了训练数据和超参数k。
- `predict`：用于预测新数据的情感标签。它计算新数据与训练数据之间的曼哈顿距离，并根据最近的k个邻居的标签进行投票来决定新数据的标签。
- `score`：用于评估模型在测试集上的准确率。它首先使用`predict`方法对测试集进行预测，然后计算预测标签与真实标签之间的匹配程度来得到准确率。

注意：自定义的KNN实现可能不是最优化的，特别是在计算距离和排序时可能存在效率问题。在实际应用中，建议使用scikit-learn等成熟库提供的优化过的KNN实现。

## 运行说明

1. 确保已经安装了Python环境以及所需的库（如numpy、pandas、scikit-learn等）。
2. 将代码和数据集放置在同一目录下。
3. 运行代码，等待程序执行完毕。执行过程中可能会打印一些日志信息，以显示进度和结果。
4. 执行完毕后，会在当前目录下生成一个名为`result.xlsx`的Excel文件，其中包含不同k值对应的准确率数据。可以使用Excel或其他表格处理软件打开该文件进行查看和分析。