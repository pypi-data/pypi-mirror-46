# Author：Wang Luzhou
# Create: 2018-08-14
# 逻辑库
# 所有很宏观逻辑相关的库都在这里，蛤蛤
import numpy as np
import pandas as pd
# import talib

#  -----------事件原子逻辑算子------------------------

"""
零阶事件
"""


def zo1(data, args=[3]):
    """
    1个参数
    过去n个月的最大值
    :param data:
    :param args: args[0]: past n periods
    :return:
    """
    ind = pd.Series(index=data.index)
    past = args[0]
    for i in range(past - 1, len(data)):
        max = data[i - past + 1: i + 1].max()
        min = data[i - past + 1: i + 1].min()
        if data[i] == max:
            ind[i] = 1
        elif data[i] == min:
            ind[i] = -1
        else:
            ind[i] = 0
    return ind.dropna()


def zo2(data, args=(36, 0)):
    """

    :param data:
    :param args:
    :return:
    """
    past = args[0]
    threshold = args[1]
    if len(data) > 500:  # 说明是日度，直接在日度级别上进行标准化，防止信息丢失
        score = (data - data.rolling(window=past * 20).mean()) / data.rolling(window=past * 20).std()
        score = score.resample("M").mean().apply(lambda x: 0 if abs(x) < threshold else x)
    else:
        data = data.resample("M").mean()
        score = (data - data.rolling(window=past).mean()) / data.rolling(window=past).std()
        score = score.apply(lambda x: 0 if abs(x) < threshold else x)
    return score.dropna()


"""
一阶事件
"""


def fo1(data, args=[6]):
    """
    边际强度
    CPI： 2,2,2,2,2.5 产生最大的影响
    :param data:
    :param args:
    :return:
    """
    # 参数赋值
    # 计算分值
    from macroasset.first_logic import logic
    past = args[0]
    dif = pd.DataFrame(columns=range(1, past + 1), index=data.index)  # 存放斜率
    dif_b = pd.DataFrame(columns=range(1, past + 1), index=data.index)
    for i in dif.columns:
        dif.loc[:, i] = (data - data.shift(i)) / i
        dif_b.loc[:, i] = logic.one_signal(dif.loc[:, i])
    score_dif = dif_b.sum(axis=1)
    return score_dif


def fo2(data, args=[5]):
    """
    体现指标连续上涨的持续性
    :param data:
    :param args:
    :return:
    """
    past = args[0]
    dd = one_signal(data.diff().dropna())
    score = dd.rolling(window=past).sum()
    return score


def fo3(data, args=[1, 12]):
    """
    均线缺口本质是处于一阶和二阶之间的逻辑。在本框架内，我们将其视为1阶逻辑。
    2个参数
    data为series类型
    均线缺口,无截距
    args[0]:short period
    args[1]:long period
    args[2]: base line
    """
    data = data.ffill()
    ind = data.rolling(window=int(args[0])).mean() - data.rolling(window=int(args[1])).mean()
    return ind


def fo4(data, args=[1, 12, 1]):
    """
    3个参数
    :param data:
    :param args:0：短周期，1：长周期，2. 波动率截距
    :return:
    """
    data = data.ffill()
    short_mean = data.rolling(window=int(args[0])).mean()
    long_mean = data.rolling(window=int(args[1])).mean()
    vol_intercept = data.rolling(window=int(args[1])).std() * args[2]
    ind = short_mean - long_mean - vol_intercept
    return ind


def so1(data, args=[5]):
    """
    this logic contains first-order and second-order part, it is a mixed logic
    :param data:
    :param args: [0]: the longest length for past window; [1]:weight of the first order
    :return:
    """
    length = args[0]
    f_weight = 1
    d = []
    for i in range(1, length + 1):
        d.append((data - data.shift(i)) / i)  # reserve the nan to keep the same index
    # logic
    score = pd.Series(index=data.index)
    for j in range(length, len(data)):
        score[j] = f_weight * (1 if d[0][j] < 0 else (-1 if d[0][j] > 0 else 0))
        for i in range(len(d) - 1):
            score[j] = score[j] + (-1 if d[i][j] < d[i + 1][j] else (1 if d[i][j] > d[i + 1][j] else 0))
    score = score.dropna()
    return score


