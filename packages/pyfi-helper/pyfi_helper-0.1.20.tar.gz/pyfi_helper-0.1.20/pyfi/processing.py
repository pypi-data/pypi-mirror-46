# 数据序列预处理模块,存放一些时间序列预处理的通用模块，一般会被data_agent调用
import datetime as dt
import pandas as pd
import numpy as np


def yoy2fixedbaseindex(orgfbi, yoylist, option1='index', option2='yoy', fbiloc='start'):
    """
    将同比序列转换为定基指数
    author: HuPeiran
    # input: orgfib, yoylist = pandas.data dataframe
    # option1 = 'index' OR 'mom', option2 = 'yoy' OR 'cumyoy', fbiloc = 'start' OR ?

    # option1 代表初始定基指数的形式，指数形式 - 'index'，环比形式 - 'mom'
    # option2 代表计算定基指数的数据形式，同比数据 - 'yoy'，累计同比数据 - 'cumyoy'
    # option3 用于指定初始定基指数和后面环比数据位置

    # 初始定基指数不能与同比数据叠加
    # 举例：初始定基指数'2011-01:2011-12'，同比数据'2012-01:2018-05'
    # 函数最后将初始定基指数和同比数据一并返回
    :param orgfbi:
    :param yoylist:
    :param option1:
    :param option2:
    :param fbiloc:
    :return:
    """
    startmonth = orgfbi.index[0].month
    endmonth = orgfbi.index[-1].month
    cyc = endmonth - startmonth + 1

    if option1 == 'mom':
        temp = [1 + i for i in orgfbi.iloc[:, 0].values]
        temp[0] = 1
        orgfbi_list = np.cumprod(temp)
        orgfbi_list = [i * 100 for i in orgfbi_list]
    elif option1 == 'index':
        start = orgfbi.iloc[:, 0].values[0]
        temp = [i / start * 100 for i in orgfbi.iloc[:, 0].values]
        orgfbi_list = temp

    startyear = yoylist.iloc[:, 0].index[0].year
    alldatelist = yoylist.index
    allyearlist = [i.year for i in alldatelist]
    temp = list()
    [temp.append(i) for i in allyearlist if not i in temp]  # 取yoy数据的所有年份
    allyearlist = temp

    len_ = len(yoylist[str(allyearlist[-1])])
    if len_ != cyc:
        newdate = pd.date_range(start=dt.date(allyearlist[0], startmonth, 1),
                                end=dt.date(allyearlist[-1], endmonth, 31), freq='M')
        adddata = [0] * (cyc * (len(allyearlist) - 1) + len_) + [np.nan] * (cyc - len_)
        adddata_dataf = pd.DataFrame(data=adddata, index=newdate, columns=['temp'])
        yoylist.columns = ['temp']
        yoylist_new = yoylist + adddata_dataf

    yoy_1year = list()
    yoy_1year.append(orgfbi_list)

    for year_count in allyearlist:
        yoy_1year.append(
            [float(i) / 100 + 1 for i in yoylist_new.loc[str(year_count), :].values])  # dataframe.values = array

    yoy_1year_array = np.array([i for i in yoy_1year])
    re = list(np.cumprod(yoy_1year_array.T, axis=1).T.reshape((1, cyc * (len(allyearlist) + 1)))[0])
    re[-(cyc - len_):] = []
    re = pd.DataFrame(data=re, index=list(orgfbi.index) + list(yoylist.index), columns=['FixedBaseIndex'])
    return re


def macro_adjust(yoy, cyoy, method=1):
    """
    author: Wang Luzhou
    update date: 2018-08-01
    introduction: 去除1月，2月信息用累计同比
    :param yoy:
    :param cyoy:
    :param method: 1:remove Jan data; 2: copy Dec data to Jan
    :return:

    """
    for i in range(len(yoy)):
        if yoy.index[i].month == 2: # 2月份
            yoy[i] = cyoy[i]
        if yoy.index[i].month == 1: # 1月份
            if method == 1 or i == 0:
                yoy.iloc[i] = np.nan
            elif method == 2:
                yoy.iloc[i] = yoy.iloc[i - 1]
    return yoy.dropna()


def ffill_mon_data(data):
    """
    author: Wang Luzhou
    update: 2018-08-14
    将数据进行月度级别的填充，并向前复制覆盖na值
    日度数据也可以转换为月度数据
    :param data:
    :return:

    Examples
    --------
    当我们调用人民币定存利率的时候，我们收到的是不规则的低频数据，
    因此需要依靠这个函数将数据转换为月度数据
    """
    return data.resample("M").last().ffill().dropna()


def get_supseason_ind(data):
    """
    输入的为环比数据,返回的是超季节性指数
     # input: data = pandas.series
    :return:
    """
    from pyfi import spring_month
    # 环比数据
    data = data
    # cpi_r = w.edb(codes=[code], begin_date=datetime(1995, 1, 1), end_date=cur_date).iloc[:, 0]
    # 标记春节， 该月有春节则标记True,否则标记False
    spring = pd.Series(index=data.index)
    for i in range(len(data)):
        if data.index[i].month == 1 or i == 0:
            spring_m = spring_month(data.index[i].year)
        if data.index[i].month == spring_m:
            spring[i] = True
        else:
            spring[i] = False
    # 标记完成
    supseason_ind = pd.Series(index=data.index)
    supseason_cum_ind = pd.Series(index=data.index)
    cpi_cum_r = pd.Series(index=data.index)
    window = 5  # 和过去五年作比较
    for i in range(12, len(data)):
        if cpi_cum_r.index[i].month == 1:
            cpi_cum_r[i] = data[i]/100.0
        else:
            cpi_cum_r[i] = (1 + (0 if np.isnan(cpi_cum_r[i - 1]) else cpi_cum_r[i - 1])) * (1 + data[i]/100.0) - 1
        past = data[:i]
        past_cum = cpi_cum_r[:i]
        past_spring = spring[:i]
        spring_cur = spring[i]
        chosen = past.loc[(past.index.month == data.index[i].month) & (past_spring == spring_cur)][-window:]
        chosen_cum = past_cum.loc[(past_cum.index.month == cpi_cum_r.index[i].month)][-window:].dropna()
        if len(chosen) > 0:
            avg = chosen.mean()
            supseason_ind[i] = data[i] - avg
        if len(chosen_cum) > 0:
            avg_cum = chosen_cum.mean()
            supseason_cum_ind[i] = cpi_cum_r[i] - avg_cum
    return supseason_ind, supseason_cum_ind
