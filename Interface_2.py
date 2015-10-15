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


    def Help(self):
        """This function opens a new window with information regardinng the helpdesk of the application"""
        win = Toplevel()
        win.geometry("200x200")
        Label(win, text="Welkom bij de helpdesk").grid(row=1)

    # def aanbiederInlog(self, name, password):
    #     """This function checks if the supplier is in the database"""
    #     if name == ' ' and password == ' ':
    #         tkinter.messagebox.showinfo("Netflix à la 1900", "U bent succesvol ingelogd!")
    #         film_a = Toplevel()
    #         film_a.geometry("600x400")
    #         Label(film_a, text="Hier komen de films van de aanbieder").grid(row=1)
    #         """Here needs to be a function that checks all the movies of the supplier and puts them in the interface
    #         with all the customers"""
    #     else:
    #         tkinter.messagebox.showinfo("Netflix à la 1900", "Verkeerde inlog gegevens")
    #         self.aanbiederSite()

    def aanbiederSite(self):
        """This function opens a new window with a site for the film suppliers """
        aan = Toplevel()
        aan.geometry("200x100")
        Label(aan, text="Naam").grid(row=0,sticky=E)
        Label(aan, text="Password").grid(row=1,sticky=E)
        global entry_3
        entry_3 = Entry(aan)
        entry_3.grid(row=0, column=1)
        global entry_4
        entry_4 = Entry(aan)
        entry_4.grid(row=1, column=1)
        button1= Button(aan, text="Inloggen", command=self.loginButton_provider)
        button1.grid(row=2,column=1)


    def loginButton_provider(self):
        """This function does the same as loginButton but for a different page"""
        name_s = entry_3
        pass_s = entry_4
        if name_s == '' and pass_s == '':
            tkinter.messagebox.showinfo("Netflix à la 1900", "Verkeerde inlog gegevens")
            self.aanbiederSite()
        else:
            tkinter.messagebox.showinfo("Netflix à la 1900", "U bent succesvol ingelogd!")
            film_a = Toplevel()
            film_a.geometry("600x400")
            Label(film_a, text="Hier komen de films van de aanbieder").grid(row=1)
            """Here needs to be a function that checks all the movies of the supplier and puts them in the interface
            with all the customers"""

    def ticket(self,filmnaam,username,email):
        naam_film = filmnaam[0]
        begintijd = filmnaam[1]
        ticket_code = hoofd_file.codegenerator(username,email,naam_film,begintijd)
        #url = pyqrcode.create(ticket_code)
        #url.gif("qrcode.gif", scale=10)
        qr = pyqrcode.QRCode(ticket_code)
        qr.show()
        img = qr.make_image(block_in_pixels=50, border_in_blocks=0)
        img.save("qr.gif", "GIF")
        #schrijft de ticket informatie naar de database
        hoofd_file.SQL_Write_User(username, email, ticket_code, filmnaam[0], filmnaam[1], filmnaam[3])

        #weergeeft de ticketcode in de UI
        ticketcode_schem = Toplevel()
        ticketcode_schem.geometry("800x800")
        Label(ticketcode_schem,text = "Uw ticketcode is als onderstaande").grid(row=1)
        Label(ticketcode_schem,text = ticket_code).grid(row=2)
        self.QRCode_printen(ticketcode_schem)

    def Movies(self, name, mail):
        """This function takes you to a new window with all available movies"""
        film_window = Toplevel()
        film_window.geometry("300x300")
        label_film = Label(film_window, text="Beschikbare films vandaag")
        label_film.grid(row=1)
        #voor het gemak ff een list
        films_query = hoofd_file.SQL_Select_Film()
        row = 2
        for filmnaam in films_query:
            provider_name = hoofd_file.SQL_Select_Provider(filmnaam[0])
            keuze = filmnaam + tuple(provider_name)
            if len(keuze) > 4:
                c = Button(film_window, text=keuze, command=(lambda filmen=keuze: self.ticket(filmen,name,mail)))
                c.grid(row=row, sticky=W)
                row +=1
            else:
                continue

    def loginButton(self):
        """This function saves the login that is entered in the two entry's"""
        name = entry_1.get()
        mail = entry_2.get()
        if name == "" and mail == "":
            tkinter.messagebox._show("Netflix à la 1900", "Vul uw gegevens in")
        else:
            tkinter.messagebox._show("Netflix à la 1900", "U bent succesvol ingelogd")
            self.Movies(name,mail)

#tijdelijke kladblok

    def QRCode_printen(self,QR):
        canvas_1 = Canvas(QR, width=500, height=500)
        print("A")
        canvas_1.grid(row=3)
        print("B")
       # img = Image.open("qr.gif")
        print("C")
        print("D")
        canvas_1.create_image(0,0,image="qr.gif",anchor="nw")
        print("E")

root = Tk()
i = Interface(root)
p = Interface(root)

entry_1 = Entry(root)
entry_2 = Entry(root)
entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)
entry_3 = Entry(root)
entry_4 = Entry(root)
entry_3.grid(row=0, column=1)
entry_4.grid(row=1, column=1)
Button(root, text="Inloggen", command=i.loginButton).grid(row=2,column=1)
Button(root,text="Site voor aanbieders", command=p.aanbiederSite).grid(row=1,column=2,columnspan=1)
root.mainloop()
