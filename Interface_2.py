from tkinter import *
import tkinter.messagebox
import hoofd_file
import pyqrcode


class Interface:
    """This is a class for the interface, all the functions related to the interface are in this class"""
    def __init__(self, master):
        """This is the main function for the interface, all statements needed for the first page of the aplication are in here
        :parameter      master = different name for the root window, wich is the first window
        """
        master.wm_title("Netflix à la 1900")
        master.geometry("310x400")
        taakbalk = Menu(master)
        master.config(menu=taakbalk)
        submenu = Menu(taakbalk)
        taakbalk.add_cascade(label="About", menu=submenu)
        submenu.add_command(label="Help", command=self.Help)
        Label(master, text="Naam").grid(row=0, sticky=E)
        Label(master, text="E-mailadres").grid(row=1, sticky=E)
        canvas = Canvas(master, width=300, height=325)
        canvas.grid(row=4, column=0, columnspan=3)
        Button(master, text="Site voor aanbieders", command=self.ProviderSite).grid(row=1, column=2, columnspan=1)

    def Help(self):
        """This function opens a new window with information regarding the helpdesk of the application"""
        win = Toplevel()
        win.geometry("200x200")
        Label(win, text="Welkom bij de helpdesk").grid(row=1)

    def ProviderSite(self):
        """This function opens a new window that enables you to login as a film providers"""
        global Provider_Inlog_Screen
        Provider_Inlog_Screen = Toplevel()
        Provider_Inlog_Screen.geometry("200x100")
        Label(Provider_Inlog_Screen, text="E-mail").grid(row=0, sticky=E)
        Label(Provider_Inlog_Screen, text="Password").grid(row=1, sticky=E)
        global entry_3
        entry_3 = Entry(Provider_Inlog_Screen)
        entry_3.grid(row=0, column=1)
        global entry_4
        entry_4 = Entry(Provider_Inlog_Screen)
        entry_4.grid(row=1, column=1)
        button1 = Button(Provider_Inlog_Screen, text="Inloggen", command=self.loginButton_provider)
        button1.grid(row=2, column=1)

    def loginButton_provider(self):
        """This function does the same as loginButton but for a different page"""
        mail = entry_3.get()
        password = entry_4.get()
        if hoofd_file.Check_Provider_Login(mail, password):
            tkinter.messagebox.showinfo("Netflix à la 1900", "U bent succesvol ingelogd!")
            film_a = Toplevel()
            film_a.geometry("600x400")
            Label(film_a, text="Hier komen de films van de aanbieder").grid(row=1)
            i = 2
            for e in hoofd_file.SQL_Select_Provided_Films(mail):
                print(e)
                Label(film_a, text=e).grid(row=i)
                i += 1

            """Here needs to be a function that checks all the movies of the supplier and puts them in the interface
            with all the customers"""
        else:
            tkinter.messagebox.showinfo("Netflix à la 1900", "Verkeerde inlog gegevens")
            self.ProviderSite()

    def ticket(self, filmnaam, username, email):
        """This function creates the ticket code and also makes a qr code that connects with your ticket code
        :parameter  filmnaam= is the movies chosen by the user
                    username= the name that was entered in the login-screen of the user
                    email= the e-mailadres entered in the login-screen of the user
        """
        naam_film = filmnaam[0]
        begintijd = filmnaam[1]
        ticket_code = hoofd_file.codegenerator(username, email, naam_film, begintijd)
        qr = pyqrcode.QRCode(ticket_code)
        qr.show()
        # Schrijft de ticket informatie naar de database
        hoofd_file.SQL_Write_User(username, email, ticket_code, filmnaam[0], filmnaam[1], filmnaam[3])
        # Weergeeft de ticketcode in de UI
        ticketcode_schem = Toplevel()
        Label(ticketcode_schem, text="Uw ticketcode is als onderstaande", width=100).grid(row=1)
        Label(ticketcode_schem,text=ticket_code, width=100).grid(row=6)

    def Film_Site(self, name, mail):
        """This function takes you to a new window with all available movies
        :parameter      name= the name of the user got from the login
                        mail= the mail of the user got form the login
        """
        film_window = Toplevel()
        label_film = Label(film_window, text="Beschikbare films vandaag")
        label_film.grid(row=1)
        films_query = hoofd_file.SQL_Select_Film()
        row = 2
        for filmnaam in films_query:
            provider_name = hoofd_file.SQL_Select_Provider(filmnaam[0])
            keuze = filmnaam + tuple(provider_name)
            if len(keuze) > 4:
                c = Button(film_window, width=100, bg = 'white', text=keuze,
                           command=(lambda filmen=keuze: self.ticket(filmen, name, mail)))
                c.grid(row=row, sticky=W)
                row += 1
            else:
                continue

    def loginButton(self):
        """This function saves the login that is entered in the two entry's for the user """
        name = entry_1.get()
        mail = entry_2.get()
        if name == "" and mail == "":
            tkinter.messagebox._show("Netflix à la 1900", "Vul uw gegevens in")
        else:
            tkinter.messagebox._show("Netflix à la 1900", "U bent succesvol ingelogd")
            self.Film_Site(name, mail)

root = Tk()
i = Interface(root)
p = Interface(root)
"""The entry's and buttons for the mainpage"""
entry_1 = Entry(root)
entry_2 = Entry(root)
entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)
Button(root, text="Inloggen", command=i.loginButton).grid(row=2, column=1)
Button(root, text="Site voor aanbieders", command=p.ProviderSite).grid(row=1, column=2, columnspan=1)
root.mainloop()
