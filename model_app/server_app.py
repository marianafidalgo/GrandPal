#!/usr/bin/env python3
from flask import Flask, abort, request
from transformers import AutoModelWithLMHead, AutoTokenizer, AutoConfig
import json

from bot_app import chat

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-small')
model = AutoModelWithLMHead.from_pretrained('GrandPal')

@app.route('/input', methods = ["POST"])
def input():
    j = request.get_json()
    print(j["question"])
    ret = chat(j["question"], model, tokenizer)
    try:
        print(ret)
        return {"answer": ret}
    except:
        abort(400)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)