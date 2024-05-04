# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 12:03:16 2024

@author: vitto
"""


import json
# importing modules
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import os

#to use nltk you need to 
#1. pip install nltk
#2. import nltk
#3. nltk.download('all')

def write(page):
        data = {
            "page_id":page["page_id"],
            "index":page["Content"]
                }

        # 将Python对象转换为JSON字符串
        json_data = json.dumps(data)

        # 写入JSON字符串到文件
        with open("index.json", "a") as file:
            file.write(json_data)
            file.write("\n")

#unwanted_char=["(",")","/","\n","\r","-",",","."]
pages = []
path = "../crawler/data.json"
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))
tokenizer = RegexpTokenizer(r'\w+')

with open(path, "r", encoding="utf-8") as file:
    for line in file:
        pages.append(json.loads(line))
        
    if os.path.exists("index.json"):
        os.remove("index.json")
        
    for page in pages:
        page['Content']=tokenizer.tokenize(page['Content'].lower())
        page['Content'] = [w for w in page['Content'] if not w in stop_words]
        page['Content']=list(map(lambda pair: (ps.stem(pair[1]),pair[0]),enumerate(page['Content'])))
        write(page)


