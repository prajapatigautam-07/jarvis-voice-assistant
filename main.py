import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests


recognizer = sr.Recognizer()

# Put your NEW NewsAPI key here
newsapi = "YOUR_NEW_NEWSAPI_KEY"


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def processCommand(c):
    command = c.lower().strip()

    # Open Google
    if "open google" in command:
        webbrowser.open("https://google.com")

    # Open Facebook
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")

    # Open YouTube
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")

    # Open LinkedIn
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")

    # Play music
    elif command.startswith("play"):
        song = command.replace("play", "", 1).strip()

        print("Song:", song)

        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            webbrowser.open(link)
        else:
            speak("Sorry, I could not find that song.")
            print("Song not found:", song)

    # News
    elif "news" in command:
        print("Getting news...")

        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"

        r = requests.get(url)

        if r.status_code == 200:
            data = r.json()

            articles = data.get("articles", [])

            if not articles:
                speak("Sorry, I could not find any news.")
                return

            for article in articles[:5]:
                title = article.get("title")

                if title:
                    print(title)
                    speak(title)

        else:
            print("News API Error:", r.status_code)
            speak("Sorry, I could not fetch the news.")


if __name__ == "__main__":

    speak("Initializing Jarvis...")

    while True:

        r = sr.Recognizer()

        print("Recognizing...")

        try:
            # Listen for wake word
            with sr.Microphone() as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=3
                )

            word = r.recognize_google(audio)

            print("You said:", word)

            if word.lower().strip() == "jarvis":

                speak("Yes")

                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")

                    r.adjust_for_ambient_noise(source, duration=0.5)

                    audio = r.listen(source)

                    command = r.recognize_google(audio)

                    print("Processing:", command)

                    processCommand(command)

        except sr.WaitTimeoutError:
            print("No speech detected.")

        except sr.UnknownValueError:
            print("Could not understand audio.")

        except sr.RequestError as e:
            print("Speech recognition service error:", e)

        except Exception as e:
            print("Error:", e)