def so2(data, args=[5, 1, 1]):
    """
    this logic contains first-order and second-order part, it is a mixed logic
    :param data:
    :param args: [0]: the longest length for past window; [1]:weight of the first order
    :return:
    """
    length = args[0]
    f_weight = args[1]
    width = args[2]
    d = []
    for i in range(1, length + 1):
        d.append((data - data.shift(i * width)) / i)  # reserve the nan to keep the same index
    # logic
    score = pd.Series(index=data.index)
    for j in range(length, len(data)):
        score[j] = f_weight * (1 if d[0][j] < 0 else (-1 if d[0][j] > 0 else 0))
        for i in range(len(d) - 1):
            score[j] = score[j] + (-1 if d[i][j] < d[i + 1][j] else (1 if d[i][j] > d[i + 1][j] else 0))
    score = score.dropna()
    return score


def trend(data, args):
    """
    计算近期数据的拟合斜率
    :param data:
    :param args: 0：确定时间窗口的长短
    :return:
    """
    from sklearn import linear_model
    past = args[0]
    regr = linear_model.LinearRegression()
    s_data = pd.Series(index=data.index)
    for i in range(past, len(data)):
        regr.fit(np.array(list(range(past))).reshape(1, -1), data.values[i - past + 1: i + 1])
        s_data.iloc[i] = regr.coef_[0]
    return s_data.dropna()


def trend_count(data, args=[5]):
    """
    统计近几个月涨跌的净个数
    :param data:
    :param args:
    :return:
    """
    d = data.diff().dropna()
    count = args[0]
    ind = pd.Series(index=d.index)

    for i in range(count - 1, len(d)):
        ind[i] = d[i - count + 1: i + 1].apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0)).sum()
    return ind


def season(data, args):
    """
    季节性事件：当前的值和过去三年的均值进行对比，此类数据一般是环比月度数据
    :param data:
    :param args:
    :return:
    """
    ind = pd.Series()
    for i in range(1, 13):
        tmp = data.loc[data.index.month == i]
        tmp_mean = tmp.rolling(window=5).mean().shift(1)
        tmp_season = tmp / tmp_mean - 1 - args[0]
        ind.append(tmp_season)
    return ind.sort_index()


def mg3(data, args=[12, 1, 1]):
    """
    3个参数
    :param data:
    :param args:0：短周期，1：长周期，2. 波动率截距
    :return:
    """
    data = data.ffill()
    short_mean = data.rolling(window=int(args[0])).mean()
    long_mean = data.rolling(window=int(args[1])).mean()
    vol_intercept = data.rolling(window=int(args[1])).std() * args[2]
    ind = short_mean - long_mean - vol_intercept
    return ind


def mg2(data, args=[12, 1]):
    """
    2个参数
    data为series类型
    均线缺口,无截距
    args[0]:short period
    args[1]:long period
    args[2]: base line
    """
    data = data.ffill()
    ind = data.rolling(window=int(args[0])).mean() - data.rolling(window=int(args[1])).mean()
    return ind


# def cmo(data, args):
#     """
#     1个参数，趋势指标，返回Series
#     """
#     arg1 = args[0]
#     data = data.ffill()
#     ind = pd.Series(talib.CMO(data.values, timeperiod=arg1), index=data.index)
#     return ind

#
# def mom(data, args):
#     """
#     1个参数
#     momentum,多日的涨幅
#     :param data: pandas.Series
#     :param args: args[0]->timeperiod
#     :return: pandas.Series
#     """
#     data = data.ffill()
#     ind = pd.Series(talib.MOM(data.values, timeperiod=int(args[0])), index=data.index)
#     return ind


# def wmom(data, args):
#     """
#     3个参数
#     加权mom指标，多个不同时间端的涨幅的加权和
#     :param data:
#     :param args:
#     :return:
#     """
#     ind = (mom(data, int(args[0])).dropna()
#            + mom(data, int(args[1])).dropna()
#            + mom(data, int(args[2])).dropna()) / 3.0
#     return ind.dropna()


def slope(data, args):
    """
    区间头尾斜率
    :param data:
    :param args:0:近端斜率对应的区间， 1:远端斜率对应的区间
    :return:
    """
    past = args[0]
    slope = (data - data.shift(past - 1)) / past
    return slope


"""
2阶事件：反转事件
"""


