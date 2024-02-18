import numpy as np

# 定义一个包含重复元素的NumPy数组
array = np.array([1, 2, 2])
b=np.array([1,2,3])

# 使用np.unique()获取数组中的唯一元素

print(array!=b)
print((array!=b).any())