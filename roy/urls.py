from django.urls import path,include
from .views import *

app_name = "roy"

urlpatterns = [
    path('audio', audio,name="audio"),
    path('audio_last', audio_online,name="audio_online"),
    path('get_audio', get_laste,name="last"),
    path('liste_des_audios', liste_audio,name="liste_audio"),
]