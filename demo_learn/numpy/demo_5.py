import numpy as np

# 数组和矩阵元素的访问方式可以通过下标来访问
a = np.array([[3.2, 1.5], [2.5, 4]])
print(a[0][1])
print(a[0, 1])

# 可以通过下标来改变访问数组元素的值
# 直接赋值是传递地址
b = a
a[0][1] = 2.0
print("a: \n", a)
print("b: \n", b)

# 采用深拷贝才是重新创建
a = np.array([[3.2, 1.5], [2.5, 4]])
b = a.copy()
a[0][1] = 2.0
print("a: \n", a)
print("b: \n", b)

# 若对a重新赋值，即将a指向其他地址，b仍在原来的地址
a = np.array([[3.2, 1.5], [2.5, 4]])
b = a
a = np.array([[2, 1], [9, 3]])
print("a: \n", a)
print("b: \n", b)

# 可以访问到某一维的全部数据，再访问到指定列
a = np.arange(20).reshape(4, 5)
print("a: \n", a)
print("the 2 and 4 column of a: \n", a[:, [1, 3]])

# 复杂一点的场景，尝试取满足条件的元素，例如：取第一列大于5的行中的第3个元素
print("greater than 5: \n", a[:, 2][a[:, 0] > 5])

# 也可以使用where函数来查看特定值在数组中的位置
loc = np.where(a == 11)
print("where:", loc)
