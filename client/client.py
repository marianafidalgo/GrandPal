#!/usr/bin/env python3
from flask import Flask, request
from flask import jsonify, abort
from flask import render_template
from time import sleep
import requests
import speech_recognition as sr

from gtts import gTTS
from pydub import AudioSegment
import subprocess
import re
from spectrum import spectrum
from getapis import get_weather, play_radio

app = Flask(__name__)
print("Talk to me\n")

def user_input():
    subprocess.call('arecord --format=S16_LE --rate=16000 --file-type=wav --duration=5 question.wav', shell=True)

    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Reading Audio file as source
    # listening the audio file and store in audio_text variable

    with sr.AudioFile('question.wav') as source:

        audio_text = r.listen(source)

    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            #, language="pt-PT"
            # using google speech recognition
            text = r.recognize_google(audio_text, language="pt-PT")
            print('Converting audio transcripts into text ...')
            print(text)
            return text

        except:
            print('Sorry.. run again...')
            text = user_input()
            return text

def play_message(output):
    tts = gTTS(output, lang='pt', tld='pt')
    tts.save('1.mp3')
    subprocess.call('rm -rf *.wav', shell=True)
    subprocess.call(['ffmpeg', '-i', '1.mp3', '1.wav'],stderr=subprocess.DEVNULL)
    subprocess.call('rm -rf *.mp3', shell=True)
    try:
        spectrum()
    except:
        pass

#@app.route("/", methods = ["GET"])
def createQuestion():
    question = ""
    while question != "adeus":
        question = user_input()
        if question == "adeus":
            exit(0)

        if "tempo" in question:
            play_message("Gostavas de saber como está o tempo hoje?")
            print("Gostavas de saber como está o tempo hoje\n")
            #ans = input()
            ans = user_input()
            if "sim" in ans:
                print('meteo')
                play_message(get_weather())

        elif "Toca" in question and "música" in question:
            play_message("Gostavas que ligasse o rádio?")
            print("Gostavas que ligasse o rádio?\n")
            #ans = input()
            ans = user_input()
            if  "sim" in ans:
                print('meteo')
                play_radio()
        else:
            params = {'target_lang': 'en',
                    'text': question,
                    'source_lang':'ROMANCE',
                    'beam_size':5}
            question_en = requests.get("http://192.168.1.85:24080/translate", params=params)
            resp = requests.post("http://192.168.1.85:4000/input", json = {"question": question_en.json()["translated"][0]})
            if(resp.status_code == 200):
                answer = resp.json()
                sentences = re.split('((?<=[.?!]")|((?<=[.?!])(?!")))\s*', answer["answer"])
                answer_=''
                for s in sentences:
                    if s != '':
                        answer_+=' >>pt<<'+s

                print(answer_)
                params = {'target_lang': 'ROMANCE',
                    'text': answer_,
                    'source_lang':'en',
                    'beam_size':5}
                answer_pt = requests.get("http://192.168.1.85:24080/translate", params=params)
                play_message(answer_pt.json()["translated"][0])
                print(answer_pt.json()["translated"][0])
            else:
                abort(resp.status_code)

with app.app_context():
    createQuestion()

if __name__ == "__main__":
    app.run(host='192.168.1.86', port=8000, debug=True)
   #app.run(host='127.0.0.1', port=8000, debug=True)
