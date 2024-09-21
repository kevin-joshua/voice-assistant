import speech_recognition as sr
import webbrowser
import pyttsx3 
import musicLibrary
import requests
import dotenv
import os
from gtts import gTTS
import pygame





engine = pyttsx3.init()
pygame.mixer.init()
dotenv.load_dotenv()
api_key = os.getenv("api_key")

def processCommand(c):
  if "open google" in c.lower():
    webbrowser.open("https://google.com")
  if "open facebook" in c.lower():
    webbrowser.open("https://facebook.com")
  if "open youtube" in c.lower():
    webbrowser.open("https://youtube.com")
  if "open github" in c.lower():
    webbrowser.open("https://github.com")
  elif c.lower().startswith("play"):
    song = c.lower().split(" ")[1]
    link = musicLibrary.music[song]
    webbrowser.open(link)
  elif "news" in c.lower():
    url = f'https://newsapi.org/v2/top-headlines?sources=the-times-of-india,ndtv,the-economic-times,financial-times&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Extract the headlines
        articles = data.get('articles', [])
        
        # Print out the titles of the headlines
        for i, article in enumerate(articles, start=1):
            speak(f"{i}. {article['title']}")
    else:
        print(f"Failed to fetch news. Status code: {response.status_code}")
  else:
    output = aiProcess(c)
    speak(output)
def aiProcess(command):
    import google.generativeai as genai

    # Directly set the API key
    genai.configure(api_key=api_key)

    # Create the model
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    # Generate content
    response = model.generate_content(command+"give short responses")
    return response.text

def speak_old(text):
  engine.say(text)
  engine.runAndWait()

def speak(text):
    try:
        tts = gTTS(text)
        tts.save('temp.mp3')
        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.remove("temp.mp3")
    except requests.exceptions.ConnectionError:
        print("Failed to connect to Google TTS. Using pyttsx3 as a fallback.")
        speak_old(text)  # Fallback to pyttsx3



if __name__ == "__main__":
  speak("Initializing Jarvis")
  while True:
    r = sr.Recognizer()
    try:
      with sr.Microphone() as source:
        print("Listening....")
        audio = r.listen(source,timeout=2,phrase_time_limit=1)
      print('recognizing...')
      word= r.recognize_google(audio)
      if(word.lower() == "hello"):
         speak("jarvis activated")
         with sr.Microphone() as source:
           print("jarvis active")
           audio = r.listen(source,timeout=2,phrase_time_limit=2)
           print("recognizing")
           command = r.recognize_google(audio) 
           processCommand(command)   
    except Exception as e:
      print(f"Error:{e}")

