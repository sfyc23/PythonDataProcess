import pandas as pd
import numpy as np
from pyecharts import *


def get_gank_df(csv_name='gank.csv'):
    '''
    获取 gank 的 dataFrame
    :return:
    '''
    gank_df = pd.read_csv(csv_name, engine='python', encoding='utf-8')
    gank_df['createdAt'] = pd.to_datetime(gank_df['createdAt'])
    gank_df['publishedAt'] = pd.to_datetime(gank_df['publishedAt'])
    return gank_df


def show_type_pie():
    '''
    Gank 发布类型比例
    :return: None
    '''
    gank_df = get_gank_df()
    gank_type_counts_ser = gank_df.type.value_counts()
    type_pie = Pie("Gank 发布类型比例", "数据来源：gank.io", title_pos='center')
    type_pie.add("占比", gank_type_counts_ser.index, gank_type_counts_ser.values, is_random=True,
                 radius=[30, 75], rosetype='radius',
                 is_legend_show=False, is_label_show=True)
    type_pie.use_theme('dark')
    type_pie.render()  # 保存图
    type_pie


def show_everyYear_type_pie():
    '''
    Gank 每年发布类型比例趋势
    :return:
    '''
    gank_df = get_gank_df()
    timeline = Timeline(is_auto_play=True, timeline_bottom=0)
    timeline.use_theme('dark')

    gank_year_group = gank_df.groupby(pd.Grouper(key='publishedAt', freq='1Y'))
    for name, group in gank_year_group:
        type_group_count_ser = group['type'].value_counts()
        type_group_pie = Pie("Gank 发布类型比例", "数据来源：gank.io", title_pos='center')
        type_group_pie.add("占比", type_group_count_ser.index, type_group_count_ser.values, is_random=True,
                           radius=[30, 75], rosetype='radius',
                           is_legend_show=False, is_label_show=True)
        timeline.add(type_group_pie, name.year)

    # timeline.render(path='Gank 每年发布类型比例趋势.gif')
    timeline


def show_who_bar_top20():
    '''
    Gank 提交 Top20 的大佬
    :return: None
    '''
    gank_df = get_gank_df()
    who_counts_ser = gank_df['who'].value_counts()

    who_bar = Bar("Gank 提交 Top20 的大佬", "来源：gank.io", width=1000, height=600)
    who_bar.use_theme('vintage')
    who_bar.add("提交次数", who_counts_ser.index[:20], who_counts_ser.values[:20], mark_point=['max'],
                xaxis_rotate=30)
    # who_bar.render(path='Gank 提交 Top20 的大佬.png') # 保存图
    who_bar


def show_year_sum_bar():
    '''
      Gank 每年发布的数量
      :return: None
      '''
    gank_df = get_gank_df()
    year_count_ser = gank_df.groupby(pd.Grouper(key='publishedAt', freq='1Y'))['_id'].count()  # groupby each 1 年时间
    year_count_bar = Bar("Gank 每年发布的数量", "来源：gank.io")
    year_count_bar.add("发布数量",
                       year_count_ser.index.strftime('%Y'),
                       year_count_ser.values,
                       is_label_show=True
                       )
    # year_count_bar.render('Gank 每年发布的数量.png')
    year_count_bar


def show_every_count_line():
    '''
    Gank 每次发送的数量
     :return: None
     '''
    gank_df = get_gank_df()
    gank_df['_date'] = gank_df['publishedAt'].map(lambda x: str(x)[:10])  # 生成一日期类，用于分组
    gank_every_counts_ser = gank_df.groupby('_date').size()  # # 使用日期分组，并统计数量
    gank_every_counts_ser.head()
    gank_every_counts_line = Line("Gank 每次发送的数量", "来源：gank.io")
    gank_every_counts_line.use_theme('vintage')
    gank_every_counts_line.add('日期',
                               gank_every_counts_ser.index,
                               gank_every_counts_ser.values,
                               mark_point=['max'],
                               is_datazoom_show=True
                               )
    # gank_every_counts_line.render('Gank 每次发送的数量.png')
    gank_every_counts_line


