from tkinter import *
import tkinter.messagebox
import Function_file
import pyqrcode


class Interface:
    """This is a class for the interface, all the functions related to the interface are in this class"""
    def __init__(self, master):
        """This is the main function for the interface, all statements needed for the first page of the application are in here
        :parameter      master = different name for the root window, witch is the first window
        """
        master.wm_title("Thuisbioscoop Team 2 ")
        master.geometry("310x300")
        master.configure(background="steel blue")
        upper_menu = Menu(master)
        master.config(menu=upper_menu)
        submenu = Menu(upper_menu)
        upper_menu.add_cascade(label="About", menu=submenu)
        submenu.add_command(label="Help", command=self.help)
        Label(master, text="Naam", bg="steel blue").grid(row=0, sticky=E, )
        Label(master, text="E-mailadres", bg="steel blue").grid(row=1, sticky=E)
        Button(master, text="Site voor aanbieders", command=self.provider_site).grid(row=1, column=2, columnspan=1)

    def help(self):
        """This function opens a new window with information regarding the helpdesk of the application"""
        help_window = Toplevel()
        help_window.config(background="steel blue")
        Label(help_window, text="Welkom bij onze thuisbioscoop applicatie", background="steel blue").grid(row=1)
        help_1 = Label(help_window, text="Deze applicatie kan gebruikt worden om films te reserveren "
                                         "in de thuisbioscoop.", background="steel blue")
        help_1.grid(row=2)
        help_2 = Label(help_window, text="Daarnaast is het mogelijk om de reserveringen per filmaanbieder in te zien.",
                       background="steel blue")
        help_2.grid(row=3)
        Label(help_window, text="Dit kan gedaan worden door eerst in te loggen met een geldige aanbieder.",
              background="steel blue").grid(row=4)
        Label(help_window, text="Een lijst met geldige aanbieders kan men vinden in de readme.md",
              background="steel blue").grid(row=5)

    def provider_site(self):
        """This function opens a new window that enables you to login as a film providers
        globals:        Provider_Inlog_Screen = The screen for the provider to login
                        Entry_3 = The entry for the E-mailadres
                        Entry_4 = The entry for the password"""
        global Provider_Inlog_Screen
        Provider_Inlog_Screen = Toplevel()
        Provider_Inlog_Screen.geometry("200x100")
        Provider_Inlog_Screen.config(background="steel blue")
        Label(Provider_Inlog_Screen, text="E-mail", background="steel blue").grid(row=0, sticky=E)
        Label(Provider_Inlog_Screen, text="Password", background="steel blue").grid(row=1, sticky=E)
        global entry_3
        entry_3 = Entry(Provider_Inlog_Screen)
        entry_3.grid(row=0, column=1)
        global entry_4
        entry_4 = Entry(Provider_Inlog_Screen)
        entry_4.grid(row=1, column=1)
        button_1 = Button(Provider_Inlog_Screen, text="Inloggen", command=self.loginbutton_provider)
        button_1.grid(row=2, column=1)

    def loginbutton_provider(self):
        """This function checks if a provider is logged in correctly
        if: mail and password are in the database: provider logged in succesfully
        else: provider not logged in correctly"""
        mail = entry_3.get()
        password = entry_4.get()
        if Function_file.Check_Provider_Login(mail, password):
            tkinter.messagebox.showinfo("Netflix à la 1900", "U bent succesvol ingelogd!")
            film_table_screen = Toplevel()
            film_table_screen.geometry("600x400")
            film_table_screen.config(background="steel blue")
            Label(film_table_screen, text="Hier worden uw bezoekers getoond.", background="steel blue").grid(row=1)
            t = 2
            for e in Function_file.SQL_Select_Provided_Films(mail):
                print(e)
                Label(film_table_screen, text=e).grid(row=i)
                t += 1

            """Here needs to be a function that checks all the movies of the supplier and puts them in the interface
            with all the customers"""
        else:
            tkinter.messagebox.showinfo("Netflix à la 1900", "Verkeerde inlog gegevens")
            Provider_Inlog_Screen.destroy()
            self.provider_site()



    def ticket(self, filmnaam, username, email):
        """This function creates the ticket code and also makes a qr code that connects with your ticket code
        :parameter  filmnaam= is the movies chosen by the user
                    username= the name that was entered in the login-screen of the user
                    email= the e-mailadres entered in the login-screen of the user
        """
        name_film = filmnaam[0]
        starttime = filmnaam[1]
        ticket_code = Function_file.codegenerator(username, email, name_film, starttime)
        qr_code = pyqrcode.QRCode(ticket_code)
        qr_code.show()
        # Schrijft de ticket informatie naar de database
        Function_file.SQL_Write_User(username, email, ticket_code, filmnaam[0], filmnaam[1], filmnaam[3])
        # Weergeeft de ticketcode in de UI
        ticketcode_schem = Toplevel()
        Label(ticketcode_schem, text="Uw ticketcode is als onderstaande", width=100).grid(row=1)
        Label(ticketcode_schem, text=ticket_code, width=100).grid(row=6)

    def film_site(self, name, mail):
        """This function takes you to a new window with all available movies
        :parameter      name= the name of the user got from the login
                        mail= the mail of the user got form the login
        """
        film_window = Toplevel()
        film_window.config(background="steel blue")
        label_film = Label(film_window, text="Beschikbare films vandaag", background="steel blue")
        label_film.grid(row=1)
        films_query = Function_file.SQL_Select_Film()
        row = 2
        for filmname in films_query:
            provider_name = Function_file.SQL_Select_Provider(filmname[0])
            keuze = filmname + tuple(provider_name)
            if len(keuze) > 4:
                c = Button(film_window, width=100, bg='white', text=keuze,
                           command=(lambda filmen=keuze: self.ticket(filmen, name, mail)))
                c.grid(row=row, sticky=W)
                row += 1
            else:
                continue

    def login_button(self):
        """This function saves the login that is entered in the two entry's for the user
        if: name and mail are empty: user didn't put in any data, no acces to films
        else: acces to films of that day"""
        name = entry_1.get()
        mail = entry_2.get()
        if name == "" and mail == "":
            tkinter.messagebox._show("Netflix à la 1900", "Vul uw gegevens in")
        else:
            tkinter.messagebox._show("Netflix à la 1900", "U bent succesvol ingelogd")
            self.film_site(name, mail)


root = Tk()
i = Interface(root)
p = Interface(root)
"""The entry's and buttons for the mainpage"""
entry_1 = Entry(root)
entry_2 = Entry(root)
entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)
Button(root, text="Inloggen", command=i.login_button).grid(row=2, column=1)
Button(root, text="Site voor aanbieders", command=p.provider_site).grid(row=1, column=2, columnspan=1)
root.mainloop()
