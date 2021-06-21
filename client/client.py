#!/usr/bin/env python3
from flask import Flask, request
from flask import jsonify, abort
from flask import render_template
from time import sleep
import requests

from gtts import gTTS
from pydub import AudioSegment
import subprocess

from spectrum import spectrum
from getapis import get_weather, play_radio

app = Flask(__name__)
print("Talk to me\n")

def play_message(output):
    tts = gTTS(output, lang='en')
    tts.save('1.mp3')
    subprocess.call('rm -rf *.wav', shell=True)
    subprocess.call(['ffmpeg', '-i', '1.mp3', '1.wav'],stderr=subprocess.DEVNULL)
    subprocess.call('rm -rf *.mp3', shell=True)
    spectrum()

#@app.route("/", methods = ["GET"])
def createQuestion():
    question = ""
    while question != "stop":
        question = input()
        if question == "stop":
            exit(0)

        if "weather" in question:
            play_message("Would you like to know the weather for today?")
            print("Would you like to know the weather for today?(y/n)\n")
            ans = input()
            #ans = user_input()
            if ans == "y":
                play_message(get_weather())

        elif "play " in question and "music" in question:
            play_message("Would you like me to play some music?")
            print("Would you like me to play some music?(y/n)\n")
            ans = input()
            #ans = user_input()
            if ans == "y":
                play_radio()

        else:
            resp = requests.post("http://192.168.1.7:4000/input", json = {"question": question})
            if(resp.status_code == 200):
                answer = resp.json()
                play_message(answer["answer"])
                print(answer["answer"])
            else:
                abort(resp.status_code)

with app.app_context():
    createQuestion()

if __name__ == "__main__":
   app.run(host='192.168.1.6', port=8000, debug=True)
   #app.run(host='127.0.0.1', port=8000, debug=True)
