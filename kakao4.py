#데이터 불러오기
import imp
import pandas as pd
import numpy as np
from pprint import pprint
import pickle

with open("cleaned_data.pk","rb") as f:
    data=pickle.load(f)
    
data.reset_index(inplace=True,drop=True)
print(data.head())
print(data.info())

#데이터 전처리
#2. 날짜표현 변경
date=data['data']

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

data['Date']=pd.to_datetime(data['Date'])
data=data.drop('data',axis=1)
print(data)

#이름에 띄어쓰기 적용된거 해제시키기
#name=[]
#for i in data['name']:
#    name.append(i.replace(' ',''))
#data['name']=name
#data.reset_index(inplace=True)
#data.drop('index',axis=1,inplace=True)
#print(data.shape)


#3. Author Topic Model 위한 데이터 전처리
users=set(data['name'])
print(users)
authors=data.groupby('name')
pprint(authors.groups)
print(type(authors.groups))

#리스트로 바꾸기
author_list={}
for user,index in authors.groups.items():
    author_list[user]=list(index)
    
print(author_list)

#4. gensim 이용한  Author Topic Model
tokenized_data=[msg.split() for msg in list(data['content'])]
print(tokenized_data[:10])


from gensim.models import AuthorTopicModel
from gensim.corpora import Dictionary, bleicorpus
from gensim import corpora
