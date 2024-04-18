import json
import math

with open('./inverted_index.json', "r", encoding="utf-8") as file:
    for line in file:
        line = json.loads(line)
        df = len(line["content"])
        N = 297
        idf = math.log2(N/df)
        data = {
            "key":line["key"],
            "idf":idf 
        }
        json_data = json.dumps(data)
        with open("idf.json", "a") as file:
            file.write(json_data)
            file.write("\n")