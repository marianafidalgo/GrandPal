import sqlite3
import csv
import pandas as pd

conn = sqlite3.connect('miniBabel.db')

c = conn.cursor()

c.execute("""CREATE TABLE translations (
            english TEXT,
            portuguese TEXT
            )""")

c.execute ("""CREATE TABLE rating (
            id INTEGER,
            rate INTEGER
            )""")

df = pd.read_csv('translationDB.csv')
df.to_sql('translations', conn, if_exists='append', index=False)

c.commit()