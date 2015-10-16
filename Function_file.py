# This is the main file of our python program
import sqlite3
import codecs
import requests
import datetime
import xmltodict
import os
# Intergratie
# XML PART


def datum():
    """This function specifies the current date, this date is used in the request url"""
    i = datetime.datetime.now()
    date = ("%s-%s-%s" % (i.day, i.month, i.year))
    return date


def schrijf_xml(data):
    """This function opens filmlijst.xml and writes it into a local xml file
    :parameter     data = is the current date
    """
    open('filmlijst.xml', 'w')
    bestand = codecs.open('filmlijst.xml', "w", "utf-8")
    bestand.write(str(data))
    bestand.close()


def apicall():
    """this function transfers data from the filmtotaal server, by using API, into the schrijf_xml function"""
    date = datum()
    response = requests.get('http://www.filmtotaal.nl/api/filmsoptv.xml?apikey=zmp3tnvbezlo4gbl4bh0mkro5e63xzkb&dag=' +
                            date+'&sorteer=0')
    response.encoding = 'utf-8'
    schrijf_xml(response.text)


def read_xml():
    """this function makes it so that the xml file can actually be read like string"""
    bestand = open('filmlijst.xml', 'r')
    xml_string = bestand.read()
    bestand.close()
    return xmltodict.parse(xml_string)


# The functions below are used to create lists for titels, begin time and start time


def list_titels(lijst):
    """Here, the titles of the lists are added to a list
    :parameter      lijst =the data from the API """
    list_1 = []
    for film in lijst['filmsoptv']['film']:
        list_1.append(film['titel'])
    return list_1


def xml_date(lijst):
    """This function determines what the date is today
    :parameter      lijst =the data from the API"""
    list_1 = []
    for film in lijst['filmsoptv']['film']:
        bewerk = datetime.datetime.fromtimestamp(
            int(film['starttijd'])
        ).strftime('%Y-%m-%d')
        list_1.append(bewerk)
    return list_1


def list_begin_time(lijst):
    """The begin times which are listed in the xml files will be put into a list
    :parameter      lijst =the data from the API """
    list_1 = []
    for film in lijst['filmsoptv']['film']:
        bewerk = datetime.datetime.fromtimestamp(
            int(film['starttijd'])
        ).strftime('%H:%M:%S')
        list_1.append(bewerk)
    return list_1


def list_end_time(lijst):
    """
    The end times which are listed in the xml files will be put into a list
    :parameter      lijst = the data from the API
    """
    list_1 = []
    for film in lijst['filmsoptv']['film']:
        bewerk = datetime.datetime.fromtimestamp(
            int(film['eindtijd'])
        ).strftime('%H:%M:%S')
        list_1.append(bewerk)
    return list_1

# list with providers and a list with e-mails
provider_name = ['Elmo Tilo', 'Andreas Fabian', 'Merten Bertram', 'Meinrad Severin', 'David Bernhard',
                 'Vinzent Timotheus']
provider_email = ['elmo.tilo@gmail.com', 'andreas.fabian@gmail.com', 'merten.bertram@gmail.com',
                  'mainrad.severin@gmail.com', 'david.bernhard@gmail.com', 'vinzent.timotheus@gmail.com']
provider_password = ['Welkom01', 'Welkom02', 'Welkom03', 'Welkom04', 'Welkom05', 'Welkom06']
# Creating the proper data from the API. (used to write to the database)
apicall()
data_xml = read_xml()
Film_Name = list_titels(data_xml)
Start_Time = list_begin_time(data_xml)
End_Time = list_end_time(data_xml)
Date = xml_date(data_xml)


# SQL PART


def SQL_Check_DB_Directory():
    """Checks the existence of the database and its folder, If database does not exist, it will create one."""
    database_folder = 'Database'
    # checks if the directory already exists, if it does not, it will throw an exception. (Which will usually be because
    # of insufficent permissions)
    if not os.path.exists(database_folder):
        try:
            os.makedirs(database_folder)
        except PermissionError:
            print("Cannot create required directory, Aborting!")


