#!/usr/bin/env python3
from flask import Flask, abort, request, redirect, jsonify
import json
from flask import render_template
import requests

from common import cache

from bot import chat

app = Flask(__name__)

print("ups")
bot_input_ids = []
chat_history_ids = []
cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': '/tmp'})

cache.set("bot_input_ids", bot_input_ids)
cache.set("chat_history_ids", chat_history_ids)
cache.set("step", 0)

@app.route('/input', methods = ["POST"])
def input():
    j = request.get_json()
    print(j["question"])
    ret = chat(j["question"])
    try:
        print(ret)
        return {"answer": ret}
    except:
        abort(400)


if __name__ == "__main__":
    app.run(host='192.168.1.85', port=4000, debug=True)