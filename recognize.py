import json, pyaudio
from vosk import Model, KaldiRecognizer

model = Model(r"vosk/ru")
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


def recognize_speak():
    while True:
        data = stream.read(120000)
        rec.AcceptWaveform(data)
        x = json.loads(rec.Result())
        if x["text"] == "":
            continue
        else:
            return x["text"]
