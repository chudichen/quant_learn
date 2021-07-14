"""
用来创建交易策略，生成交易信号
"""
import data.stock as st
import numpy as np
import matplotlib.pyplot as plt
import calculate_strategy.base as ba


def week_period_strategy(code, time_freq, start_date, end_date):
    # 新建周期字段
    data = st.get_single_price(code, time_freq, start_date, end_date)
    data['weekday'] = data.index.weekday
    # 周四买入
    data['buy_signal'] = np.where(data['weekday'] == 3, 1, 0)
    # 周一卖出
    data['sell_signal'] = np.where(data['weekday'] == 0, -1, 0)

    # 整合信号
    data = ba.compose_signal(data)
    # 计算收益
    data = ba.calculate_prof_pct(data)
    data = ba.calculate_max_drawdown(data)
    data = ba.calculate_cum_prof(data)
    return data


if __name__ == '__main__':
    df = week_period_strategy('159949.XSHE', 'daily', '2021-01-01', '2021-07-06')
    # print(df)
    # df[['cum_profit']].plot()
    # plt.show()
    print(df)
