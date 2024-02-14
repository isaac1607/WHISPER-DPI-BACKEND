from django.urls import path,include
from .views import *

app_name = "roy"

urlpatterns = [
    path('audio', audio,name="audio"),
    path('audio_last', audio_last,name="audio_last"),
    path('last', get_laste,name="last"),
]