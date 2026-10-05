import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import subprocess
import sys, subprocess
import ollama


recognizer = sr.Recognizer()
engine = pyttsx3.init()

recognizer.energy_threshold = 150
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 1.2
recognizer.phrase_threshold = 0.2
recognizer.non_speaking_duration = 0.6


def speak(text):
    print("Assistant:", text)
    code=("import sys, pyttsx3\n"
          "e=pyttsx3.init()\n"
          "e.say(sys.argv[1])\n"
          "e.runAndWait()\n")
    
    subprocess.run([sys.executable,"-c",code,text])
def ask_ai(question):
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful voice assistant. "
                    "Answer the user's question directly and accurately. "
                    "Keep answers short, usually 1 to 3 sentences. "
                    "Never ignore the user's question. "
                    "Do not greet the user unless they greet you."
                    "Give accurate answers."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        keep_alive=-1
    )

    return response["message"]["content"]
def listen():
    with sr.Microphone() as source:
        print("\nListening... (threshold):",recognizer.energy_threshold,")")


        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=12
            )

        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""
        try:
             print("Recognizing...")
             text = recognizer.recognize_google(audio)
             print("You:", text)
             return text.lower()

        except sr.UnknownValueError:
             print("Couldn't understand.")
             return ""

        except sr.RequestError:
             print("Internet/speech service problem.")
             return ""

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print("You:", text)
        if "open youtube" in text.lower():
         speak("Opening YouTube")
         webbrowser.open("https://www.youtube.com")
        return text.lower()
    

    except sr.UnknownValueError:
        print("Couldn't understand.")
        return ""

    except sr.RequestError:
        print("Internet/speech service problem.")
        return ""

while True:
    command = listen()

    if command:

        if "hello" in command:
            speak("Hello bro!")
        elif"hi" in command:
            speak("whats up")
        elif"how are you" in command:
             speak("i am good what about you")

        elif "open youtube" in command:
            speak("Opening YouTube")        
            webbrowser.open("https://www.youtube.com")

        elif "open google" in command:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif "what time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak("The time is " + current_time)

        elif "what date" in command:
            current_date = datetime.datetime.now().strftime("%d %B %Y")
            speak("Today is " + current_date)

        elif "open calculator" in command:
            speak("Opening calculator")
            subprocess.Popen("calc.exe")

        elif "stop" in command:
            speak("Goodbye bro!")
            break

        else:
            answer = ask_ai(command)
            speak(answer)