def slopes(data, args=[5, 1, 1]):
    """
    this logic contains first-order and second-order part, it is a mixed logic
    :param data:
    :param args: [0]: the longest length for past window; [1]:weight of the first order
    :return:
    """
    length = args[0]
    f_weight = args[1]
    width = args[2]
    d = []
    for i in range(1, length + 1):
        d.append((data - data.shift(i * width)) / i)  # reserve the nan to keep the same index
    # logic
    score = pd.Series(index=data.index)
    for j in range(length, len(data)):
        score[j] = f_weight * (1 if d[0][j] < 0 else (-1 if d[0][j] > 0 else 0))
        for i in range(len(d) - 1):
            score[j] = score[j] + (-1 if d[i][j] < d[i + 1][j] else (1 if d[i][j] > d[i + 1][j] else 0))
    score = score.dropna()
    return score


def max_reversal(data, args):
    """
    高点前后两者斜率差
    :param data:
    :param args: 0 考察最近几个月的高点, 1. 截距
    :return:
    """
    # 找出高点
    ind = pd.Series(0.0, index=data.index)
    period = int(args[0])
    for i in range(period - 1, len(data)):
        tmp = data[i - period + 1:i]
        max_spot = tmp.max()
        idx = tmp.get_loc(max_spot)
        if idx != period - 2:
            continue
        else:
            ind.loc[ind.index == data.index[i]] = (tmp[-1] - tmp[idx]) / (tmp[0] - tmp[idx]) - 1 - args[1]
    return ind


def min_reversal(data, args):
    """
    触底反弹，低点前后两者斜率差
    :param data:
    :param args: 0 考察最近几个月的高点, 1. 截距
    :return:
    """
    # 找出高点
    ind = pd.Series(0.0, index=data.index)
    period = int(args[0])
    for i in range(period - 1, len(data)):
        tmp = data[i - period + 1:i]
        min_spot = tmp.min()
        idx = tmp.get_loc(min_spot)
        if idx != period - 2:
            continue
        else:
            ind.loc[ind.index == data.index[i]] = (tmp[-1] - tmp[idx]) / (tmp[0] - tmp[idx]) - 1 - args[1]
    return ind


def reversal(data, args):
    """
    连续N个周期上涨或下跌，最后一个交易日下跌或者上涨
    :param data:
    :param args:
    :return:
    """
    n = args[0]
    pct = data.pct_change()
    for i in range(n, len(pct)):
        if pct[i - n: i].sum() == n and pct[i] < 0:
            return -1.0
        elif pct[i - n: i].sum() == 0 and pct[i] > 0:
            return 1.0
        else:
            return 0.0


def slope_change(data, args):
    """
    两个区间的斜率变化差
    :param data:
    :param args:0:近端斜率对应的区间， 1:远端斜率对应的区间
    :return:
    """
    near_n = args[0]
    far_n = args[1]
    near_slope = (data - data.shift(near_n)) / near_n
    far_slope = (data - data.shift(far_n)) / far_n
    return near_slope - far_slope


def momentum(data, config, begin_date=None, end_date=None):
    """
    基于AQR Value and Momentum everywhere，过去指定时间的累积涨幅
    :param data:
    :param config: 0：past
    :param begin_date:
    :param end_date:
    :return:
    """
    past = config[0]
    mom = data / data.shift(past) - 1
    return mom.dropna()


# -------------简单N阶逻辑生成器----------------------------

def zero_order(data, begin_date=None, end_date=None):
    """
    :param data:
    :param begin_date:
    :param end_date:
    :return:
    """
    data = data.dropna()
    if begin_date is not None and end_date is not None:
        return data.loc[(data.index >= begin_date) & (data.index <= end_date)]
    else:
        return data


def first_order(data, begin_date=None, end_date=None):
    f_data = data.diff().dropna()
    if begin_date is not None and end_date is not None:
        return f_data.loc[(f_data.index >= begin_date) & (f_data.index <= end_date)]
    else:
        return f_data


def second_order(data, begin_date=None, end_date=None):
    s_data = data.diff().diff().dropna()
    if begin_date is not None and end_date is not None:
        return s_data.loc[(s_data.index >= begin_date) & (s_data.index <= end_date)]
    else:
        return s_data


# -------------逻辑长度算子----------------------------
def impulse(data, event_date, begin_date=None, end_date=None, args=[1]):
    """
    冲激
    :param data:
    :param event_date:
    :param begin_date:
    :param end_date:
    :param args: [height]
    :return:
    """
    height = args[0]
    data.loc[event_date] += height
    return slice(data, begin_date, end_date)


