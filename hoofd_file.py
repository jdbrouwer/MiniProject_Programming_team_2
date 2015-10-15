#This is the main file of our python program
import sqlite3, codecs, requests, datetime, xmltodict, os
from tkinter import *
import tkinter.messagebox

#Intergratie database

#XML PART

def datum():
    '''This function specifies the current date, this date is used in the request url'''
    i = datetime.datetime.now()
    date = ("%s-%s-%s" % (i.day, i.month, i.year) )
    return date

def schrijf_xml(data):
    '''This function opens filmlijst.xml and writes it into a local xml file'''
    bestand = open('filmlijst.xml', 'w')
    bestand = codecs.open('filmlijst.xml', "w", "utf-8")
    bestand.write(str(data))
    bestand.close()


def apicall():
    '''this function transfers data from the filmtotaal server, by using API, into the schrijf_xml function'''
    date = datum()
    response = requests.get('http://www.filmtotaal.nl/api/filmsoptv.xml?apikey=zmp3tnvbezlo4gbl4bh0mkro5e63xzkb&dag='+date+'&sorteer=0')
    response.encoding='utf-8'
    schrijf_xml(response.text)

def read_xml():
    '''this function makes it so that the xml file can acctually be read like string'''
    bestand = open('filmlijst.xml', 'r')
    xml_string= bestand.read()
    bestand.close()
    return xmltodict.parse(xml_string)

#The functions below are used to create lists for titels, begin time and start time

def list_titels(lijst):
    '''Here, the titles of the lists are added to a list'''
    list = []
    for film in lijst['filmsoptv']['film']:
        list.append(film['titel'])
    return(list)

def xml_date(lijst):
    list = []
    for film in lijst['filmsoptv']['film']:
        bewerk = datetime.datetime.fromtimestamp(
            int(film['starttijd'])
        ).strftime('%Y-%m-%d')
        list.append(bewerk)
    return(list)

def list_begin_time(lijst):
    '''The begin times which are listed in the xml files will be put into a list'''
    list = []
    for film in lijst['filmsoptv']['film']:
        bewerk = datetime.datetime.fromtimestamp(
            int(film['starttijd'])
        ).strftime('%H:%M:%S')
        list.append(bewerk)
    return(list)

def list_end_time(lijst):
    '''The end times which are listed in the xml files will be put into a list'''
    list = []
    for film in lijst['filmsoptv']['film']:
        bewerk = datetime.datetime.fromtimestamp(
            int(film['eindtijd'])
        ).strftime('%H:%M:%S')
        list.append(bewerk)
    return(list)

#list with providers and a list with e-mails
provider_name = ['Elmo Tilo', 'Andreas Fabian', 'Merten Bertram', 'Meinrad Severin', 'David Bernhard', 'Vinzent Timotheus']
provider_email = ['elmo.tilo@gmail.com', 'andreas.fabian@gmail.com', 'merten.bertram@gmail.com', 'mainrad.severin@gmail.com', 'david.bernhard@gmail.com', 'vinzent.timotheus@gmail.com']
provider_password = 'Welkom01'
#Creating the proper data from the API. (used to write to the database)
apicall()
data_xml = read_xml()
Film_Name = list_titels(data_xml)
Start_Time = list_begin_time(data_xml)
End_Time = list_end_time(data_xml)
Date = xml_date(data_xml)

'''SQL PART'''

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
                        Ticket_code INTEGERUNIQUE,
                        Chosen_Film STRING,
                        StartTime_Film TIME,
                        Date_Film DATE);''')
        #aanmaken van Provider Tabel
        conn.execute('''CREATE TABLE Providers
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        E_mail STRING NOT NULL UNIQUE,
                        Password STRING NOT NULL,
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

def SQL_Write_Films(Name_Film,Start,End,Date_of_Film):
    '''Writing Films from the API to the SQLLite database.'''
    sqlite_file = 'Database/db_project.sqlite'
    '''initializing SQlite connector'''
    conn = sqlite3.connect(sqlite_file)
    c= conn.cursor()
    try:
#executing sql query for each item in films
        for e in Name_Film:
            position = Name_Film.index(e)
            conn.execute('''INSERT INTO Films (Film_Name, Start_time_Film, End_time_Film, Date)
                        VALUES (?,?,?,?)''',(Name_Film[position],Start[position],End[position],Date_of_Film[position]))
    except:
            print("Could not write to Table films, Check if lists are being passed to this function")
    finally:
        conn.commit()
        conn.close()


def SQL_Write_User(user_name,email,ticket_code,chosen_film_name, chosen_film_time, chosen_film_date):
    '''Writing user information tot the database.'''
    sqlite_file = 'Database/db_project.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c= conn.cursor()
    #try:
#executing sql query for each item in fuser
    conn.execute('''INSERT INTO User (Name, E_mail, Ticket_code, Chosen_Film, StartTime_Film, Date_Film)
            VALUES (?,?,?,?,?,?)''',(user_name,email,ticket_code,chosen_film_name,chosen_film_time,chosen_film_date))
    #except:
           # print("Could not write to Table users, Check if lists are being passed to this function")
   # finally:
        #closing connection
    conn.commit()
    conn.close()

def SQL_Write_Provider(email,password,providername,film):
    sqlite_file = 'Database/db_project.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    try:
#executing sql query for each item in fuser

            conn.execute('''INSERT INTO Providers (E_mail, Password, ProviderName, Film)
                        VALUES (?,?,?,?)''',(email,password,providername,film))
    except:
            print("Could not write to provider table, Check if lists are being passed to this function")

    finally:
        #closing connection
        conn.commit()
        conn.close()

def SQL_Select_Film():
    ''' Read functions to show all databases into the film .'''
    sqlite_file = 'Database/db_project.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c= conn.cursor()
    cursor = conn.execute("SELECT Film_Name , Start_Time_Film, End_Time_Film, Date FROM Films ORDER BY Date ASC, time(Start_Time_Film) ASC")
    returnlist = []
    for row in cursor:
        returnlist.append(row)


    return returnlist






def codegenerator(name, mail, film, starttijd):
    """
 this function makes from the name, mail, film and starttijd a code
    """
    gen_name = []
    for c in name:
        shift = ord(c) + 4
        change = chr(shift)
        gen_name.append(change)
        gen_name = gen_name[:2] + gen_name[-3:]
        gen_done_name = ''.join(gen_name)
    gen_mail = []
    for h in mail:
        shift_h = ord(h) + 4
        change_h = chr(shift_h)
        gen_mail.append(change_h)
        gen_mail_2 = gen_mail[:4] + gen_mail[-4:]
        gen_done_mail = ''.join(gen_mail_2)
    e_ticket = gen_done_name +gen_done_mail+ film + starttijd
    print(e_ticket)
    return e_ticket


#SQL execution of code.
SQL_Check_DB_Directory()
SQL_Create_Database()
SQL_Write_Films(Film_Name, Start_Time, End_Time, Date)



