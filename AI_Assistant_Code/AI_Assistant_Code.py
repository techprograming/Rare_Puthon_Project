import speech_recognition as sr
import pyttsx3
import requests
import pywhatkit as kit
import webbrowser
import spacy
import datetime

# Initialize spacy NLP
nlp = spacy.load('en_core_web_sm')

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Function to convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Function to listen to user input via microphone"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"User said: {query}")
        return query.lower()
    except Exception as e:
        print("Sorry, I did not catch that.")
        return None

def get_weather(city):
    """Function to get weather information using OpenWeather API"""
    api_key = "your_api_key"  # Replace with your OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        main = data["main"]
        temp = main["temp"]
        weather_desc = data["weather"][0]["description"]
        return f"The temperature in {city} is {temp}°C with {weather_desc}."
    else:
        return "Sorry, I couldn't fetch the weather information."

def play_music(song):
    """Function to play a song on YouTube using pywhatkit"""
    kit.playonyt(song)

def search_web(query):
    """Function to search the web using webbrowser"""
    webbrowser.open(f"https://www.google.com/search?q={query}")

def process_command(command):
    """Process and execute the voice command"""
    # NLP processing to extract intents
    doc = nlp(command)
    
    # Check for weather command
    if 'weather' in command:
        city = command.split("in")[-1].strip()
        weather_report = get_weather(city)
        speak(weather_report)

    # Check for playing music command
    elif 'play' in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song} on YouTube.")
        play_music(song)

    # Check for searching web command
    elif 'search' in command:
        query = command.replace("search", "").strip()
        speak(f"Searching for {query}.")
        search_web(query)

    # Check for time command
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}.")

    # Default response if command is not recognized
    else:
        speak("Sorry, I didn't understand that command.")

def main():
    """Main function to run the assistant"""
    speak("Hello, I am your personal assistant. How can I help you today?")
    
    while True:
        command = listen()
        if command:
            process_command(command)
        else:
            speak("Please repeat your command.")
    
if __name__ == "__main__":
    main()
