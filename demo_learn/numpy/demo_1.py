import numpy as np

v = np.version.full_version
print(v)

# Numpy中的积累对象是同类型的多维数组，这与C++中的数组是一致的。
a = np.arange(20)
print(a)

# 通过函数reshape，我们可以重新构造一下这个数组。
a = a.reshape(4, 5)
print(a)

# 更高维的也没有问题
a = a.reshape(2, 2, 5)
print(a)

# 既然a是array，我们还可以调用array的函数进一步查看a的相关属性：ndim查看维度；shape查看各个维度的大小
# size查看全部元素个数，等于各个维度大小的乘机；dtype可查看元素类型，dsize查看元素占位（bytes）大小。
print("维度:", a.ndim)
print("各个维度的大小：", a.shape)
print("元素个数：", a.size)
print("元素类型:", a.dtype)
