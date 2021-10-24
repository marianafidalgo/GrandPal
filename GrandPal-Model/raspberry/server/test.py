from transformers import AutoModelWithLMHead, AutoTokenizer, AutoConfig
import torch
import requests
import re

tokenizer = AutoTokenizer.from_pretrained('tokenizer', config=AutoConfig.from_pretrained('microsoft/DialoGPT-small'))
model = AutoModelWithLMHead.from_pretrained('GrandPal')

raw = ""
while raw != "END":
  raw = input(">> User:")
  if raw == "END":
    break

  params = {'target_lang': 'en',
      'text': raw,
      'source_lang':'ROMANCE',
      'beam_size':5}

  question = requests.get("http://localhost:24080/translate", params=params)

  print('input', question.json()["translated"][0])

  new_user_input_ids = tokenizer.encode(question.json()["translated"][0] + tokenizer.eos_token, return_tensors='pt')
  # print(new_user_input_ids)

  # append the new user input tokens to the chat history
  bot_input_ids = new_user_input_ids

  # generated a response while limiting the total chat history to 1000 tokens
  chat_history_ids = model.generate(
        bot_input_ids,
        max_length=200,
        do_sample=True,
        temperature = 0.7,
        top_k=50, # the K most likely next words are filtered and the probability mass is redistributed among only those K next words
        top_p=0.92, # chooses from the smallest possible set of words whose cumulative probability exceeds the probability p
        no_repeat_ngram_size=3,
        pad_token_id=tokenizer.eos_token_id

    )

  # pretty print last ouput tokens from bot
  output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
  print('output', output)
  sentences = re.split('((?<=[.?!]")|((?<=[.?!])(?!")))\s*', output)
  answer_=''
  for s in sentences:
      if s != '':
          answer_+=' >>pt<<'+s
  params = {'target_lang': 'ROMANCE',
      'text': answer_,
      'source_lang':'en',
      'beam_size':5}

  answer = requests.get("http://localhost:24080/translate", params=params)

  print("GrandPal: {}".format(answer.json()["translated"][0]))

  bot_input_ids = []
  chat_history_ids=[]
  print("\n")
  step=0
