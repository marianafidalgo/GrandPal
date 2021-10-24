from flask import Flask, abort, request
from transformers import AutoModelWithLMHead, AutoTokenizer, AutoConfig
import json

from common import cache

from bot import chat

app = Flask(__name__)

chat_history = []
cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': '/tmp'})

cache.set("chat_history", chat_history)

tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-small')
model = AutoModelWithLMHead.from_pretrained('GrandPal')

@app.route('/input', methods = ["POST"])
def input():
    cache.get("chat_history", chat_history)
    j = request.get_json()
    print(j["question"])
    chat_history.append(j["question"])
    ret = chat(chat_history[-5:], model, tokenizer)
    try:
        print(chat_history)
        chat_history.append(ret)
        cache.set("chat_history", chat_history)
        return {"answer": ret}
    except:
        abort(400)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)