from django.apps import AppConfig
import nltk
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "SE"
    data = os.path.join(BASE_DIR, "SE\\data\\data.jsonl")
    matrix = os.path.join(BASE_DIR, "SE\\data\\adj_matrix.jsonl")
    tf = os.path.join(BASE_DIR, "SE\\data\\tf.jsonl")
    page_data = {}
    link = {}
    top_5 = {}

    def ready(self):
        print("download stopwords")
        nltk.download("stopwords")

        with open(SeConfig.matrix, "r", encoding="utf-8") as file:
            for line in file:
                line = json.loads(line)
                SeConfig.link[line["Parent_ID"]] = line["Child_IDs"]

        with open(SeConfig.tf, "r", encoding="utf-8") as file:
            for line in file:
                line = json.loads(line)
                tf_list = line["tf"]
                sorted_list = sorted(tf_list, key=lambda x: x[1], reverse=True)
                SeConfig.top_5[line["page_id"]] = sorted_list[:5]

        with open(SeConfig.data, "r", encoding="utf-8") as file:
            for line in file:
                line = json.loads(line)
                del line["Content"]
                line["child_id"] = SeConfig.link.get(line["page_id"], [])
                SeConfig.page_data[line["page_id"]] = line

        for key, value in SeConfig.page_data.items():

            SeConfig.page_data[key]["child_id"] = [
                {
                    "title": SeConfig.page_data[id]["Title"],
                    "url": SeConfig.page_data[id]["URL"],
                    "id": id,
                }
                for id in SeConfig.page_data[key]["child_id"]
            ]
            parent_id = SeConfig.page_data[key]["parent_id:"]
            SeConfig.page_data[key]["parent_id"] = (
                [
                    {
                        "title": SeConfig.page_data[parent_id]["Title"],
                        "url": SeConfig.page_data[parent_id]["URL"],
                        "id": parent_id,
                    }
                ]
                if parent_id != 0
                else []
            )
            SeConfig.page_data[key]["freq"] = SeConfig.top_5.get(key)
