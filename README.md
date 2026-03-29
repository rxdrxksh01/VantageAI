# VANTAGE — Your AI Life Assistant
> A voice-powered personal AI assistant for college students. Talk to it, it remembers everything.

---

## Features
| Feature | Status |
|---|---|
| Voice Input + Output | Done |
| LLM via Groq (Llama 3.3 70B) | Done |
| Persistent Memory (ChromaDB) | Done |
| Google Calendar | Coming Soon |
| Attendance Tracker (BunkSmart) | Coming Soon |
| Gmail Integration | Coming Soon |

---

## Quick Start
```bash
git clone https://github.com/yourusername/vantage.git
cd vantage
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
brew install portaudio
```
Add your key to `.env` -> `GROQ_API_KEY=your_key_here`
```bash
python main.py
```

---

## How It Works
```
You speak
    |
listener.py  -> Speech to Text (Google STT)
    |
store.py     -> Search past memories (ChromaDB)
    |
llm.py       -> Send to Groq LLM
    |
store.py     -> Save exchange to memory
    |
speaker.py   -> Speak reply (Mac say)
    |
Loop
```

---

## Tech Stack
Groq · LangChain · ChromaDB · SpeechRecognition · Python 3.12

---

