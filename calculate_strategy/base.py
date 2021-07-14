import numpy as np
import pandas as pd


def evaluate_strategy(data):
    """
    评估策略收益表现
    :param data: dataframe,包含单词收益率数据
    :return: 评估指标
    """
    # 评估策略效果，总收益率、年化收益率、最大回撤、夏普比
    data = calculate_cum_prof(data)
    # 获取总收益率
    total_return = data['cum_profit'].iloc[-1]
    # 计算年化收益率(每月开仓)
    annual_return = data['profit_pct'].mean() * 12
    # 计算近一年最大回撤
    data = calculate_max_drawdown(data, window=12)
    # 获取近一年最大回撤
    max_drawdown = data['max_dd'].iloc[-1]
    # 计算夏普比率
    sharpe, annual_sharpe = calculate_sharpe(data)
    # 放到dict中
    results = {'总收益率': total_return, '年化收益率': annual_return, '最大回撤': max_drawdown, '夏普比率': annual_sharpe}
    print(results)
    return data


def compose_signal(data):
    """
    整合信号
    :param data: 数据
    :return:
    """
    data['buy_signal'] = np.where((data['buy_signal'] == 1)
                                  & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1)
                                   & (data['sell_signal'].shift(1) == -1), 0, data['sell_signal'])
    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data


def calculate_prof_pct(data):
    """
    计算单次收益率：开仓、平仓（开仓的全部股票数量）
    :param data: 数据
    :return: 收益率
    """
    # 筛选
    data = data[data['signal'] != 0]
    data['profit_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    data = data[data['signal'] == -1]
    return data


def calculate_cum_prof(data):
    """
    计算累计收益率
    :param data: 数据
    :return: 累计收益率
    """
    data['cum_profit'] = pd.DataFrame(1 + data['profit_pct']).cumprod() - 1
    return data


def calculate_max_drawdown(data, window=252):
    """
    计算最大回撤比
    :param window: 窗口时间
    :param data: 数据
    :return: 收益率
    """
    # 模拟持仓金额：投入的总金额 × (1+收益率)
    data['close'] = 10000 * (1 + data['cum_profit'])
    # 选取时间周期中的最大净值
    data['roll_max'] = data['close'].rolling(window=window, min_periods=1).max()
    # 计算当天的回撤比
    data['daily_dd'] = data['close'] / data['roll_max'] - 1
    # 选取时间周期内最大的回撤比，即最大回撤
    data['max_dd'] = data['daily_dd'].rolling(window, min_periods=1).min()
    return data


def calculate_sharpe(data):
    """
    计算夏普比率，返回的是年化的夏普比率
    :param data: 数据
    :return: 夏普比率
    """
    # 公式：sharpe = (回报率的均值 - 无风险利率) / 回报率的标准差
    daily_return = data['profit_pct'].pct_change()
    avg_return = daily_return.mean()
    sd_return = daily_return.std()
    # 计算夏普：每日收益率 × 252 = 每年收益率
    sharpe = avg_return / sd_return
    sharpe_year = sharpe * np.sqrt(252)
    return sharpe, sharpe_year


def calculate_portfolio_return(data, signal, n):
    """
    计算组合收益率
    :param data: dataframe
    :param signal: dataframe
    :param n: int
    :return returns: dataframe
    """
    returns = data.copy()
    # 投组收益率（等权重）= 收益率之和 / 股票个数
    returns['profit_pct'] = (signal * returns.shift(-1)).T.sum() / n
    returns = calculate_cum_prof(returns)
    return returns.shift(1)  # 匹配对应的交易月份