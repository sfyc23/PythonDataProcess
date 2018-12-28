from multiprocessing.pool import ThreadPool
import requests
import os
import time
import pandas as pd
import numpy as np
from multiprocessing import Pool


def download_image(entry):
    '''
    :param entry:
    :return: 下载图片
    '''
    print('hello')
    path, uri = entry
    path = os.path.join('福利',f"{path}.jpg")
    if not os.path.exists(path):
        try:
            res = requests.get(uri, stream=True)
            if res.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(res.content)
                time.sleep(2)
                print(f'已下载:{path}')
        except Exception as e:
            print(f"请求出错: {path}")
    return path

if __name__ == '__main__':
    gank_df = pd.read_csv('gank.csv', engine='python', encoding='utf-8')
    girls_df = gank_df[gank_df['type'] == '福利'][['publishedAt', 'url']]

    downloads_url = [(str(row['publishedAt'])[:10], row['url']) for _, row in girls_df.iterrows()]
    downloads_url = downloads_url[:50]
    print(downloads_url)

    # 存放的文件夹
    image_folder = '福利'
    # 如果不存在则生成
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # 开启多线程下载图片
    ThreadPool(8).map(download_image, downloads_url)
    print('下载完成')