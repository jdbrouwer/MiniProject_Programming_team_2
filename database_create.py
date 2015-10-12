#creert een database voor het gebruik van de applicatie. Dit script creert de database.

import sqlite3
#het opslaan van de sql database in /PATH/project_db.sqlite
#path comment jacob D:\HU_DATA\Python_miniproject\db_project.sqlite


#sqlite_file = 'C:\Documenten\HBO-ICT\Python project\database\db_project.sqlite'
sqlite_file = 'D:\HU_DATA\Python_miniproject\db_project.sqlite'
#connect python en sql
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

#aanmaken van User tabel
conn.execute('''CREATE TABLE User
                (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Name STRING NOT NULL
                E_mail STRING UNIQUE NOT NULL,
                Ticket_code STRING UNIQUE,
                Gekozen_Film STRING,
                StartTime_Film,
                Date_Film);''')

#aanmaken van Provider Tabel
conn.execute('''CREATE TABLE Providers
                (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                E_mail STRING NOT NULL UNIQUE,
                ProviderName STRING NOT NULL,
                Film STRING NOT NULL);''')

#aanmaken van film database
conn.execute('''CREATE TABLE Films
                (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Film_Name STRING NOT NULL,
                Start_Time_Film TIME,
                End_Time_Film TIME,
                Date DATE);''')


print('Committing to database')
conn.commit()
conn.close()

print("Database created Succesfully")