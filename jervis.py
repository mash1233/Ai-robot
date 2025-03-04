import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import openai

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('volume', 0.9)
engine.setProperty('rate', 180)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening..........")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing..........")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        speak("I didn't get it Say that again please..........")
        return "None"
    return query

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 6 and hour < 12:
        speak("Good morning, Mash")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon, Mash")
    else:
        speak("Good evening, Mash")
    speak("I am here How may I help you? ")

def sendEmail(to, content):
    # Make sure to replace 'your-email@gmail.com' and 'your-password' with your actual email and password
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your-email@gmail.com', 'your-password')
    server.sendmail('your-email@gmail.com', to, content)
    server.close()

def get_openai_response(prompt):
    openai.api_key = 's'
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'search' in query:
            speak('Searching Wikipedia...')
            query = query.replace('search', '')
            results = wikipedia.summary(query, sentences=2)
            speak('According to Wikipedia')
            print(results)
            speak(results)
        elif 'who are you' in query:
            speak("I am Jervis, your first assistant, sir")
        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
            speak("opening")
        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
            speak("opening")
        elif 'open chatgpt' in query:
            webbrowser.open("https://www.chatgpt.com")
            speak("opening")
        elif 'play music' in query:
            music_dir = 'D:\\Music'
            speak("playing")
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
        elif 'time now' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        elif 'open chrome' in query:
            codepath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(codepath)
            speak("opening")
        elif 'open everything' in query:
            evrypath = "C:\\Program Files\\Everything\\Everything.exe"
            os.startfile(evrypath)
            speak("opening")
        elif 'email to mash' in query:
            try:
                speak("What should I write, sir?")
                content = takeCommand()
                to = "mashqurulislam224@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("Sorry, I am unable to send the email")
        elif 'exit' in query:
            speak("Goodbye, Mash!")
            break
