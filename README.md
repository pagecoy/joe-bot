# About Joe Bot
This is a simple brain for a local LLM that can listen, talk, and reply to you. 
I used very small models because my current machine can't handle it.  
Note: Only works on Windows for now. I use WSL2 in my workflow now but I haven't updated the part in speak().

**Why this version only works on Windows?** The commands I have in the speak function that makes the reply.wav and plays it
only work in Powershell. You can change it though.

### What I Used
**Software**
- Ears Drums: faster_whisper from WhisperModel
- Voice: Piper, en_US-joe-medium.onnx
- Brain: Ollama, gemma3:1b

**Hardware**
- Mouth: My laptop's speakers
- Ears: Free webcam we had
- Eyes: The webcam

Also, if you wanna play with test_eyes.py - you should change VideoCapture in cap variable to 0. I figured you have a default camera 
and in the system it would be 0.
