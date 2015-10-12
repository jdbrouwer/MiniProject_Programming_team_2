#This is the main file of our python program:
import sqlite3

def SQL_Write_Films(Film_Name,Start_Time,End_Time,Date):

    #SQLlite database needs to be defined
    sqlite_file = 'A File needs to be here'

    #initializing SQlite connector
    conn = sqlite3.connect(sqlite_file)
    c= conn.cursor()

    #executing query with variables that can be passed through to the function.
    conn.execute('''INSERT INTO Films (Film_Name, Start_time, End_time, Date)
                VALUES (?,?,?,?)''',(Film_Name,Start_Time,End_Time,Date))
    conn.commit()
    conn.close()

