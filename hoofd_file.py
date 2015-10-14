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
                        Ticket_code STRING UNIQUE,
                        Choosen_Film STRING,
                        StartTime_Film STRING,
                        Date_Film STRING,
                         UNIQUE (Name,E_Mail);''')
        #aanmaken van Provider Tabel
        conn.execute('''CREATE TABLE Providers
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        E_mail STRING NOT NULL UNIQUE,
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
    try:
#executing sql query for each item in fuser
        for e in user_name:
            position = user_name.index(e)
            conn.execute('''INSERT INTO User (Name, E_mail, Ticket_code, Choosen_Film, StartTime_Film, Date_Film)
                        VALUES (?,?,?,?)''',(user_name[position],email[position],ticket_code[position],chosen_film_name[position], chosen_film_time[position], chosen_film_date[position]))
    except:
            print("Could not write to Table users, Check if lists are being passed to this function")
    finally:
        #closing connection
        conn.commit()
        conn.close()

def SQL_Write_Provider(name, email):
    sqlite_file = 'Database/db_project.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c= conn.cursor()

    try:
#executing sql query for each item in fuser
        for e in name:
            position = name.index(e)
            conn.execute('''INSERT INTO Providers (E_mail, ProviderName, Film)
                        VALUES (?,?,?,?)''', email[position],(name[position]))
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


#SQL execution of code.
SQL_Check_DB_Directory()
SQL_Create_Database()
SQL_Write_Films(Film_Name, Start_Time, End_Time, Date)

class Interface:

    def __init__(self, master):
        """This is the main function for the interface, all the graphic related things are in this function"""
        master.wm_title("Netflix à la 1900")
        master.geometry("310x400")
        taakbalk = Menu(master)
        master.config(menu=taakbalk)
        subMenu = Menu(taakbalk)
        taakbalk.add_cascade(label="About", menu=subMenu)
        subMenu.add_command(label="Help", command=self.Help)
        Label(master, text="Naam").grid(row=0,sticky=E)
        Label(master, text="E-mailadres").grid(row=1,sticky=E)
        canvas = Canvas(master, width=300, height=325)
        canvas.grid(row=4,column=0,columnspan=3)
        canvas.create_rectangle(0,0,370,350, fill="black")
        Button(master,text="Site voor aanbieders", command=self.aanbiederSite).grid(row=1,column=2,columnspan=1)

    def Help(self):
        """This function opens a new window with information regardinng the helpdesk of the application"""
        win = Toplevel()
        win.geometry("200x200")
        Label(win, text="Welkom bij de helpdesk").grid(row=1)

    def aanbiederInlog(self):
        """This function checks if the supplier is in the database"""
        In_database = True
        if In_database == True:
            tkinter.messagebox.showinfo("Netflix à la 1900", "U bent succesvol ingelogd!")
            film_a = Toplevel()
            film_a.geometry("600x400")
            Label(film_a, text="Hier komen de films van de aanbieder").grid(row=1)
            """Here needs to be a function that checks all the movies of the supplier and puts them in the interface
            with all the customers"""
        else:
            tkinter.messagebox.showinfo("Netflix à la 1900", "Verkeerde inlog gegevens")

    def aanbiederSite(self):
        """This function opens a new window with a site for the film suppliers """
        def loginButton_1():
            """This function does the same as loginButton but for a different page"""
            name_s = entry_3.get()
            mail_s = entry_4.get()
            self.aanbiederInlog()
        aan = Toplevel()
        aan.geometry("200x100")
        Label(aan, text="Naam").grid(row=0,sticky=E)
        Label(aan, text="E-mailadres").grid(row=1,sticky=E)
        entry_3 = Entry(aan)
        entry_3.grid(row=0, column=1)
        entry_4 = Entry(aan)
        entry_4.grid(row=1, column=1)
        Button(aan, text="Inloggen", command=loginButton_1).grid(row=2,column=1)

root = Tk()
i = Interface(root)

def loginButton():
        """This function saves the login that is entered in the two entry's"""
        def ticket(filmnaam):
                ticket1 = Toplevel()
                ticket1.geometry("600x400")
                Label(ticket1, text=filmnaam).grid(row=1)
                print(filmnaam)
        def Movies():
            """This function takes you to a new window with all available movies"""
            film = Toplevel()
            film.geometry("300x300")
            label_film = Label(film, text="Beschikbare films vandaag")
            label_film.grid(row=1)
            #voor het gemak ff een list
            films = SQL_Select_Film()
            row = 2
            for filmnaam in films:
                c = Button(film, text=filmnaam, command=(lambda filmen=filmnaam: ticket(filmen)))
                c.grid(row=row, sticky=W)
                row +=1
        In_database_2 = True
        name = entry_1.get()
        mail = entry_2.get()
        print("Naam: ", name)
        print("Mail: ", mail)
        if In_database_2 is True:
                tkinter.messagebox._show("Netflix à la 1900", "U bent succesvol ingelogd")
        else:
                tkinter.messagebox.show("Netflix à la 1900", "U bent een nieuwe klant, welkom!")
        Movies()

entry_1 = Entry(root)
entry_2 = Entry(root)
entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)
Button(root, text="Inloggen", command=loginButton).grid(row=2,column=1)
root.mainloop()

