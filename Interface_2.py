from tkinter import *
import tkinter.messagebox


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
            films = ["q", "e", "r"]
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