from django.apps import AppConfig
import nltk


class SeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "SE"
    
    def ready(self):
        print('download stopwords')
        nltk.download('stopwords')