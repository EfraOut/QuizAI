"""
Filename: speech_to_text.py
Author: Efrain Gomez Fajardo and Ashlee Hart
Purpose: Functions that interact with the OpenAI API
"""

import speech_recognition as sr

def start_listening() -> str:
    """
    Using the microphone, transcribes everything that was
    said while the space bar was being held down.
    """

    # Obtain audio from the microphone.
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("When you are ready, press and hold the space bar to record")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 2)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Couldn't recognize voice. Try again")
