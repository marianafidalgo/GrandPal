import streamlit as st
import pandas as pd
import requests
import re
import sqlite3

st.set_page_config(layout="wide")

def write_history(msgHistoty):

    col1, col2 = st.columns([1,8])

    for index, msg in enumerate(reversed(msgHistoty)):

        if index%2 == 0:

            col1.write('**GrandPal:**')
            col2.write(msg)

        else:

            col1.write('**You:**')
            col2.write(msg)

    return

def pt_en_translate(pt_str: str) -> str:
    params = {'target_lang': 'en',
                'text': pt_str,
                'source_lang':'ROMANCE',
                'beam_size':5}

    question = requests.get("http://translation-api:80/translate", params=params)

    en_str = question.json()["translated"][0]

    return en_str

def en_pt_translate(en_str: str) -> str:
    sentences = re.split('((?<=[.?!]")|((?<=[.?!])(?!")))\s*', en_str)
    answer_=''
    for s in sentences:
        if s != '':
            answer_+=' >>pt<<'+s

    params = {'target_lang': 'ROMANCE',
        'text': answer_,
        'source_lang':'en',
        'beam_size':5}
    question = requests.get("http://translation-api:80/translate", params=params)
    answer_pt = question.json()["translated"][0]

    return  answer_pt

@st.cache(hash_funcs={sqlite3.Connection: id}, allow_output_mutation=True)
def dbConnection():

    return sqlite3.connect('chat-rating.db', check_same_thread=False)


def main():

    if 'msgHistory' not in st.session_state:
        st.session_state.msgHistory = []
    if 'msgHistory_pt' not in st.session_state:
        st.session_state.msgHistory_pt = []

    st.title("GrandPal - Portuguese Chatbot")

    st.subheader("Engage in a conversation with GrandPal in Portuguese! You will be able to evaluate its quality from 1 to 10.")
    #st.subheader("**You will be able to evaluate its quality from 1 to 10.**")

    col1, col2 = st.columns([3,1])

    with col1.form(key = 'send_msg', clear_on_submit=True):

        #if len(st.session_state.msgHistory) > 0:
        #    st.write(st.session_state.msgHistory_pt[-1])
        #else:
        st.write('**GrandPal: **','Fala comigo! :)')

        user_msg = st.text_input(label="Insert Text Here")
        send_msg_button = st.form_submit_button(label='Send')


    if send_msg_button:
    #send message to API
        st.session_state.msgHistory_pt.append(user_msg)
        en_str = pt_en_translate(pt_str=user_msg)
        st.session_state.msgHistory.append(en_str)

        #receive message from API
        resp = requests.post("http://bot-api:5000/input", json = {"question": st.session_state.msgHistory[-5:]})

        if(resp.status_code == 200):
            answer = resp.json()
            answer_pt = en_pt_translate(en_str=answer["answer"])
            st.session_state.msgHistory.append(answer["answer"])

            st.session_state.msgHistory_pt.append(answer_pt)
            write_history(st.session_state.msgHistory_pt)


    if int(len(st.session_state.msgHistory)) >= 6:

        with col2.form(key = 'evaluate', clear_on_submit=True):

            rating = st.number_input(label="Evaluate GrandPal Performance from 1-10", min_value=1, max_value=10, step=1, key='rate', value=5)

            submit_rating_button = st.form_submit_button(label='Submit')

        if submit_rating_button:

            insert_query = f"insert into rating (rate) values ({rating});"

            c = dbConnection()
            c.execute(insert_query)
            c.commit()

            st.session_state.msgHistory = []
            st.session_state.msgHistory_pt = []

    else:
        col2.subheader(f'You need {int(len(st.session_state.msgHistory))}/6 minimum interactions in order to be able to submit an evaluation!')

if __name__ == '__main__':
    main()
