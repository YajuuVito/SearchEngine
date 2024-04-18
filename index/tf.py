import json

idf = {}
with open("./idf.json", "r", encoding="utf-8") as file:
    for line in file:
        line = json.loads(line)
        idf[line["key"]] = line["idf"]

with open("./index.json", "r", encoding="utf-8") as file:
    for line in file:
        line = json.loads(line)
        word_list = line["index"]
        word_map = {}
        tf_list = []
        max_tf = 0
        for [word, idx] in word_list:
            word_map[word] = word_map.get(word) + 1 if word_map.get(word) else 1
        for key, value in word_map.items():
            if value > max_tf:
                max_tf = value
            tf_list.append([key, value, idf.get(key)])
        data = {"page_id": line["page_id"], "max_tf": max_tf, "tf": tf_list}
        json_data = json.dumps(data)
        with open("tf_idf.json", "a") as file:
            file.write(json_data)
            file.write("\n")
