import speech_recognition as sr

def recognize_speech_from_mic():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    try:
        # Use the default system microphone as the audio source
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening... Speak now.")

            # Listen to the microphone
            audio = recognizer.listen(source)

        # Try recognizing the speech
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio)
        print("You said:", text)

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")

    except sr.RequestError as e:
        print(f"Could not request results; {e}")

    except OSError:
        print("Microphone not found or is not accessible.")

if __name__ == "__main__":
    recognize_speech_from_mic()
