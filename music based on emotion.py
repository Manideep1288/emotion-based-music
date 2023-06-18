import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3
import cv2
from deepface import DeepFace
import time
from pygame import mixer
import random

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

emotions = {"angry" : 0, "disgust" : 0, "fear" : 0, "happy" : 0, "neutral" : 0, "sad" : 0, "surprise" : 0}
songs = [["No Pelli.mp3","Single-Pasanga.mp3"],["Manasaa.mp3","Naalona Pongenu.mp3"],["Lala Bheemla.mp3","Rowdy Baby.mp3"],
         ["Hoyna Hoyna.mp3","Ye Chota Nuvvunna.mp3"],["The Karma Theme.mp3"],["Adiga Adiga.mp3","Emai Poyave.mp3"],
         ["Gunjukunna.mp3","Pavizha-Mazha.mp3"]]

def playSong(final_emotion):
    ind = list(emotions.keys()).index(final_emotion)
    song = random.choice(songs[ind])
    path = "songs\\"+final_emotion+"\\"+song
    speak("It seams you are feeling"+final_emotion)
    print(final_emotion)
    speak("playing"+song)
    mixer.init()
    mixer.music.load(path)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(1)

def music():
    capture = cv2.VideoCapture(0)
    for i in range(30):
        _, frame = capture.read()
        try:
            prediction = DeepFace.analyze(frame, actions = ["emotion"])
        except:
            continue
        emotion = prediction["dominant_emotion"]
        emotions[emotion] += 1
    final_emotion = ""
    count = 0
    for emotion in emotions.keys():
        if emotions[emotion]>=count:
            final_emotion = emotion
            count = emotions[emotion]
    capture.release()
    cv2.destroyAllWindows
    playSong(final_emotion)



if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("600x400")
    window.title("Assistant")
    music_bt = tk.Button(window, text="start music", height = 200, width = 200, borderwidth = 5,command = music).place(relx=0.5, rely = 0.5, anchor = "center")
    window.mainloop()
