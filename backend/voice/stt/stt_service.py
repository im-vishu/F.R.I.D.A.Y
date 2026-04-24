import os
import vosk
import queue
import json
import sounddevice as sd
import sys

# === SET YOUR MODEL PATH HERE ===
# Use ABSOLUTE PATH for Windows to avoid path issues!
MODEL_PATH = "C:/Projects/F.R.I.D.A.Y/backend/voice/stt/vosk-model-small-en-us-0.15"  # <-- Adjust if needed!

SAMPLE_RATE = 16000

def check_model_path(model_path):
    """Diagnose model loading issues by printing path and its contents."""
    print("Current Working Directory:", os.getcwd())
    if not os.path.isdir(model_path):
        print(f"ERROR: Model path '{model_path}' does NOT exist or is not a directory!")
        sys.exit(1)
    contents = os.listdir(model_path)
    if not contents or 'am' not in contents:
        print(f"ERROR: Model path '{model_path}' does NOT contain expected Vosk model files (got: {contents})")
        sys.exit(1)
    print(f"Model path OK. Contents: {contents}")

def main():
    check_model_path(MODEL_PATH)
    print("Loading Vosk model...")
    model = vosk.Model(MODEL_PATH)
    print("Model loaded. Starting STT stream...")

    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=callback
    ):
        print("STT streaming! Speak into your microphone.")
        rec = vosk.KaldiRecognizer(model, SAMPLE_RATE)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get('text', '')
                if text:
                    print(f"[STT] FINAL: {text}")
            else:
                partial = json.loads(rec.PartialResult()).get('partial', '')
                if partial:
                    print(f"[STT] PARTIAL: {partial}")

if __name__ == "__main__":
    main()