from backend.ai.agent_base import AgentBase
import sounddevice as sd
import queue
import sys
import vosk
import json
import threading

class SpeechAgent(AgentBase):
    def __init__(self, event_bus, model_path="vosk-model-small-en-us-0.15"):
        super().__init__("stt", event_bus)
        self.model_path = model_path
        self.q = queue.Queue()
        self.running = True

    def start_listen_thread(self):
        threading.Thread(target=self.listen_and_publish, daemon=True).start()

    def listen_and_publish(self):
        model = vosk.Model(self.model_path)
        recognizer = vosk.KaldiRecognizer(model, 16000)
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16", channels=1, callback=self.callback):
            print("[SpeechAgent] Listening for speech (press Ctrl+C to stop)...")
            while self.running:
                data = self.q.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").strip()
                    if text:
                        print(f"[SpeechAgent] STT Recognized: {text}")
                        self.publish("stt.result", {
                            "text": text
                        })

    def callback(self, indata, frames, time, status):
        self.q.put(bytes(indata))

if __name__ == "__main__":
    from backend.event_bus import EventBus
    bus = EventBus()
    agent = SpeechAgent(bus)
    agent.start_listen_thread()
    bus.run_forever()