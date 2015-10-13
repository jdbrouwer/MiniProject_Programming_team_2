#This is the main file of our python program
import sqlite3, codecs, requests, datetime, xmltodict
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

data_xml = read_xml()
Film_Name = list_titels(data_xml)
Start_Time = list_begin_time(data_xml)
End_Time = list_end_time(data_xml)
Date = xml_date(data_xml)

'''SQL PART'''

def SQL_Write_Films(Name_Film,Start,End,Date_of_Film):

    '''Writing Films from the API to the SQLLite database.'''
    sqlite_file = '..\db_project.sqlite'

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
            print("Could not write to database, Check if lists are being passed to this function")

    finally:

        conn.commit()
        conn.close()

SQL_Write_Films(Film_Name, Start_Time, End_Time, Date)

def SQL_Write_User(user_name,email,ticket_code,chosen_film):
    '''Writing user information tot the database.'''
    sqlite_file = '..\db_project.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c= conn.cursor()

    try:
#executing sql query for each item in fuser
        for e in user_name:
            position = user_name.index(e)
            conn.execute('''INSERT INTO User (Film_Name, Start_time_Film, End_time_Film, Date)
                        VALUES (?,?,?,?)''',(user_name[position],email[position],ticket_code[position],chosen_film[position]))
    except:
            print("Could not write to database, Check if lists are being passed to this function")

    finally:
        #closing connection
        conn.commit()
        conn.close()


def SQL_Select_Film():
    ''' Read functions to show all databases into the film .'''
    sqlite_file = '..\db_project.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c= conn.cursor()

    cursor = conn.execute("SELECT Film_Name , Start_Time_Film, End_Time_Film, Date from Films")

    returnlist = []
    for row in cursor:
        returnlist.append(row)


    return returnlist


#Intergratie UI

class Interface:

    def __init__(self, master):
        """This is the main function for the interface, all the graphic related things are in this function"""
        master.wm_title("Netflix à la 1900")
        master.geometry("600x400")

        taakbalk = Menu(master)
        master.config(menu=taakbalk)
        subMenu = Menu(taakbalk)
        taakbalk.add_cascade(label="About", menu=subMenu)
        subMenu.add_command(label="Help", command=self.Help)

        label_naam = Label(master, text="Naam")
        label_email = Label(master, text="E-mailadres")
        label_space = Label(master, text="                               ")
        label_naam.grid(row=0, sticky=E)
        label_email.grid(row=1, sticky=E)
        label_space.grid(row=4, column=2)

        info_text = Label(root, text="Met deze applicatie kunt u zich opgeven voor een film \n bij één van de aanbieders. "
                             "Voer uw naam en \n e-mailadres in en kies een film om te bezoeken \n ")
        info_text.grid(row=4, column=0 , rowspan=5, columnspan=5, sticky=W)

        canvas = Canvas(master, width=300, height=325)
        canvas.grid(row=4, column=3)
        canvas.create_rectangle(0,0,350,350, fill="black")

        button_2 = Button(master,text="Site voor aanbieders", command=self.aanbiederSite)
        button_2.grid(row=1, column=3)

    def Help(self):
        """This function opens a new window with information regardinng the helpdesk
        of the application"""
        win = Toplevel()
        win.geometry("200x200")
        message = "Welkom bij de helpdesk"
        labelhelp = Label(win, text=message)
        labelhelp.grid(row=1)

    def aanbiederInlog(self):
        """This function checks if the supplier is in the database"""
        In_database = True
        if In_database == True:
            tkinter.messagebox.showinfo("Netflix à la 1900", "U bent succesvol ingelogd!")
            film_a = Toplevel()
            film_a.geometry("600x400")
            label_test = Label(film_a, text="Hier komen de films van de aanbieder")
            label_test.grid(row=1)
            """Here needs to be a function that checks all the movies of the supplier and puts them in the interface
            with all the customers"""
        elif In_database != True:
            tkinter.messagebox.showinfo("Netflix à la 1900", "Verkeerde inlog gegevens")

    def aanbiederSite(self):
        """This function opens a new window with a site for the film suppliers """
        def loginButton_1():
            """This function does the same as loginButton but for a different page"""
            name_s = entry_3.get()
            mail_s = entry_4.get()
            print(name_s)
            print(mail_s)
            self.aanbiederInlog()


        aan = Toplevel()
        aan.geometry("200x100")

        label_naam = Label(aan, text="Naam")
        label_email = Label(aan, text="E-mailadres")
        label_naam.grid(row=0, sticky=E)
        label_email.grid(row=1, sticky=E)

        entry_3 = Entry(aan)
        entry_4 = Entry(aan)
        entry_3.grid(row=0, column=1)
        entry_4.grid(row=1, column=1)
        button_3 = Button(aan, text="Inloggen", command=loginButton_1)
        button_3.grid(row=2, column=1)

    def Movies(self):
        """This function takes you to a new window with all available movies"""
        t = loginButton()
        if t == 2:
            film = Toplevel()
            film.geometry("300x300")

root = Tk()
i = Interface(root)

def loginButton():
        """This function saves the login that is entered in the two entry's"""
        def Movies():
            """This function takes you to a new window with all available movies"""
            film = Toplevel()
            film.geometry("300x300")
            label_film = Label(film, text="Beschikbare films vandaag")
            label_film.grid(row=1)
            #voor het gemak ff een list
            films = SQL_Select_Film()
            row = 2
            for i in films:
                c = Checkbutton(film, text=i)
                c.grid(row=row)
                row +=1

        teller = 1
        In_database_2 = True
        name = entry_1.get()
        mail = entry_2.get()
        print("Naam: ", name)
        print("Mail: ", mail)
        if In_database_2 == True:
                tkinter.messagebox._show("Netflix à la 1900", "U bent succesvol ingelogd")
        elif In_database_2 != True:
                tkinter.messagebox.show("Netflix à la 1900", "U bent een nieuwe klant, welkom!")
        Movies()

entry_1 = Entry(root)
entry_2 = Entry(root)
entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)
button_1 = Button(root, text="Inloggen", command=loginButton)
button_1.grid(row=2, column=1)


root.mainloop()
