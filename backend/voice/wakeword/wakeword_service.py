import sounddevice as sd
import numpy as np
import vosk
import queue
import sys
import json
import asyncio
from backend.voice.event_bus import publish_event

MODEL_PATH = "vosk-model-small-en-us"
WAKEWORDS = ["wake up", "wake up friday", "friday"]
SAMPLE_RATE = 16000

model = vosk.Model(MODEL_PATH)
q = queue.Queue()

def audio_callback(indata, frames, time, status):
    q.put(bytes(indata))

def wakeword_loop():
    rec = vosk.KaldiRecognizer(model, SAMPLE_RATE)
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        print("Listening for wake word...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").lower()
                for word in WAKEWORDS:
                    if word in text:
                        print(f"Wake word '{word}' detected!")
                        asyncio.run(publish_event("wakeword.detected", {"keyword": word}))
                        return

if __name__ == "__main__":
    wakeword_loop()