__author__ = 'Jochem'

import sqlite3
#het opslaan van de sql database in /PATH/project_db.sqlite
sqlite_file = '/Users/Sebastian/Desktop/my_db.sqlite'
#connect python en sql
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


conn.commit()
conn.close()