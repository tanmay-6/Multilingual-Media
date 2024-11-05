import assemblyai as aai
from key import aai_api_key

aai.settings.api_key = aai_api_key

transcriber = aai.Transcriber()
transcript = transcriber.transcribe("aud1.wav")

subtitle = transcript.export_subtitles_srt()

with open("subtitles.srt", "w") as f:
    f.write(subtitle)
print(subtitle)