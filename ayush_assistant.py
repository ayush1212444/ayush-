import speech_recognition as sr
from gtts import gTTS
import os
import time
from gpiozero import Button
from openai import OpenAI

# ================== IMPORTANT CONFIG ==================
# YAHAN APNI OPENAI API KEY DAALO (zaruri hai)
openai_client = OpenAI(api_key="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")  # ←←← APNI KEY YAHAN CHANGE KARO

BUTTON_GPIO = 17   # Button GPIO pin (physical pin 11)
button = Button(BUTTON_GPIO, pull_up=True)

# Ayush - Legal Helper System Prompt
messages = [
    {"role": "system", "content": "You are Ayush, a legal helper AI assistant. You provide helpful, accurate, and professional legal advice along with general assistance. Always respond clearly, politely, and concisely in simple and easy language."}
]

def listen():
    """Voice se text nikaalo"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... Boliye")
        r.adjust_for_ambient_noise(source, duration=0.8)
        try:
            audio = r.listen(source, timeout=8, phrase_time_limit=12)
            text = r.recognize_google(audio, language="en-IN")
            print("Aapne kaha:", text)
            return text
        except:
            print("❌ Samajh nahi aaya. Dobara button dabakar try karo.")
            return None

def speak(text):
    """Text ko voice mein bolo"""
    if not text:
        return
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save("response.mp3")
        os.system("mpg321 response.mp3")
        os.remove("response.mp3")
    except:
        print("Sound play karne mein problem")

# ================== STARTUP ==================
print("🚀 Ayush Legal Helper starting on Raspberry Pi...")
speak("Hello, I am Ayush, your legal helper assistant. I am ready. Press the button and speak.")

print("✅ System ready! Button dabao aur baat shuru karo.")

# ================== MAIN LOOP ==================
while True:
    button.wait_for_press()          # Button dabane ka wait
    print("🔘 Button pressed!")
    speak("Listening. Please speak now.")
    
    user_text = listen()
    if user_text:
        messages.append({"role": "user", "content": user_text})
        
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=600,
                temperature=0.7
            )
            reply = response.choices[0].message.content.strip()
            print("Ayush:", reply)
            speak(reply)
            messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            print("API Error:", e)
            speak("Sorry, network issue hai. Thodi der baad try karo.")
    
    time.sleep(0.3)   # Double press rokne ke liye
