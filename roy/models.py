from django.db import models

# Create your models here.

class App(models.Model):
    text = models.TextField(verbose_name="Text")
    audio = models.FileField(upload_to="audio/")

    class Meta:
        db_table = 'App'
        verbose_name = 'App'