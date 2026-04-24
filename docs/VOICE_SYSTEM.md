# F.R.I.D.A.Y Voice System

- Wakeword: Vosk-based detection ("Wake up F.R.I.D.A.Y", "wake up")
- STT: Vosk (streaming mode, local-first, low-latency)
- TTS: Coqui TTS (streaming, interruption-capable)
- All comms via event bus (WebSocket), emitting events:
  - `wakeword.detected`, `stt.partial`, `stt.result`, `tts.speak`, etc.
- Privacy: No audio leaves device. Hot-reloading agents for fast retrain/iteration.
- Extensible: Swap STT model, TTS engine, or add noise-reduction preproc as needed.