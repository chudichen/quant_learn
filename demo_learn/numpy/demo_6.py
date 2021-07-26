import numpy as np
"""
数组操作
"""

# 还是拿矩阵作为例子，首先来看矩阵转置：
a = np.random.rand(2, 4)
print("a: \n", a)
a = np.transpose(a)
print("a is an array, by using transpose(a): \n", a)

b = np.random.rand(2, 4)
b = np.mat(b)
print("b:\n", b)
print("b is a matrix, by using b.T: \n", b.T)