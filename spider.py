#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jerry'


import requests
import pandas as pd
import time
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from jieba.analyse import extract_tags
from scipy.misc import imread


def get_html(page):

    user_data = []
    for i in range(page):
        url = 'https://www.zhihu.com/api/v4/members/excited-vczh/' \
              'followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender' \
              '%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)' \
              '%5D.topics&offset={}&limit=20'.format(i*20)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 ',
        }

        r = requests.get(url, headers=headers)

        status = r.status_code
        print('正在爬取第%s页，状态码:%s' % (str(i+1),str(status)))

        response = r.json()['data']
        user_data.extend(response)

        time.sleep(1)

    return user_data


def printYuntu(user_data,filename):
    words = []
    for i in range(len(user_data)):
        words.append(user_data[i]['name'])

    with open(filename,'w', encoding='utf-8') as f:
        for i in words:
            f.write(i)


def generater(**kwargs):
    content_name = kwargs['content_name']
    content_path = './{}.txt'.format(content_name)
    top_k = kwargs['top_k']
    bg_name = kwargs['bg_name']
    color = kwargs['color']
    font_type = kwargs['font_type']

    with open(content_path, mode='r', encoding='utf-8') as f:
        content = f.read()

    tags = extract_tags(sentence=content, topK=top_k)
    words = [word for word in jieba.cut(content, cut_all=True)]
    words_freq = {}

    for tag in tags:
        freq = words.count(tag)
        if freq > 0:
            words_freq[tag] = freq

    bg_path = './{}.png'.format(bg_name)
    bg_img = imread(bg_path)
    font_path = './{}.ttf'.format(font_type)
    word_cloud = WordCloud(font_path=font_path,  # 设置字体
                           background_color=color,  # 背景颜色
                           mask=bg_img,  # 背景图
                           max_words=top_k,  # 词云显示的最多词数
                           max_font_size=100  # 字体最大

                           )
    word_cloud.generate_from_frequencies(words_freq)
    plt.imshow(word_cloud)
    plt.axis('off')  # 不显示坐标轴
    plt.show()

    # 保存图片
    word_cloud_img = './{}_word_cloud.jpg'.format(content_name)
    word_cloud.to_file(word_cloud_img)


if __name__ == '__main__':
    print('Spider: Job start:')
    user_data = get_html(50)
    df = pd.DataFrame.from_dict(user_data)
    df.to_csv('zhihu.csv')

    printYuntu(user_data,'Yuntu.txt')
    print('\nSpider: Job done!')

    generater(content_name='Yuntu',
              top_k=200,
              bg_name='backimg',
              color='black',
              font_type='wryh')