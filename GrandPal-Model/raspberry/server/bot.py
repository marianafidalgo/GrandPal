from flask import Flask
from common import cache
import torch

#def user_input():
  #get_audio()

  # Initialize recognizer class (for recognizing the speech)
  #r = sr.Recognizer()

  # Reading Audio file as source
  # listening the audio file and store in audio_text variable

#   with sr.AudioFile('tmp.wav') as source:

#       audio_text = r.listen(source)

#   # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
#       try:
#           #, language="pt-PT"
#           # using google speech recognition
#           text = r.recognize_google(audio_text)
#           print('Converting audio transcripts into text ...')
#           print(text)
#           return text

#       except:
#           print('Sorry.. run again...')
#           text = user_input()
#           return text


def chat(model, tokenizer):

    for i, sentence in enumerate(history):
        new_user_input_ids = tokenizer.encode(sentence + tokenizer.eos_token, return_tensors='pt')
        # append the new user input tokens to the chat history
        bot_input_ids = torch.cat([bot_input_ids, new_user_input_ids], dim=-1) if i > 0 else new_user_input_ids

    # generate response,
    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=150,
        do_sample=True,
        temperature = 0.7,
        top_k=50, # the K most likely next words are filtered and the probability mass is redistributed among only those K next words
        top_p=0.92, # chooses from the smallest possible set of words whose cumulative probability exceeds the probability p
        no_repeat_ngram_size=3,
        pad_token_id=tokenizer.eos_token_id
    )

    # pretty print last ouput tokens from bot
    output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    return output