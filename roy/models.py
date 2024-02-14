from django.db import models

# Create your models here.

class App(models.Model):
    text = models.TextField(verbose_name="Text")

    class Meta:
        db_table = 'App'
        verbose_name = 'App'