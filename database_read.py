__author__ = 'Jochem'

import sqlite3
#het openen van een sql database in /PATH
sqlite_file = '/Users/Sebastian/Desktop/my_db.sqlite'
#connect python en sql
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


conn.commit()
conn.close()