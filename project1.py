import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import sys
import pywhatkit as kit
import requests
from bs4 import BeautifulSoup

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  
    speak('May I help you with something')


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 200
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...")  
        return "None"
    query=query.lower()
    return query

def news():
    main_url = 'https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=03119ef6b57a40248a7c771be08c427a'
    main_page=requests.get(main_url).json()
    articles=main_page["articles"]
    head=[]
    day=["first","second","third","fourth","fifth","sixth","seventh","eight","ninth","tenth"]
    for ar in articles:
        head.append(ar["title"])
    speak("today's highlights are")
    for i in range(len(day)):
        speak(f"{day[i]} is: {head[i]}")

def TaskExecution():
    wishMe()
    while True:
        query = takeCommand()
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            #print(results)
            speak(results)

        elif 'hello jarvis' in query:
            speak('Hello , may I help you with something')

        elif 'how are you' in query:
            speak('I am fine, what about you')

        elif 'open youtube' in query:
            speak("what should i search")
            cm=takeCommand()
            kit.playonyt(f"{cm}")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("what should i search")
            cm=takeCommand()
            webbrowser.open(f"{cm}")

        elif 'temperature' in query:
            search='temperature in delhi'
            url=f"https://www.google.com/search?q={search}"
            r=requests.get(url)
            data=BeautifulSoup(r.text,"html.parser")
            temp=data.find("div",class_="BNeawe").text
            speak(f"current {search} is {temp}")

        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")   

        elif 'play music' in query:
            music_dir = 'D:\music'
            songs = os.listdir(music_dir)
            for song in songs:
                if song.endswith('.mp3'):
                    print(song)
                    os.startfile(os.path.join(music_dir, song))
        
        elif "tell me news" in query:
            speak("please wait, fetching the latest news")
            news()

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"the time is {strTime}")

        elif 'open cmd' in query:
            os.system("start cmd")

        elif 'open code' in query:
            codePath = "C:\\Users\\divya\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
        
        elif 'open notepad' in query:
           codepath="C:\Windows\System32\notepad.exe"
           os.startfile(codePath)

        elif 'shut down' in query:
            os.system("shutdown /s /t 5")
        
        elif 'sleep now' in query:
            speak("say hello jarvis to wakeup me anytime")

            break
            
            

if __name__ == "__main__":
    speak("Hello, I am Jarvis. Please tell me how may I help you")
    speak(" to wake me say hello jarvis")
    while True:
        permission=takeCommand()
        if "hello jarvis" in permission:
            TaskExecution()
        elif "goodbye" in permission:
            speak("thanks for using me, have a good day")
            sys.exit()