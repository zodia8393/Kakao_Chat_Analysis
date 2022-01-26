#시간대별 빈도 분석

#1. 데이터 불러오기 , 인덱스 초기화
import matplotlib
import pandas as pd
import pickle
from pprint import pprint

import wordcloud

with open("cleaned_data.pk","rb") as f:
    data=pickle.load(f)
    
data.reset_index(inplace=True,drop=True)
print(data.info())

#2. 날짜표현 변경
date=data['data']
print(date)

date_fix=[]
for i in date:
    i = i.replace(' ','')
    if i[6]=='월':
        i=i[:5]+'0'+i[5:]
    if i[9]=='일':
        i=i[:8]+'0'+i[8:]
    i=i.replace('년','-').replace('월','-').replace('일','')
    date_fix.append(i[0:10])
    
data['Date']=date_fix
a=data['Date']
print(data)

#3. datetime 변환후 인덱스 설정
data['Date']=pd.to_datetime(data['Date'])

data=data.set_index('Date')
print(data.head())

#쓸모없는 열 지우기
data=data.drop('data',axis=1)
print(data)

#4. 월별 분석 위한 분할
sep=data['2021-09-01':'2021-09-30']
oct=data['2021-10-01':'2021-10-31']
nov=data['2021-11-01':'2021-11-30']
dec=data['2021-12-01':'2021-12-31']
jan=data['2022-01-01':'2022-01-31']

slice0=[msg for msg in list(sep['content'])]
slice1=[msg for msg in list(oct['content'])]
slice2=[msg for msg in list(nov['content'])]
slice3=[msg for msg in list(dec['content'])]
slice4=[msg for msg in list(jan['content'])]

print(slice0[:10])

#빈도분석 및 시각화
import nltk
import matplotlib.pyplot as plt
import platform
from matplotlib import font_manager, rc
from wordcloud import WordCloud



def time_freq_analysis(time_slice):
    total_tokens=[token for doc in slice0 for token in doc.split()]
    text=nltk.Text(total_tokens,name="kakao")

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
                        background_color='white',
                        ).generate_from_frequencies(dict(wc))

    plt.figure(figsize=(16,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    
time_freq_analysis(slice4)
