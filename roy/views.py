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
def audio_last(request):
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
    print("Réponse")
    print(transcript.text)

    return Response({"text": transcript.text},status=status200)


@api_view(['GET'])
def get_laste(request):
    app = App.objects.all().last()
    if app == None or len(app.text) > 0:
        return Response({"text": "","etat":0})
    else:
        return Response({"text": app.text,"etat":1})
   