
import requests
import re

out = open('answers_pt.txt', 'a')

lines = []
with open('answers.txt') as f:
    lines = f.readlines()



for line in lines:
    sentences = re.split('((?<=[.?!]")|((?<=[.?!])(?!")))\s*', line)
    answer_=''
    for s in sentences:
        if s != '':
            answer_+=' >>pt<<'+s

    params = {'target_lang': 'ROMANCE',
        'text': answer_,
        'source_lang':'en',
        'beam_size':5}
    answer_pt = requests.get("http://0.0.0.0:24080/translate", params=params)
    out.write(answer_pt.json()["translated"][0])
    out.write("\n")


f.close()
out.close()