import numpy as np

# 数组的创建可通过转换列表实现，高维数组可通过转换嵌套列表实现：
raw = [0, 1, 2, 3, 4]
a = np.array(raw)
print(a)

raw = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
b = np.array(raw)
print(b)

# 一些特殊的数组有特别定制的命令生成，如4*5的全零矩阵：
d = (4, 5)
a = np.zeros(d)
print(a)

# 默认生成的是浮点型，可以通过指定类型改为整型：
d = (4, 5)
a = np.ones(d, dtype=int)
print(a)

# 生成区间在[0, 1)的随机数组：
a = np.random.rand(5)
print(a)