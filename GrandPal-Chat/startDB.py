import sqlite3
import csv
import pandas as pd

conn = sqlite3.connect('chat-rating.db')

c = conn.cursor()

c.execute ("""CREATE TABLE rating (
            rate INTEGER
            )""")
