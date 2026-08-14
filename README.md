# AI-Voice-Assistant-in-Python-
An AI Voice Assistant built with Python uses speech recognition, natural language processing, and text-to-speech to understand voice commands and respond intelligently. It can perform tasks such as answering questions, opening applications, searching the web, setting reminders, and automating everyday activities.
# AI Voice Assistant in Python

> Talking assistant with skills for time, math, unit conversion, Wikipedia, notes and jokes — speaks via OS text-to-speech, optional microphone input.

**Status:** 🟢 Complete · Part of [Machine Learning Projects](../README.md)

## What it does
An Alexa-style assistant built on a pluggable skill pipeline: each skill inspects the query and answers if it matches (time/date, arithmetic, km↔miles / kg↔lbs / °C↔°F conversion, Wikipedia summaries, note-taking, jokes). Replies are spoken with macOS `say` (pyttsx3 elsewhere). Add `--voice` for microphone input via SpeechRecognition, or run fully typed.

## Results
All skills verified: live Wikipedia lookup, arithmetic, conversions and notes work end-to-end offline-first.

## How to run
```bash
python main.py            # typed input, spoken replies (no deps!)
python main.py --demo
pip install SpeechRecognition pyaudio && python main.py --voice
```

## Keywords
`voice-assistant` `speech-recognition` `text-to-speech` `alexa` `python` `wikipedia-api` `skills-engine` `automation` `stdlib`

