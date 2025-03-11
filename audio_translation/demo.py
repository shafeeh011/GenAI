import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
'''
# This is for openai = 0.28
audio = open("/home/muhammed-shafeeh/AI_ML/GenAI/audio_translation/recorded.mp3", "rb")
out_put = openai.Audio.translate("whisper-1", audio)
print(out_put)
'''

# Initialize client (no need for openai.OpenAI()) # This is for openai >= 0.28
client = openai.Client()

# Open the audio file
audio_file = open("/home/muhammed-shafeeh/AI_ML/GenAI/audio_translation/recorded.mp3", "rb")

# Use the correct method for Whisper-1 translation
response = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)

# Print the transcribed text
print(response.text)
