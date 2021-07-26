import numpy as np

# 简单的四则运算已经重载过了，全部的+,-,*,/都是基于全部的数组元素的
a = np.array([[1.0, 2], [2, 4]])
print("a: \n", a)

b = np.array([[3.2, 1.5], [2.5, 4]])
print("b: \n", b)

print("a + b: \n", a + b)
print("3 * a: \n", 3 * a)
print("b + 1.8: \n", b + 1.8)

# 类似于C++的，+=,-=,*=,/=在NumPy中都是支持的
a /= 2
print("a /= 2: \n", a)

# 开根号求指数也很容器:
print("a: \n", a)
print("np.exp(a): \n", np.exp(a))
print("np.sqrt(1): \n", np.sqrt(a))
print("np.square(a): \n", np.square(a))
print("np.power(a, 3): \n", np.power(a, 3))

# 需要知道二维数组的最大最小值怎么办？想计算全部元素的和、按行求和、按列求和怎么办？for循环吗？不，NumPy有对应的内置函数。
a = np.arange(20).reshape(4, 5)
print("a: \n", a)
print("sum of all elements in a: ", str(a.sum()))
print("maximum element in a: ", str(a.max()))
print("minimum element in a: ", str(a.min()))
print("maximum element in each row of a: ", str(a.max(axis=1)))
print("minimum element in each column of a: ", str(a.min(axis=0)))
