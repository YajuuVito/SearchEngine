# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 13:03:47 2024

@author: vitto
"""

import json

pages = []
path = "./index.json"
with open(path, "r", encoding="utf-8") as file:
    for line in file:
        pages.append(json.loads(line))
posting={}
for page in pages:
    for index in page['index']:
        if index[0] in posting:
            posting[index[0]].append((page['page_id'],index[1]))
        else:
            posting[index[0]]=[(page['page_id'],index[1])]
            
            
for key in posting:
        data = {
            "key":key,
            "content":posting[key]
                }

        # 将Python对象转换为JSON字符串
        json_data = json.dumps(data)

        # 写入JSON字符串到文件
        with open("inverted_index.json", "a") as file:
            file.write(json_data)
            file.write("\n")
