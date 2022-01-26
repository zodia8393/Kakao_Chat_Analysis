from datetime import date
from tkinter import SW
import pandas as pd
import re

list1=['대장이','솔이','애플','바울','얀이','쿠식','주디','마리','라떼','순이','소희','다비','세리','베리','삼돌']

def talk_msg_parse(file_path):
    my_data=list()
    talk_msg_pattern= "[0-9]{4}[년.] [0-9]{1,2}[월.] [0-9]{1,2}[일.] 오\S [0-9]{1,2}:[0-9]{1,2},.*:"
    date_info = "[0-9]{4}년 [0-9]{1,2}월 [0-9]{1,2}일 \S요일"
    
    for line in open(file_path,encoding='utf-8'):
        if (re.match(date_info,line)) or (line==''):
            continue
        elif re.match(talk_msg_pattern,line):
            line=line.split(",")
            date_time =line[0]
            user_text=line[1].split(" : ",maxsplit=1)
            user_name=user_text[0].strip()
            text=user_text[1].strip()
            my_data.append({'data':date_time,
                                 'name':user_name,
                                 'content':text
                                 })
        else:
            if len(my_data)>0:
                my_data[-1]['content']+="\n"+line.strip()
                
    return my_data

f_path='C:/Users/User/Documents/Python WS/KakaoTalkChats.txt'

result=talk_msg_parse(f_path)
content_df=pd.DataFrame(result)

print(content_df)


import nltk


total_tokens = [token for msg in content_df['content'] for token in str(msg).split()]
print(len(total_tokens))

text=nltk.Text(total_tokens,name="NMSC")
print(len(set(text.tokens)))
print(text.vocab().most_common(20))

import matplotlib.pyplot as plt
import platform
from matplotlib import font_manager, rc

path = "C:/Windows/Fonts/malgun.ttf"
if platform.system() =='Windows':
    font_name=font_manager.FontProperties(fname=path).get_name()
    rc('font',family=font_name)
else:
    print("알 수 없는 시스템입니다")
        
plt.figure(figsize=(16,10))
text.plot(50)


content_df2=content_df.copy()
content_series2=content_df2['content']
print(content_series2)

def message_cleaning(docs):
    docs=[str(doc) for doc in docs]
    #1.쓸모없는 단어 삭제
    pattern1=re.compile("<사진|<동영상")
    docs=[pattern1.sub("",doc)for doc in docs]
    
    #2.쓸모없는 단어 삭제
    pattern2=re.compile("읽지|않음>")
    docs=[pattern2.sub("",doc)for doc in docs]   
    
    #3.단순 자음, 단순 모음 삭제
    pattern3=re.compile("[ㄱ-ㅎ]*[ㅏ-ㅢ]*")
    docs=[pattern3.sub("",doc)for doc in docs] 
    
    #4.하이퍼링크 글 삭제
    pattern4=re.compile(r"\b(https?:\/\/)?([\w.]+){1,2}(\.[\w]{2,4}){1,2}(.*)")
    docs=[pattern4.sub("",doc)for doc in docs]
    
    #5.특수문자 삭제
    pattern5=re.compile("[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]")
    docs=[pattern5.sub("",doc)for doc in docs]
    
    return docs

def define_stopwords(path):
    SW=set()
    with open(path,encoding='utf-8') as f:
        for word in f:
            SW.add(word)
    return SW

SW=define_stopwords("stopwords-ko.txt")

cleaned_corpus =message_cleaning(content_series2)
print(len(cleaned_corpus))
print(cleaned_corpus[:10])

cleaned_corpus2=[]
for i in cleaned_corpus:
    cleaned_corpus2.append(i.strip())
    
cleaned_text=pd.Series(cleaned_corpus2)
content_df2['content']=cleaned_text
cleaned_data=content_df2[content_df2['content'] !=""]
cleaned_data.info()
print(cleaned_data)

import pickle
with open ("cleaned_data.pk","wb") as f:
    pickle.dump(cleaned_data,f)
    
print(SW)