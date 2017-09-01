import sqlite3

conn = sqlite3.connect('data.db')
db = conn.cursor()

db.execute('''CREATE TABLE ranks (filename text, rank real)''')

conn.commit()
conn.close()