def SQL_Create_Database():
    """
    creates the database required for the program. Should be used in conjunction with SQL_Check_Database to make sure
    database does not already exist
    """
    sqlite_file = 'Database/db_project.sqlite'
    # connect python en sql
    conn = sqlite3.connect(sqlite_file)
    try:
        # aanmaken van User tabel
        conn.execute('''CREATE TABLE User
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        Name STRING NOT NULL,
                        E_mail STRING  NOT NULL,
                        Ticket_code INTEGERUNIQUE,
                        Chosen_Film STRING,
                        StartTime_Film TIME,
                        Date_Film DATE);''')
        # aanmaken van Provider Tabel
        conn.execute('''CREATE TABLE Providers
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        E_mail STRING NOT NULL UNIQUE,
                        Password STRING NOT NULL,
                        ProviderName STRING NOT NULL,
                        Film STRING NOT NULL);''')
        # aanmaken van film Tabel
        conn.execute('''CREATE TABLE Films
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        Film_Name STRING NOT NULL,
                        Start_Time_Film TIME,
                        End_Time_Film TIME,
                        Date DATE,
                        UNIQUE (Film_Name,Start_Time_Film,End_time_Film,Date));''')
        print('Committing to database')
        print("Database created Succesfully")
    except:
        print("Database cannot be created, It might already exist...")

    finally:
        conn.commit()
        conn.close()


def SQL_Write_Films(name_film, start, end, date_of_film):
    """Writing Films from the API to the SQLLite database.
    :parameter      name_film = Name of the film of the API
                    Start = Start time of the film
                    End = End time of the film
                    Date_of_Film = The date of film
    """
    sqlite_file = 'Database/db_project.sqlite'
    """initializing SQlite connector"""
    conn = sqlite3.connect(sqlite_file)
    try:
        # executing sql query for each item in films
        for e in name_film:
            position = name_film.index(e)
            conn.execute('''INSERT INTO Films (Film_Name, Start_time_Film, End_time_Film, Date)
                        VALUES (?,?,?,?)''', (name_film[position], start[position], end[position],
                                              date_of_film[position]))
    except:
            print("Could not write to Table films, Check if lists are being passed to this function")
    finally:
        conn.commit()
        conn.close()


def SQL_Write_User(user_name, email, ticket_code, chosen_film_name, chosen_film_time, chosen_film_date):
    """This function writes user information tot the database.
    :parameter      user_name = column of the user table in the database
                    email = column of the user table in the database
                    ticket_code = column of the user table in the database
                    chosen_film = column of the user table in the database
                    chosen_film_time = column of the user table in the database
                    chosen_film_date = column of the user table in the database
    """
    sqlite_file = 'Database/db_project.sqlite'
    conn = sqlite3.connect(sqlite_file)
    
    try:
        # executing sql query for each item in fuser
        conn.execute('''INSERT INTO User (Name, E_mail, Ticket_code, Chosen_Film, StartTime_Film, Date_Film)
        VALUES (?,?,?,?,?,?)''', (user_name, email, ticket_code, chosen_film_name, chosen_film_time, chosen_film_date))
    except:
            print("Could not write to Table users, Check if lists are being passed to this function")
    finally:
        # closing connection
        conn.commit()
        conn.close()


def SQL_Write_Provider(email,password,providername,film):
    """This function writes information in the providers table
    :parameter      email = the e-mail of the provider
                    password = the password of the provider
                    providername = the name of the provider
                    film = the film that the provider hosts
    """
    sqlite_file = 'Database/db_project.sqlite'
    conn = sqlite3.connect(sqlite_file)
    try:
        # executing sql query for each item in fuser
        for e in provider_name:
            stap = provider_name.index(e)

            conn.execute('''INSERT INTO Providers (E_mail, Password, ProviderName, Film)
                        VALUES (?,?,?,?)''', (email[stap], password[stap], providername[stap], film[stap]))
    except:
            print("Could not write to provider table, Check if lists are being passed to this function")
    finally:
        # closing connection
        conn.commit()
        conn.close()


