"""
双均线策略
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import calculate_strategy.base as strat


def ma_strategy(data, short_window=5, long_window=20):
    """
    双均线策略
    :param data: 投资标的行情数据(必须包含收盘价)
    :param short_window: 短期n日移动平均线，默认5
    :param long_window: 长期n日移动平均线，
    :return:
    """
    print("当前周期参数：MA%d，MA%d", short_window, long_window)
    data = pd.DataFrame(data)
    # 计算技术指标：ma短期、ma长期
    data['short_ma'] = data['close'].rolling(window=short_window).mean()
    data['long_ma'] = data['close'].rolling(window=long_window).mean()

    # 生成信号：金叉买入、死叉卖出
    data['buy_signal'] = np.where(data['short_ma'] > data['long_ma'], 1, 0)
    data['sell_signal'] = np.where(data['short_ma'] < data['long_ma'], -1, 0)

    show_strategy(data)

    # 过滤信号：
    data = strat.compose_signal(data)

    # 计算单词收益
    data = strat.calculate_prof_pct(data)

    # 计算累计收益
    data = strat.calculate_cum_prof(data)

    # 删除多余的columns
    data.drop(labels=['buy_signal', 'sell_signal'], axis=1)

    # 数据预览
    return data


def show_strategy(data):
    data[['short_ma', 'long_ma']].plot()
    plt.legend()
    plt.title('Detail of Ma Strategy Profits')
    plt.show()


def show_result(data):
    # 存放累计收益率
    # 折线图
    data = data[data['signal'] != 0]
    # 数据预览
    print('开仓次数：', int(len(data)))
    print(data[['close', 'signal', 'profit_pct', 'cum_profit']])
    data['cum_profit'].plot()
    plt.legend()
    plt.title('Comparison of Ma Strategy Profits')
    plt.show()
