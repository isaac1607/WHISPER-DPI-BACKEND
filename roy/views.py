from rest_framework import status,viewsets
from rest_framework.response import Response
from .tests import *
from .models import *
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
import whisper
import os
from django.conf import settings
from openai import OpenAI


# Create your views here.

status200 = status.HTTP_200_OK
status400 = status.HTTP_400_BAD_REQUEST
status401 = status.HTTP_401_UNAUTHORIZED
status404 = status.HTTP_404_NOT_FOUND
status500 = status.HTTP_500_INTERNAL_SERVER_ERROR

message401 = "Non autorisé"
model = whisper.load_model("base")



@api_view(['POST'])
def audio(request):
    if 'audio_file' not in request.FILES:
        return Response({"error": "No audio file provided"}, status=400)

    audio_file = request.FILES['audio_file']
    file_name = default_storage.save(audio_file.name, audio_file)
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    result = model.transcribe(file_path, fp16=False)
    
    # Suppression du fichier après traitement pour nettoyer
    default_storage.delete(file_path)

    return Response({"text": result["text"]})

@api_view(['POST'])
def audio_online(request):
    if 'audio' not in request.FILES:
        return Response({"error": "No audio file provided"}, status=400)
    print("Entrer")
    
    audio = request.FILES['audio']
    file_name = default_storage.save(audio.name, audio)
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    
    audio_file= open(file_path, "rb")
    client = OpenAI(api_key = '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')
    print("Juste avant la transcription")

    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    
    default_storage.delete(file_path)
    app = App()
    app.text = transcript.text
    app.audio = audio
    app.save()

    audio_url =''
    audio_url = request.build_absolute_uri(settings.MEDIA_URL + str(app.audio))

    return Response({"text": transcript.text,"audio": audio_url, "id":audio.pk},status=status200)


@api_view(['GET'])
def get_laste(request):
    try:
        ide = request.GET.get('id')
        app = App.objects.get(pk=ide)
        audio_url =''
        audio_url = request.build_absolute_uri(settings.MEDIA_URL + str(app.audio))
        return Response({"text": app.text,"id":app.pk,"audio": audio_url},status=status200)
    except:
        return Response({"text": "Error id"},status=status500)


@api_view(['GET'])
def liste_audio(request):
    try:
        retour = []
        for app in App.objects.all():
            audio_url =''
            audio_url = request.build_absolute_uri(settings.MEDIA_URL + str(app.audio))
            retour.append({"text": app.text,"id":app.pk,"audio": audio_url})
        return Response(retour,status=status200)
    except:
        return Response({"text": "Error id"},status=status500)
   