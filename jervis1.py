import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import google.generativeai as genai  # Import Gemini API

# Set up Gemini API
GEMINI_API_KEY = "AIzaSyCbBEy1OBQPWNbCQ4Irpc9uIDPv4zFRwNU"  # Store your key in an environment variable
if not GEMINI_API_KEY:
    print("Error: Gemini API key is missing. Set it in environment variables.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# Initialize Text-to-Speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('volume', 0.8)
engine.setProperty('rate', 150)

def speak(audio):
    """Convert text to speech"""
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    """Takes microphone input and returns a string"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except Exception:
        print("Could not understand. Please say that again.")
        return "None"

def wishMe():
    """Greet the user based on the time of day"""
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good morning, Mash!")
    elif hour < 18:
        speak("Good afternoon, Mash!")
    else:
        speak("Good evening, Mash!")
    speak("I am Jervis. How can I help?")

def sendEmail(to, content):
    """Send an email using SMTP"""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('your-email@gmail.com', 'your-password')  # Use App Password
        server.sendmail('your-email@gmail.com', to, content)
        server.close()
        speak("Email sent successfully.")
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't send the email.")

def get_gemini_response(prompt):
    """Fetch response from Gemini API"""
    if not GEMINI_API_KEY:
        return "Gemini API key is missing."
    try:
        models = genai.list_models()
        model_id = None
        for model in models:
            # Ensure the object has model_id attribute
            if hasattr(model, 'model_id') and model['model_id'] == "gemini-pro":
                model_id = model['model_id']
                break
        if not model_id:
            return "Gemini-pro model not found. Available models are: " + ", ".join([model['model_id'] for model in models if hasattr(model, 'model_id')])
        response = genai.generate_content(model_id=model_id, prompt=prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini API error:", e)
        return "I couldn't process that request."

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        if 'tell' in query:
            speak('Searching Wikipedia...')
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentences=2)
            speak('According to Wikipedia')
            print(results)
            speak(results)
        elif 'who are you' in query:
            speak("I am Jervis, your assistant.")
        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
        elif 'open chatgpt' in query:
            webbrowser.open("https://www.chatgpt.com")
        elif 'play music' in query:
            music_dir = 'D:\\Music'  # Update path
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                speak("No music files found.")
        elif 'time now' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        elif 'open chrome' in query:
            os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        elif 'open everything' in query:
            os.startfile("C:\\Program Files\\Everything\\Everything.exe")
        elif 'email to mash' in query:
            try:
                speak("What should I write?")
                content = takeCommand()
                sendEmail("mashqurulislam224@gmail.com", content)
            except Exception as e:
                print(e)
                speak("Sorry, I am unable to send the email.")
        elif 'exit' in query:
            speak("Goodbye, Mash!")
            break
        else:
            # Use Gemini API for general queries
            gemini_response = get_gemini_response(query)
            speak(gemini_response)
            print(gemini_response)
