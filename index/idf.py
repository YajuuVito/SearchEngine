import json
import math

with open('./inverted_index.json', "r", encoding="utf-8") as file:
    for line in file:
        line = json.loads(line)
        doc_list = line["content"]
        doc_set = set()
        for id,idx in doc_list:
            doc_set.add(id)
        df = len(doc_set)
        N = 297
        idf = math.log2(N/df)
        data = {
            "key":line["key"],
            "idf":idf ,
            "df":df
        }
        json_data = json.dumps(data)
        with open("idf.json", "a") as file:
            file.write(json_data)
            file.write("\n")