import os
import sounddevice as sd
import sherpa_onnx
import numpy as np
from faster_whisper import WhisperModel
import ollama
import subprocess
import webrtcvad
import collections
import time
import re

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

MIC_INDEX = 1
PIPER_EXE = "piper.exe"
VOICE_MODEL = "en_US-joe-medium.onnx"

print("Joe is booting up...")
ears = WhisperModel("base.en", device="cpu", compute_type="int8")

# you can change its personality here
SYSTEM_PROMPT = {
    'role': 'system',
    'content': (
        "Your name is Joe."
        "Rules: "
        "1. Keep responses between 10-15 words. "
        "2. Don't use emojies."
    )
}

def speak(text):
    wav_file = "reply.wav"

    if os.path.exists(wav_file):
        try: os.remove(wav_file)
        except: pass

    print(f"[Joe is speaking...]")

    try:
        exe_path = os.path.abspath(PIPER_EXE)

        process = subprocess.Popen(
            [exe_path, "--model", VOICE_MODEL, "--output_file", wav_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )

        process.communicate(input=text)

        if os.path.exists(wav_file):
            subprocess.run([
                "powershell", "-c", 
                f"(New-Object Media.SoundPlayer '{os.path.abspath(wav_file)}').PlaySync()"
            ])
        else:
            print("Joe refuses to speak. Check if the .onnx.json file is missing.")
    except Exception as e:
        print(f"Joe's vocal cords snapped: {e}")

def ask_joe(text):
    print(f"\n[Joe is thinking...]")
    response = ollama.chat(model='gemma3:1b', messages=[
        SYSTEM_PROMPT,
        {'role': 'user', 'content': text},
    ])
    reply = response['message']['content']
    reply = reply.replace("**", "").replace("*", "").replace("#", "")
    return reply

def main():
    vad = webrtcvad.Vad(3)
    fs = 16000
    chunk_ms = 30
    chunk_size = int(fs * chunk_ms / 1000)

    print("Wait a sec...")
    time.sleep(1.0)

    try:
        while True:
            print("\n[LISTENING]")
            audio_data = []
            ring_buffer = collections.deque(maxlen=20)
            triggered = False
            voiced_frames = 0

            with sd.InputStream(samplerate=fs, channels=1, dtype='int16', device=MIC_INDEX) as stream:
                while True:
                    frame, _ = stream.read(chunk_size)
                    is_speech = vad.is_speech(frame.tobytes(), fs)

                    if not triggered:
                        if is_speech:
                            voiced_frames += 1
                            if voiced_frames > 5:
                                print("[VOICE DETECTED, KEEP TALKING]")
                                triggered = True
                                audio_data.append(frame)
                        else:
                            voiced_frames = 0
                    else:
                        audio_data.append(frame)
                        ring_buffer.append(is_speech)

                        if ring_buffer.count(False) > 0.9 * ring_buffer.maxlen:
                            print("[STOPPED LISTENING]")
                            break

            if triggered and audio_data:
                recording = np.concatenate(audio_data).flatten().astype(np.float32) / 32768.0
                
                print("[TRANSCRIBING]")
                segments, _ = ears.transcribe(recording)
                user_text = "".join([s.text for s in segments]).strip()
                
                if user_text:
                    print(f"You: {user_text}")
                    reply = ask_joe(user_text)
                    print(f"Joe: {reply}")
                    speak(reply)
                else:
                    print("Joe: 'Can't hear you. Try again.'")
                
    except KeyboardInterrupt:
        print("\n[SHUTTING DOWN]")

if __name__ == "__main__":
    main()