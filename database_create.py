import sqlite3, os
def SQL_Check_DB_Directory():
    '''Checks the existence of the database and its folder, If database does not exist, it will create one.'''
    Database_Folder = 'Database'
#checks if the directory already exists, if it does not, it will throw an exception. (Which will usually be because of insufficent permissions)
    if not os.path.exists(Database_Folder):
        try:
            os.makedirs(Database_Folder)
        except PermissionError:
            print("Cannot create required directory, Aborting!")

def SQL_Create_Database():
    '''
    creates the database required for the program. Should be used in conjunction with SQL_Check_Database to make sure database does not already exist
    '''
    sqlite_file = 'Database/db_project.sqlite'
    #connect python en sql
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    try:
        #aanmaken van User tabel
        conn.execute('''CREATE TABLE User
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        Name STRING NOT NULL,
                        E_mail STRING  NOT NULL,
                        Ticket_code STRING UNIQUE,
                        Choosen_Film STRING,
                        StartTime_Film STRING,
                        Date_Film STRING,
                         UNIQUE (Name,E_Mail);''')
        #aanmaken van Provider Tabel
        conn.execute('''CREATE TABLE Providers
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        E_mail STRING NOT NULL UNIQUE,
                        Password String NOT NULL,
                        ProviderName STRING NOT NULL,
                        Film STRING NOT NULL);''')
        #aanmaken van film Tabel
        conn.execute('''CREATE TABLE Films
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        Film_Name STRING NOT NULL,
                        Start_Time_Film TIME,
                        End_Time_Film TIME,
                        Date DATE,
                        UNIQUE (Film_Name,Start_Time_Film,End_time_Film,Date));''')
        print('Committing to database')
        conn.commit()
        conn.close()
        print("Database created Succesfully")
    except:
        print("Database cannot be created, It might already exist...")
SQL_Check_DB_Directory()
SQL_Create_Database()