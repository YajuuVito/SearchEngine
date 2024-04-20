from django.http import HttpResponse, JsonResponse
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import numpy as np
from . import apps

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PathConfig:
    index = os.path.join(BASE_DIR, "SE\\data\\index.jsonl")
    inverted_index = os.path.join(BASE_DIR, "SE\\data\\inverted_index.jsonl")
    page_rank = os.path.join(BASE_DIR, "SE\\data\\page_rank.jsonl")
    matrix = os.path.join(BASE_DIR, "SE\\data\\adj_matrix.jsonl")
    tf_idf = os.path.join(BASE_DIR, "SE\\data\\tf_idf.jsonl")


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def search(request):
    words = request.GET.get("words")
    mode = request.GET.get("mode", "vsm")
    ps = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    tokenizer = RegexpTokenizer(r"\w+")
    words = tokenizer.tokenize(words.lower())
    words = [ps.stem(w) for w in words if not w in stop_words]

    # Boolean
    doc_set = set()
    doc_map = {}
    with open(PathConfig.inverted_index, "r", encoding="utf-8") as file:
        for line in file:
            line = json.loads(line)
            if line["key"] in words:
                content = line["content"]
                temp_doc_set = set()
                for [doc, pos] in content:
                    doc_set.add(doc)
                    temp_doc_set.add(doc)
                    # Boolean weight
                for doc in temp_doc_set:
                    doc_map[doc] = doc_map.get(doc) + 1 if doc_map.get(doc) else 1
                temp_doc_set.clear()

    doc_list = list(doc_set)
    doc_rank_list = []

    # page rank
    if mode == "page_rank":
        with open(PathConfig.page_rank, "r", encoding="utf-8") as file:
            for line in file:
                line = json.loads(line)
                if line["page_id"] in doc_list:
                    doc_rank_list.append(
                        (line["page_id"], line["score"] + doc_map.get(line["page_id"]))
                    )
        doc_rank_list.sort(key=lambda x: x[1], reverse=True)

    # VSM
    if mode == "vsm":
        # calculate weight vector of each document
        # calculate tf*idf/max_tf
        vector1 = np.ones(len(words))
        with open(PathConfig.tf_idf, "r", encoding="utf-8") as file:
            for line in file:
                line = json.loads(line)
                if line["page_id"] in doc_list:
                    max_tf = line["max_tf"]
                    tf_line = line["tf"]
                    vector_list = []
                    for [key, tf, idf] in tf_line:
                        if key in words:
                            vector_list.append(tf * idf / max_tf)
                    vector2 = np.array(vector_list)
                    if len(vector_list) < len(words):
                        vector2 = np.concatenate(
                            (vector2, np.zeros(len(words) - len(vector_list)))
                        )
                    print(vector1, vector2)
                    cos_sim = np.dot(vector1, vector2) / (
                        np.linalg.norm(vector1) * np.linalg.norm(vector2)
                    )
                    doc_rank_list.append(
                        (line["page_id"], cos_sim + doc_map.get(line["page_id"]))
                    )
        doc_rank_list.sort(key=lambda x: x[1], reverse=True)

    # get page information
    doc_info_list = []
    for [key, score] in doc_rank_list:
        info = apps.SeConfig.page_data[key]
        info["score"] = score
        doc_info_list.append(info)

    res = {
        "doc_rank": doc_info_list,
    }
    return JsonResponse(res)
