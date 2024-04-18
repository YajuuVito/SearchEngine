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
    page_data = {}
    link = {}

    def ready(self):
        print("download stopwords")
        nltk.download("stopwords")

        with open(SeConfig.matrix, "r", encoding="utf-8") as file:
            for line in file:
                line = json.loads(line)
                SeConfig.link[line["Parent_ID"]] = line["Child_IDs"]

        with open(SeConfig.data, "r", encoding="utf-8") as file:
            for line in file:
                line = json.loads(line)
                del line["Content"]
                line["child_id"] = SeConfig.link.get(line["page_id"], [])
                SeConfig.page_data[line["page_id"]] = line
