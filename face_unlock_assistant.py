import cv2
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import pyautogui



import pyautogui
import ctypes
import requests

def get_weather(city="Korangi, Karachi"):
    api_key = "b9ffadf5084f3341514abb37b78ea6fc"  # get from openweathermap.org
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()

    if data["cod"] != "404":
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        speak(f"The weather in {city} is {desc} with a temperature of {temp}°C.")
    else:
        speak("City not found.")



def take_screenshot():
    file = f"screenshot_{datetime.datetime.now().strftime('%H%M%S')}.png"
    pyautogui.screenshot(file)
    speak(f"Screenshot saved as {file}")

def lock_screen():
    ctypes.windll.user32.LockWorkStation()




# Voice Engine Setup (Female Soft Voice)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower() or "zira" in voice.name.lower():  # Windows voice fallback
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 160)
engine.setProperty('volume', 1)

recognizer_speech = sr.Recognizer()

# Functions
def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning Boss Zain!")
    elif hour < 17:
        speak("Good afternoon Boss Zain!")
    else:
        speak("Good evening Boss Zain!")

def get_time_date():
    now = datetime.datetime.now()
    speak(f"The current date and time is {now.strftime('%A, %B %d, %Y, %I:%M %p')}")

def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening (you can also type)...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=8)
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"You (voice): {query}")
    except:
        query = input("You (typed): ")
    return query.lower()


def handle_command(command):
    if "hi" in command or "hello" in command:
        speak("Hello Zain! How can I assist you today?")
    elif "bye" in command or "exit" in command:
        speak("Goodbye Zain! Have a great day!")
        return False
    elif "who are you" in command:
        speak("I'm Zain virtual assistant, here to help you anytime.")
    elif "date" in command or "time" in command:
        get_time_date()
    elif "motivate" in command:
        speak("The harder you work for something, the greater you'll feel when you achieve it.")
    elif "weather" in command:
        city = command.replace("weather", "").strip()
        if city == "":
            city = "Korangi, Karachi"  # Default city if none is mentioned
        get_weather(city)

    elif "gaming" in command:
        speak("Stay hydrated, learn the maps, and focus on teamwork!")
    elif "fitness" in command:
        speak("Start small with daily walks and gradually add strength training.")
    elif "study" in command or "studies" in command:
        speak("Use the Pomodoro technique—25 minutes of work, 5-minute break.")
    elif "coding" in command:
        speak("Break problems into smaller tasks and solve step by step.")
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google...")
    elif "screenshot" in command:
        take_screenshot()
    elif "lock screen" in command:
         speak("Locking your PC now. Stay secure, boss!")
         lock_screen()
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube...")
    elif "play favourite" in command:
        webbrowser.open("https://www.youtube.com/watch?v=ga1HVaO-n84&list=RDga1HVaO-n84&start_radio=1")
        speak("playing favourite zara zara song")
    elif "open instagram" in command:
        webbrowser.open("https://www.instagram.com")
        speak("Opening Instagram...")
    elif "open notepad" in command:
        os.system("start notepad")
        speak("Opening Notepad...")
    elif "open command prompt" in command:
        os.system("start cmd")
        speak("Opening Command Prompt...")
    elif "play music" in command:
        os.system("start wmplayer")
        speak("Playing your music...")
    elif "good morning" in command:
        speak("Good morning, Zain! Ready to start your day?")
    elif "good night" in command:
        speak("Good night, Zain! Sleep well and dream big!")
    elif "joke" in command:
        speak("Why don't skeletons fight each other? Because they don't have the guts!")
    elif "help" in command:
        speak("I can help you with motivation, coding, fitness, studies, music, and more.")
    else:
        speak("Sorry, I didn't understand that. Try saying something else.")
    return True

# Face Recognition Part
def recognize_face():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")

    cam = cv2.VideoCapture(0)
    recognized = False

    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))
            label, confidence = recognizer.predict(face)

            if confidence < 60:
                recognized = True
                text = "Welcome Boss Zain!"
                color = (0, 255, 0)
                speak("Welcome Boss Zain! Face recognized. Activating your assistant.")
                cam.release()
                cv2.destroyAllWindows()
                return True
            else:
                text = "Access Denied"
                color = (0, 0, 255)

            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        cv2.imshow("Digital Soul Lock", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    return False

# MAIN LOGIC
if recognize_face():
    wish_me()
    speak("How can I serve you today?")
    while True:
        command = listen_command()
        if not handle_command(command):
            break
else:
    speak("Access Denied. Shutting down.")
