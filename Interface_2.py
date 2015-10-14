from tkinter import *
import tkinter.messagebox
import hoofd_file
from PIL import Image, ImageTk
import pyqrcode

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
        def loginButton_provider(self):
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
        Button(aan, text="Inloggen", command=loginButton_provider).grid(row=2,column=1)

    def ticket(filmnaam,username,email):
        naam_film = filmnaam[0]
        begintijd = filmnaam[1]
        ticket_code = hoofd_file.codegenerator(username,email,naam_film,begintijd)
        print(ticket_code)
        url = pyqrcode.create(ticket_code)
        url.png("qrcode.png", scale=10)

    def Movies(self,ticket):
        """This function takes you to a new window with all available movies"""
        film_window = Toplevel()
        film_window.geometry("300x300")
        label_film = Label(film_window, text="Beschikbare films vandaag")
        label_film.grid(row=1)
        #voor het gemak ff een list
        films_query = hoofd_file.SQL_Select_Film()
        row = 2
        for filmnaam in films_query:
            c = Button(film_window, text=filmnaam, command=(lambda filmen=filmnaam: ticket(filmen)))
            c.grid(row=row, sticky=W)
            row +=1

    def loginButton(self):
    #This function saves the login that is entered in the two entry's#
        name = entry_1.get()
        mail = entry_2.get()
        hoofd_file.SQL_Write_User(name,mail, '11111111','henk', '05:00:00', '2015-11-13')
        if name == "" and mail == "":
            tkinter.messagebox._show("Netflix à la 1900", "Vul uw gegevens in")
        else:
            tkinter.messagebox._show("Netflix à la 1900", "U bent succesvol ingelogd")


    def QRCode_printen(self):
        QR = Toplevel()
        canvas_1 = Canvas(QR, width=400, height=400)
        canvas_1.pack()
        img = Image.open("qrcode.png")
        canvas_image= ImageTk.PhotoImage(img)
        canvas_1.create_image(0,0,image=canvas_image,anchor="nw")

        #code generator moet hier!!

root = Tk()
i = Interface(root)


entry_1 = Entry(root)
entry_2 = Entry(root)
entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)
Button(root, text="Inloggen", command=i.loginButton).grid(row=2,column=1)
root.mainloop()
