import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                          os.pardir, os.pardir, os.pardir,
                                                          "speech_recognition", "My First Project-25336ff1f246.json")

def transcribe(filename, language_code):
    # Instantiates a client
    client = speech.SpeechClient()

    # Loads the audio into memory
    with io.open(filename, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=language_code)

    # Detects speech in the audio file
    response = client.recognize(config, audio)
    transcript = " ".join([result.alternatives[0].transcript for result in response.results])

    return transcript