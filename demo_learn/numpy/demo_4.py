import numpy as np

# 科学计算中大量使用到矩阵运算，除了数组，NumPy同事提供了矩阵对象（matrix）
a = np.arange(20).reshape(4, 5)
a = np.asmatrix(a)
print(type(a))

b = np.matrix('1.0 2.0; 3.0 4.0')
print(type(b))

# 接下来测试一下矩阵乘法
b = np.arange(2, 45, 3).reshape(5, 3)
b = np.mat(b)
print("matrix a: \n", a)
print("matrix b: \n", b)
c = a * b
print("matrix c: \n", c)

# 使用linspace生成矩阵
t = np.linspace(0, 2, 9)
print("linspace: \n", t)
