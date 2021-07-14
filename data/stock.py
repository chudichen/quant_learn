"""
@author: chu
@software: pycharm
@time 2021/07/05
"""
from jqdatasdk import *
import pandas as pd
import datetime
import os.path as path

# 设置行列不忽略
pd.set_option('display.max_rows', 1000000)
pd.set_option('display.max_column', 1000)

# 全局变量
data_dir = '/home/chu/PycharmProjects/quant_learn/save_data/'


def login():
    """
    登录优矿
    :return:
    """
    auth("18102582460", "582460")


def init_db():
    """
    初始化股票数据库
    :return:
    """
    # 1. 获取所有股票代码
    stocks = get_stock_list()
    # 2. 存储到csv文件中
    for code in stocks:
        df = get_single_price(code, 'daily')
        export_data(df, code, 'price')


def get_stock_list():
    """
    获取所有A股列表
    上海证券交易所.XSHG
    深圳证券交易所.XSHE
    :return: stock_list
    """
    login()
    return list(get_all_securities(['stock']).index)


def get_index_list(index_symbol):
    """
    获取指数成分股，指数代码查询：https://www.joinquant.com/indexData
    :param index_symbol: 指数的代码，默认沪深300
    :return: list，成分股代码
    """
    login()
    return get_index_stocks(index_symbol)


def get_single_price(code, time_freq, start_date=None, end_date=None):
    """
    获取单个股票价格
    :param code: 股票代码
    :param time_freq: 时间间隔
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: 股票价格
    """
    login()
    # 如果start_date=None，默认为从上市日期开始
    if start_date is None:
        start_date = get_security_info(code).start_date
    if end_date is None:
        end_date = datetime.datetime.today()
    # 获取行情数据
    data = get_price(code, start_date=start_date, end_date=end_date,
                     frequency=time_freq, panel=False)  # 获取获得在2015年
    return data


def export_data(data, filename, type, mode=None):
    """
    导出股票相关数据
    :param type: 股票数据类型，可以是：price、finance
    :param data: 数据
    :param filename: 文件名字,可以是股票代码
    :param mode: a代表追加，none代码默认w写入
    :return: void
    """
    file_path = get_filepath(filename, type)
    data.index.names = ['date']
    if mode == 'a':
        data.to_csv(file_path, mode=mode, header=False)
        # 读取数据，删除重复值
        data = pd.read_csv(file_path)
        # 以日期为准
        data = data.drop_duplicates(subset=['date'])
        # 重新写入
        data.to_csv(file_path, index=False)
    else:
        data.to_csv(file_path)
    print('已成功存储至：', file_path)


def get_filepath(filename, type):
    """
    获取文件路径
    :param filename: 文件名
    :param type: 文件类型
    :return: 路径
    """
    return data_dir + type + '/' + filename + '.csv'


def get_csv_price(code, start_date=None, end_date=None, columns=None):
    """
    获取本地数据，且鼠标完成数据更新工作
    :param code: 股票代码
    :param start_date: 起始日期， 为空表示创建时间
    :param end_date: 结束日期，为空标示今天
    :param columns: 可选字段
    :return: dataframe
    """
    # 使用update直接更新
    update_daily_price(code)
    # 读取数据
    file_path = get_filepath(code, 'price')
    if columns and 'date' in columns:
        data = pd.read_csv(file_path, usecols=columns, index_col='date', parse_dates=True)
    else:
        data = pd.read_csv(file_path, index_col='date', parse_dates=True)

    # 根据传入日期返回
    if not start_date and not end_date:
        return data
    elif not end_date:
        return data[data.index >= start_date]
    elif not start_date:
        return data[data.index <= end_date]
    else:
        return data[(data.index >= start_date) & (data.index <= end_date)]


def update_daily_price(code, type='price'):
    """
    更新每日数据
    :param type: 类型
    :param code: 股票代码
    :return: void
    """
    file_path = get_filepath(code, type)
    if path.exists(file_path):
        start_date = pd.read_csv(file_path, usecols=['date'])['date'].values[-1]
        end_date = datetime.datetime.today().strftime("%Y-%m-%d")
        if start_date == end_date:
            print("股票数据已是最新数据")
            return
        df = get_single_price(code, 'daily', start_date, end_date)
        export_data(df, code, 'price', 'a')
    else:
        # 重新获取该股票行情数据
        df = get_single_price(code, 'daily')
        export_data(df, code, 'price')
    print("股票数据已经更新成功:", code)


def transfer_price_freq(data, time_freq):
    """
    转换为指定周期的K:open开盘价（周期第一天）、收盘价（周期最后一天）、最高价（周期内）、最低价（周期内）
    :param data: 数据
    :param time_freq: 周期
    :return: 转换后的数据
    """
    df_trans = pd.DataFrame()
    df_trans['open'] = data['open'].resample(time_freq).first()
    df_trans['close'] = data['close'].resample(time_freq).last()
    df_trans['high'] = data['high'].resample(time_freq).max()
    df_trans['low'] = data['low'].resample(time_freq).min()
    return df_trans


def get_single_finance(code, date, stat_date):
    """
    获取单个股票财务指标
    :param code: 股票代码
    :param date: 日期
    :param stat_date: 统计日期
    :return: 财务指标
    """
    login()
    return get_fundamentals(query(indicator).filter(indicator.code == code), date=date, statDate=stat_date)


def get_single_valuation(code, date, stat_date):
    """
    获取单个股票估值指标
    :param code: 股票代码
    :param date: 日期
    :param stat_date: 统计日期
    :return: 财务指标
    """
    login()
    return get_fundamentals(query(valuation).filter(valuation.code == code), date=date, statDate=stat_date)


def calculate_change_pct(data):
    """
    涨跌幅 = （当期收盘价 - 前期收盘价） / 前期收盘价
    :param data: dataframe，带有收盘价
    :return: dataframe，带有涨跌幅
    """
    data['close_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)


def normalize_code(code):
    """
    将股票代码转换成聚宽的标准格式
    :param code: 股票代码
    :return: 代码
    """
    login()
    return normalize_code(code)
