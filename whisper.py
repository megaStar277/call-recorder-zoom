from openai import OpenAI
from pydub import AudioSegment
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
  api_key=os.getenv('API_KEY'),  # this is also the default, it can be omitted
)
audio_file = AudioSegment.from_mp3("recordings/Botjoined_20240118-043137.mp3")

audio_length =  len(audio_file)
print(audio_length)
transcription = ''
ten_minutes= 10 * 60 * 1000

for last_snippet_time_stamp in range(0, audio_length, ten_minutes):
  snippet = audio_file[last_snippet_time_stamp: ten_minutes]
  snippet.export("audio_snippet.mp3", format="mp3")
  snippet_transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=open("audio_snippet.mp3", "rb"), 
        prompt="ZyntriQix, Digique Plus, CynapseFive, VortiQore V8, EchoNix Array, OrbitalLink Seven, DigiFractal Matrix, PULSE, RAPT, B.R.I.C.K., Q.U.A.R.T.Z., F.L.I.N.T.",
        response_format="text"
    )
  transcription = transcription + snippet_transcription

print(transcription)

#Optional
with open("transcription.txt", "w") as file:
    file.write(transcription)