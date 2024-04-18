from django.http import HttpResponse, JsonResponse
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PathConfig:
    index = os.path.join(BASE_DIR, "SE\\data\\index.jsonl")
    inverted_index = os.path.join(BASE_DIR, "SE\\data\\inverted_index.jsonl")
    page_rank = os.path.join(BASE_DIR, "SE\\data\\page_rank.jsonl")
    data = os.path.join(BASE_DIR, "SE\\data\\data.jsonl")
    matrix = os.path.join(BASE_DIR, "SE\\data\\adj_matrix.jsonl")
    tf = os.path.join(BASE_DIR, "SE\\data\\tf.jsonl")
    idf = os.path.join(BASE_DIR, "SE\\data\\idf.jsonl")


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def search(request):
    words = request.GET.get("words")
    mode = request.GET.get("mode", "page_rank")
    ps = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    tokenizer = RegexpTokenizer(r"\w+")
    words = tokenizer.tokenize(words.lower())
    words = [ps.stem(w) for w in words if not w in stop_words]

    # Boolean
    doc_set = set()
    with open(PathConfig.inverted_index, "r", encoding="utf-8") as file:
        for line in file:
            line = json.loads(line)
            if line["key"] in words:
                content = line["content"]
                for [doc, pos] in content:
                    doc_set.add(doc)

    doc_list = list(doc_set)
    doc_rank_list = []
    # page rank
    if mode == "page_rank":
        with open(PathConfig.page_rank, "r", encoding="utf-8") as file:
            for line in file:
                line = json.loads(line)
                if line["page_id"] in doc_list:
                    doc_rank_list.append((line["page_id"], line["score"]))
        doc_rank_list.sort(key=lambda x: x[1], reverse=True)
    res = {"words": words, "doc": doc_rank_list}
    
    # VSM
    
    return JsonResponse(res)
