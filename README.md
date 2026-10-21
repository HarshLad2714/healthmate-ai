# HealthMate AI 🩺

A multilingual (Gujarati, Hindi, English) health information chatbot built for the
Devpost "Build with AI: BASICS" hackathon.

## Features
- Replies in the language the user writes in
- Simple, short, safe answers with a "see a doctor" nudge
- Emergency keyword detection (shows 112 / 108 / Tele-MANAS 14416)
- Built-in medical disclaimer in every answer

## Run locally
```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your_key_here"      # Windows PowerShell: $env:GEMINI_API_KEY="your_key_here"
streamlit run app.py
```
Get a free API key from https://aistudio.google.com/apikey

## Deploy (Streamlit Community Cloud)
1. Push this folder to a GitHub repo
2. Go to https://share.streamlit.io and create a new app from the repo (main file: `app.py`)
3. In Advanced settings > Secrets add: `GEMINI_API_KEY = "your_key_here"`

## Built with
Python, Streamlit, Google Gemini API, Prompt Engineering

> Disclaimer: for general information only, not medical advice.
