import numpy as np
"""
缺失值
"""

# 缺失值在分析中也是信息的一种，NumPy提供nan作为缺失值的记录，通过isnan判定
a = np.random.rand(2, 2)
a[0, 1] = np.nan
print(np.isnan(a))

# nan_to_num可以将nan代替为0
print(np.nan_to_num(a))