'''
1.爬取数据。
'''
import requests
import re
import time
from tqdm import tqdm
import pandas as pd

def get_all_date():
    '''
    获取所有 Gank 发布所有日期集合
    :return: list
    '''
    history_date_url = 'http://gank.io/api/day/history'
    history_res = requests.get(history_date_url)
    history_date_list = history_res.json().get('results')
    history_date_list = [re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\1/\2/\3', date) for date in history_date_list]
    return history_date_list


def get_all_data(history_dates):
    '''
    :param history_dates: 日期集合
    :return: 所有Gank数据
    '''
    gank_data_list = []
    for data in tqdm(history_dates[:20]):
        day_url = 'https://gank.io/api/day/' + data
        res = requests.get(day_url)
        if res.status_code == 200:
            try:
                categorys = res.json().get('category')
                result_datas = res.json().get('results')
                for category in categorys:
                    data_list = result_datas.get(category)
                    gank_data_list.extend(data_list)
                time.sleep(0.5)
            except (KeyError, TimeoutError):
                print("error:" + data)
                continue
    return gank_data_list

def save_data(gank_data_list,csv_name='gank.csv'):
    '''
    :param csv_name: 保存的文件名
    :param gank_data_list: 保存的数据
    :return: None
    '''
    gank_df = pd.DataFrame(gank_data_list)
    gank_df.to_csv(csv_name, index=False, encoding='utf-8')

if __name__ == '__main__':
    history_date_list = get_all_date()
    print(f"共有 {len(history_date_list)} 天数据 ")

    gank_data_list = get_all_data(history_date_list)
    print(f"共爬取了 {len(gank_data_list)} 条数据")

    csv_name = 'gank.csv'
    save_data(gank_data_list, csv_name)
    print('数据保存成功')