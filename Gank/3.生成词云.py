from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import jieba
import pandas as pd
import numpy as np

gank_df = pd.read_csv('gank.csv', engine='python',encoding='utf-8')
# 过滤列 type为福利的项，取出列 desc 项中所有的值，将值转成 list
desc_dict = gank_df[gank_df['type'] != '福利']['desc'].tolist()
# 将 list 转成 str ，用于分词。
desc_texts = ' '.join(desc_dict)

# 分词
word_cut_list = jieba.cut(desc_texts, cut_all=True)
word_space_cut_split = ' '.join(word_cut_list)

#
coloring = np.array(Image.open("gank_frog.jpg"))
my_wordcloud = WordCloud(background_color="white",
                         width = 1280,
                         height = 720,
                         max_words=500,
                         mask=coloring,
                         max_font_size=200,
                         random_state=42,
                         font_path=r'simkai.ttf' # 中文字体
                        ).generate(word_space_cut_split)
image_colors = ImageColorGenerator(coloring)
fig = plt.figure(figsize=(32,18))
image_colors = ImageColorGenerator(coloring)
plt.imshow(my_wordcloud.recolor(color_func=image_colors))
plt.imshow(my_wordcloud)
plt.axis("off")
plt.savefig('gank_word_cloud.png')
plt.show()