def show_gank_interval_line():
    '''
     发布数量与断更时间的比较
     :return: None
     '''
    gank_df = get_gank_df()
    gank_df['_date'] = gank_df['publishedAt'].map(lambda x: str(x)[:10])  # 生成一日期类，用于分组
    gank_every_counts_ser = gank_df.groupby('_date').size()  # # 使用日期分组，并统计数量
    gank_every_counts_ser.head()

    # 得到发布时间间隔。
    gank_every_counts_ser_index = gank_every_counts_ser.index
    # date_interval_dict 每次发布时间的间隔天数 dict.
    date_interval_dict = {gank_every_counts_ser_index[0]: 0}  # 第一项 为 0
    for i in range(1, gank_every_counts_ser_index.shape[0]):
        day = (pd.to_datetime(gank_every_counts_ser_index[i]) - pd.to_datetime(gank_every_counts_ser_index[i - 1])).days
        date_interval_dict[gank_every_counts_ser_index[i]] = day

    # 发布数量最大的日期 top2o
    gank_every_ser_top20 = gank_every_counts_ser.sort_values(ascending=False)[:20]
    # 通过上一项的数值得到当天离上一天的时间间隔
    date_interval_value = [date_interval_dict[index] for index in gank_every_ser_top20.index]
    gank_interval_line = Line("发布数量与断更时间的比较", "来源：gank.io")
    gank_interval_line.use_theme('vintage')
    gank_interval_line.add('发布数量',
                           gank_every_ser_top20.index,
                           gank_every_ser_top20.values,
                           mark_point=['max']
                           )
    gank_interval_line.add('间隔天数',
                           gank_every_ser_top20.index,
                           date_interval_value,
                           mark_point=['max']
                           )
    # gank_interval_line.render('发布数量与断更时间的比较.png')
    gank_interval_line


def show_gank_interval_line_2():
    '''
     断更时间与发布数量的比较
     :return: None
     '''
    gank_df = get_gank_df()
    gank_df['_date'] = gank_df['publishedAt'].map(lambda x: str(x)[:10])  # 生成一日期类，用于分组
    gank_every_counts_ser = gank_df.groupby('_date').size()  # # 使用日期分组，并统计数量
    gank_every_counts_ser.head()

    # 得到发布时间间隔。
    gank_every_counts_ser_index = gank_every_counts_ser.index
    # date_interval_dict 每次发布时间的间隔天数 dict.
    date_interval_dict = {gank_every_counts_ser_index[0]: 0}  # 第一项 为 0
    for i in range(1, gank_every_counts_ser_index.shape[0]):
        day = (pd.to_datetime(gank_every_counts_ser_index[i]) - pd.to_datetime(gank_every_counts_ser_index[i - 1])).days
        date_interval_dict[gank_every_counts_ser_index[i]] = day
    date_interval_ser_top20 = pd.Series(date_interval_dict).sort_values(ascending=False)[:20]  # 得到时间间隔最大 top20

    gank_interval_line2 = Line("断更时间与发布数量的比较", "来源：gank.io")
    gank_interval_line2.use_theme('vintage')
    gank_interval_line2.add('间隔天数',
                            date_interval_ser_top20.index,
                            date_interval_ser_top20.values,
                            mark_point=['max']
                            )
    # gank_interval_line2.add('数量平均数',
    #                     date_interval_ser_top20.index,
    #                     [int(gank_every_counts.mean()) for _ in range(20)] ,
    #                     mark_point=['max']
    #                     )
    gank_interval_line2.add('发布数量',
                            date_interval_ser_top20.index,
                            gank_every_counts_ser[date_interval_ser_top20.index],
                            is_label_show=True
                            )
    # gank_interval_line2.render('断更时间与发布数量的比较.png')
    gank_interval_line2

def show_year_month_line():
    '''
     最活跃的月份
     :return: None
     '''
    gank_df = get_gank_df()
    year_month_line = Line("最活跃的月份", "来源：gank.io")
    year_month_line.use_theme('shine')
    year_group = gank_df.groupby(pd.Grouper(key='publishedAt', freq='1Y'))
    for name, group in year_group:
        year_mouth_count_ser = group.groupby(pd.Grouper(key='publishedAt', freq='1M'))['_id'].count()
        year_month_line.add(str(name.year),
                            year_mouth_count_ser.index.strftime('%m').tolist(),
                            year_mouth_count_ser.values.tolist(),
                            mark_point=['max'])
    # year_month_line.render('最活跃的月份.png')
    year_month_line

if __name__ == '__main__':
    # gank_df = get_gank_df()

    show_type_pie()
