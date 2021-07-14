import calculate_strategy.momentum_strategy as mo
import calculate_strategy.base as ba


data = mo.get_data('2016-01-01', '2021-07-08', ['close', 'date'], '399673.XSHE')
res = mo.momentum(data)
