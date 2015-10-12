__author__ = 'Jochem'

import sqlite3
sqlite_file = '/Users/Sebastian/Desktop/my_db.sqlite'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


conn.commit()
conn.close()