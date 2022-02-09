from django.db import models

from techtest.articles.models import Article

class Region(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=255)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    