def SQL_Select_Film():
    """Read functions to show all databases into the film ."""
    sqlite_file = 'Database/db_project.sqlite'
    conn = sqlite3.connect(sqlite_file)
    try:
        cursor = conn.execute("SELECT Film_Name,Start_Time_Film, End_Time_Film, Date FROM Films ORDER BY Date ASC, time"
                              "(Start_Time_Film) ASC")
        cursordata = cursor.fetchall()
    except:
        print("Cannot select film from film table")

    finally:
        conn.commit()
        conn.close()
        return cursordata


def SQL_Select_Provider(FilmName):
    """Read functions to show all databases into the film .
    :parameter      FilmName = ??"""
    sqlite_file = 'Database/db_project.sqlite'
    conn = sqlite3.connect(sqlite_file)
    try:
        cursor = conn.execute("SELECT ProviderName FROM Providers WHERE Film = ?", ([FilmName]))
        cursordata = cursor.fetchall()
    except:
        print("Cannot select users from provider table, Do they exist?")
    finally:
        conn.commit()
        conn.close()
        return cursordata


def Check_Provider_Login(Provider_Email, Password):
    """ Checks passwords for the providers to make sure the input matches the database,
    :return     Ture or False
    :parameter  Provider_Email = E-mail of the provider
                Password = Password of the provider"""
    sqlite_file = 'Database/db_project.sqlite'
    conn = sqlite3.connect(sqlite_file)
    
    cursor = conn.execute('''SELECT E_Mail, Password FROM Providers WHERE E_Mail = ? AND Password = ?''',
                          (str(Provider_Email), str(Password)))
    checkvalue = (len(cursor.fetchall()))
    print(type(checkvalue))
    if checkvalue == 1:
        return True
    if checkvalue == 0:
        return False


def SQL_Select_Provided_Films(Provider_E_mail):
    """
    This function gets all names ,who have chosen the same film as the provider, out of the database
    :return         This function retrieves all
    :parameter      Provider_E_mail = The e-mail of the provider
    """
    sqlite_file = 'Database/db_project.sqlite'
    conn = sqlite3.connect(sqlite_file)
    try:

        cursor = conn.execute('''SELECT StartTime_Film,Name,Film,Date_Film,Ticket_code
                                 FROM Providers INNER JOIN User on Providers.Film = User.Chosen_Film
                                 WHERE Providers.E_mail = ?
                                 ORDER BY Time(User.StartTime_Film) ASC, User.Name ASC''',([Provider_E_mail]))
        cursordata = cursor.fetchall()

    # except:
    # print("Could not write to Table asdfadsfasdf, Check if lists are being passed to this function")
    finally:
        # closing connection
        conn.commit()
        conn.close()
        return cursordata


def codegenerator(name, mail, film, starttijd):
    """
    This function makes from the name, mail, film and starttime of the film a code for a unique ticket
    :parameter      name = name of the user
                    mail = e-mailadres of the server
                    film = the movie selected by the user
                    starttijd = the starttime of the movie
    """
    gen_name = []
    for c in name:
        shift = ord(c) + 4
        change = chr(shift)
        gen_name.append(change)
        gen_name_2 = gen_name[:2] + gen_name[-3:]
        gen_done_name = ''.join(gen_name_2)
    gen_mail = []
    for h in mail:
        shift_h = ord(h) + 4
        change_h = chr(shift_h)
        gen_mail.append(change_h)
        gen_mail_2 = gen_mail[:4] + gen_mail[-4:]
        gen_done_mail = ''.join(gen_mail_2)
    e_ticket = gen_done_name + gen_done_mail + film + starttijd
    return e_ticket

# SQL execution of code.
SQL_Check_DB_Directory()
SQL_Create_Database()
SQL_Write_Films(Film_Name, Start_Time, End_Time, Date)
SQL_Write_Provider(provider_email, provider_password, provider_name, Film_Name)
print(SQL_Select_Provided_Films('andreas.fabian@gmail.com'))