def step(data, event_date, begin_date=None, end_date=None, args=[1]):
    """
    阶跃
    :param data:
    :param event_date:
    :param begin_date:
    :param end_date:
    :param args: [height]
    :return:
    """
    height = args[0]
    data.loc[data.index >= event_date] += height
    return slice(data, begin_date, end_date)


def decay(data, event_date, positive=True, begin_date=None, end_date=None, args=[5, 2, 1]):
    # to add a new signal shape to the original signal series "data"
    """
    衰减
    :param data:
    :param event_date:
    :param positive
    :param begin_date:
    :param end_date:
    :param args: [height, hold, rate]
    :return:
    """
    height = args[0]
    hold = args[1]
    rate = args[2]
    length = int(np.ceil(height / rate))
    try:
        idx = data.index.get_loc(event_date)  # get the index of date of the event occurence
    except Exception as e:
        print("The event date does not exist in the index of the data!!!")
        raise e
    # construct the shape of the signal
    shape = [height] * (1 + hold)
    shape += [max(height - rate * (i + 1), 0) for i in range(length)]
    shape = np.array(shape) * (1 if positive else -1)
    # slice the shape
    last_idx = min(idx + hold + length, len(data) - 1)
    shape = shape[0: last_idx - idx + 1]
    data.iloc[idx: last_idx + 1] = shape
    return slice(data, begin_date, end_date)


def half_life(data, T=30):
    """
    半衰期
    :param data:
    :param T:
    :return:
    """

    pass


#  ------------信号处理逻辑算子-------------------------

def cumsum(score, up=5, low=-5):
    """
    将信号逐步叠加
    :return:
    """
    score = score.fillna(0)
    cum_score = pd.Series(index=score.index)
    cum_score[0] = score[0]
    for i in range(1, len(cum_score)):
        cum_score[i] = cap(cum_score[i - 1] + score[i], low=low, up=up)
    return cum_score.dropna()


def cap(score, up=5, low=-5):
    """
    限定信号的最大值和最小值，防止信号超过阈值范围
    :param score: float or series
    :param up:
    :param low:
    :return:
    """
    if hasattr(score, "__iter__"):
        return score.apply(lambda x: min(max(x, low), up))
    return min(max(score, low), up)


def value_score(value, up, low):
    """
    针对估值指标的打分，分值具有历史惯性
    :param value: Series
    :param up:
    :param low:
    :return:
    """
    score = pd.Series(index=value.index)
    for i in range(len(score)):
        if i == 0:
            if value[i] > up:
                score[i] = 1
            elif value[i] < low:
                score[i] = -1
            else:
                score[i] = 0
        else:
            if value[i] > up:
                score[i] = 1
            elif value[i] <= low:
                score[i] = -1
            elif score[i - 1] == 1:
                if value[i] <= 0:
                    score[i] = 0  # 维持基准
                elif value[i] > 0:
                    score[i] = score[i - 1]
            elif score[i - 1] == -1:
                if value[i] >= 0:
                    score[i] = 0
                elif value[i] < 0:
                    score[i] = score[i - 1]
            else:
                score[i] = 0
    return score


def to_score(low, up, max=5, min=-5, center=0):
    pass


# -----------一般操作符--------------------------------
def slice(data, begin_date=None, end_date=None):
    if begin_date is not None:
        data = data.loc[(data.index >= begin_date)]
    if end_date is not None:
        data = data.loc[(data.index <= end_date)]
    return data


def shift(data, s=1):
    return data.shift(s)


# ------------逻辑工厂-----------------------------


def index_shift(data, shift=1, freq="M"):
    data.index = data.index.shift(shift, freq=freq)
    return data


def one_signal(data, positive=True, precious=1e-10):
    """
    将指标数据转换为-1,0，+1三维信号模式， 注意已包含去na功能
    :param precious:
    :param positive:
    :param data: pandas.Series
    :return: pandas.Series
    """
    d = 1 if positive else -1
    return data.apply(lambda x: 1 if x > precious else (-1 if x < -precious else 0)).dropna() * d


def one_signal_for_df(df):
    """
    二元信号处理
    :param df:
    :return:
    """
    df = df.copy()
    for i in range(len(df.columns)):
        df.iloc[:, i] = one_signal(df.iloc[:, i])
    return df


def signal_trans(score, frm=5, to=2):
    """
    :param score:
    :param frm: 过去的分制
    :param to: 目标分制
    :return:
    """
    return score.apply(lambda x: round(x * 1.0 * to / frm))
