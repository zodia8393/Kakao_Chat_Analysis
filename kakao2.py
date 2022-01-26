import pandas as pd
import pickle
from pprint import pprint
from kakao1 import SW


with open("cleaned_data.pk","rb")as f:
    data=pickle.load(f)
    
import matplotlib.pyplot as plt
import platform
from matplotlib import font_manager, rc
import nltk
from konlpy.tag import Twitter
from collections import Counter
from wordcloud import WordCloud


print(data)

print(data.info())

data.reset_index(inplace=True,drop=True)
print(data.info())

users=set(data['name'])
print(users)

authors=data.groupby('name')
pprint(authors.groups)
print(type(authors.groups))

author_list={}
for user,index in authors.groups.items():
    author_list[user]=list(index)
    
#print(author_list)


def user_freq_analysis(username,data,author_list):
    user_msg=[str(data['content'][idx]) for idx in author_list[username]]
    total_tokens=[token for doc in user_msg for token in doc.split()]
    text=nltk.Text(total_tokens,name='kakao')
    
    path = "C:/Windows/Fonts/malgun.ttf"
    if platform.system() =='Windows':
        font_name=font_manager.FontProperties(fname=path).get_name()
        rc('font',family=font_name)
    else:
        print("알 수 없는 시스템입니다")
        
    plt.figure(figsize=(16,10))
    text.plot(50)
    
    wc=text.vocab().most_common(100)
    
    wordcloud=WordCloud(font_path="C:/Windows/Fonts/malgun.ttf",
                        relative_scaling=0.2,
                        #stopwords=SW,
                        background_color='white',
                        ).generate_from_frequencies(dict(wc))
    plt.figure(figsize=(16,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    
user_freq_analysis("원수연",data,author_list)
    
