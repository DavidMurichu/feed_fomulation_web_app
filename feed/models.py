from django.db import models

# Create your models here.
class Feed(models.Model):
    ingridient_batch=models.JSONField()


