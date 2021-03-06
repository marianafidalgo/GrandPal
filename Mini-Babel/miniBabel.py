import streamlit as st
import pandas as pd
import sqlite3
from streamlit.script_runner import RerunException

from streamlit.type_util import Key

st.set_page_config(layout="wide", page_title='GrandPal-Translation Quality')

def translationRater(eng: st, pt: str, index: int) -> int:

    col1, col2, col3 =  st.columns([3,3,1])

    col1.write(eng)
    col2.write(pt)
    rating = col3.number_input(label="", min_value=1, max_value=10, step=1, key=index, value=5)

    st.write('---')

    return rating

@st.cache(hash_funcs={sqlite3.Connection: id}, allow_output_mutation=True)
def dbConnection():
    
    return sqlite3.connect('miniBabel.db', check_same_thread=False)

def selectTranslations(num_translations, num_ratings, cnx):
    limit_translations = 14

    if num_ratings >= num_translations:
        translations = pd.read_sql_query(f"select t.rowid, * from translations as t order by RANDOM() limit {limit_translations}", cnx)
    else:
        translations = pd.read_sql_query(f"select t.rowid, * from translations as t left join rating as r on t.rowid = r.id order by RANDOM() limit {limit_translations}", cnx)

    return translations


def main():
    st.title("Translation Quality Evaluation")

    st.subheader("Please give a rating from 1-10 regarding the quality of the translations.\n These translations were generated by a Machine Translation Model.")

    st.write('---')

    with st.form(key = 'my_form', clear_on_submit=True):

        cnx = dbConnection()

        num_translations = cnx.execute("select count(*) from translations;").fetchall()[0][0]
        num_ratings = cnx.execute("select count(*) from rating;").fetchall()[0][0]

        #st.write(num_ratings, num_translations)

        col1, col2, col3 =  st.columns([3,3,1])

        col1.write('**English**')
        col2.write('**Portuguese**')
        col3.write(f"Already done: {num_ratings}/{num_translations}")

        translations = selectTranslations(num_translations, num_ratings, cnx)
        ratings = []

        for index, row in translations.iterrows():
            
            ratings.append(translationRater(row['english'], row['portuguese'], index))

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        for index, row in translations.iterrows():
            translation_id = row["rowid"]
            rating = ratings[index]

            insert_query = f"insert into rating (id, rate) values ({translation_id}, {rating});"

            c = dbConnection()
            c.execute(insert_query)
            c.commit()

        st.experimental_rerun()
            

if __name__ == '__main__':
    main()
