import calculate_strategy.ma_strategy as ma
import data.stock as stock
import calculate_strategy.hot_stock as hot


res = hot.get_hot_stock_from_sina()
print(res)
# 创业版50
# code = '159949.XSHE'
code = '300059.XSHE'
start_time = '2021-01-01'

data = stock.get_csv_price(code, start_time)
data = ma.ma_strategy(data)
ma.show_result(data)


