import os
import torch
import sounddevice


device = torch.device('cpu')
torch.set_num_threads(4)
local_file = 'silero_models/ru/model.pt'

if not os.path.isfile(local_file):
    torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v4_ru.pt',
                                   local_file)

model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
model.to(device)


def speak(text, sample_rate=48000, speaker='xenia'):
    audio_paths = model.apply_tts(text=text,
                                 speaker=speaker,
                                 sample_rate=sample_rate)

    sounddevice.play(audio_paths, blocking=True)

if __name__ == "__main__":
    speak('Съешь этих мягких французских будочек да выпей же ча+ю')
