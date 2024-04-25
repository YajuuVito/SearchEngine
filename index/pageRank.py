# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 01:00:42 2024

@author: vitto
"""

import json


import numpy as np

"""
Page rank implementation from Wikipedia
https://en.wikipedia.org/wiki/PageRank
"""
def pagerank(M, d: float = 0.85):
    """PageRank algorithm with explicit number of iterations. Returns ranking of nodes (pages) in the adjacency matrix.

    Parameters
    ----------
    M : numpy array
        adjacency matrix where M_i,j represents the link from 'j' to 'i', such that for all 'j'
        sum(i, M_i,j) = 1
    d : float, optional
        damping factor, by default 0.85

    Returns
    -------
    numpy array
        a vector of ranks such that v_i is the i-th rank from [0, 1],

    """
    N = M.shape[1]
    w = np.ones(N) / N
    M_hat = d * M
    v = M_hat @ w + (1 - d)
    while(np.linalg.norm(w - v) >= 1e-10):
        w = v
        v = M_hat @ w + (1 - d)
        v=v/sum(v)
    return v

pages = []
path = "../crawler2/adj_matrix.json"
with open(path, "r", encoding="utf-8") as file:
    for line in file:
        pages.append(json.loads(line))
        
    adj_mat=np.zeros((297,297))
    for page in pages:
        pageID = page['Parent_ID']
        for child in page['Child_IDs']:
            adj_mat[child-1][pageID-1]=1/len(page['Child_IDs'])
            
    rank=pagerank(adj_mat)

    for i in range(297):
        # 创建一个Python对象
        data = {
            "page_id":i+1,
            "score":rank[i]
                }

        # 将Python对象转换为JSON字符串
        json_data = json.dumps(data)

        # 写入JSON字符串到文件
        with open("page_rank.json", "a") as file:
            file.write(json_data)
            file.write("\n")
