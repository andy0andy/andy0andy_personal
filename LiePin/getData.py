import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from wordcloud import WordCloud
import jieba
from collections import Counter

#设置字符集，防止中文乱码
plt.rcParams["font.sans-serif"] = [u"simHei"] #修改默认字体
plt.rcParams["axes.unicode_minus"] = False

pd.set_option('max_columns', 100)
pd.set_option('max_rows', 100)

def clean_data():
    with open('liepin-python.json','r',encoding='utf-8') as f:
        data = pd.DataFrame({
            'title':[],
            'comp':[],
            'money':[],
            'addr':[],
            'fuli':[],
            'job_yaoqiu':[],
            'job_content':[],
        })

        for line in f.readlines():
            s = pd.Series(json.loads(line))
            data = data.append(s,ignore_index=True)


    # 将数据里的"[]"去掉
    data = data.applymap(lambda i :str(i).lstrip('[').rstrip(']').strip("'"))
    # 去空值
    data = data.dropna()
    # 去面议
    data = data.drop(index=data[data['money']=="面议"].index)
    # 去空城
    data = data.drop(index=data[data['addr']=="None"].index)


    # 最小月薪
    data['min_mon'] = data['money'].apply(lambda i:i.replace('薪',"").replace('k',"").replace('·',"-").split('-')[0])
    # 最大月薪
    data['max_mon'] = data['money'].apply(lambda i: i.replace('薪', "-").replace('k', "-").replace('·', "-").split('-')[1])
    # 月薪期数  X
    data['type_mon'] = data['money'].apply(lambda i: i.replace('薪', "-").replace('k', "-").replace('·', "-").split('-')[2])

    data['addr'] = data['addr'].apply(lambda i:i.split('-')[0])

    return data

# 统计城市对Python需求量
def city_need_py(data):
    # print(data['addr'])

    y = data['title'].count()
    x = data['title'].count().index

    ps = plt.bar(x,height=y)

    for p in ps:
        x = p.get_x() + p.get_width()/2
        y = p.get_height()
        plt.text(x,y,str(y),ha="center",va="bottom")

    plt.title('城市对Python需求量')
    plt.xlabel('城市')
    plt.ylabel('岗位需求')
    plt.show()

# 制作词云
def job_wc(data,t):
    # print(data)
    words = []
    with open('哈工大停用词表.txt','r',encoding='gbk') as f:
        stopwords = f.read()

    for i in data:
        lst = jieba.lcut(i)
        lst = [l for l in lst if l not in stopwords]
        words.extend(lst)
    words = Counter(words)
    # print(words.most_common(200))

    wc = WordCloud(font_path="C:\Windows\Fonts\simkai.ttf",background_color='white')
    wc.generate(" ".join(w[0] for w in words.most_common(200)))
    wc.to_file('{}.jpg'.format(t))



def main():
    data = clean_data()
    # city_need_py(data.groupby('addr'))
    # job_wc(data['fuli'],'福利')
    # job_wc(data['job_content'],'工作内容')

if __name__ == '__main__':
    main()