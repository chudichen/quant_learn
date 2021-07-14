import data.stock as st

# 调用一直股票的行情数据
code = '159949.XSHE'

data = st.get_csv_price(code, '2021-07-01', '2021-07-05')

print(data)
