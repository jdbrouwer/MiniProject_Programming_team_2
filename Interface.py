from tkinter import *


class Interface:

    def __init__(self):




    def Help():
        """This function opens a new window with information regarding the helpdesk"""
        win = Toplevel()
        win.geometry("400x400")
        message = "Welkom bij de Helpdesk"
        label1 = Label(win, text=message)
        label1.pack()

    def loginButton():
        """This function activates when the loginbutton is clicked and saves
        the information"""
        naam = entry_1.get()
        mail = entry_2.get()
        print("Naam is: ", naam)
        print("Mail is: ", mail)


root = Tk()
root.wm_title("Netflix à la 1900")
root.geometry("600x400")
taakbalk = Menu(root)
root.config(menu=taakbalk)
subMenu = Menu(taakbalk)
taakbalk.add_cascade(label="About", menu=subMenu)
subMenu.add_command(label="Help", command=Help)

label_naam = Label(root, text="Naam")
label_email = Label(root, text="E-mailadres")
label_naam.grid(row=0, sticky=E)
label_email.grid(row=1, sticky=E)
label_space = Label(root, text="                               ")
label_space.grid(row=4, column=2)


info_text = Label(root, text="Met deze applicatie kunt u zich opgeven voor een film \n bij één van de aanbieders. "
                             "Voer uw naam en \n e-mailadres in en kies een film om te bezoeken \n ")
info_text.grid(row=4, column=0 , rowspan=5, columnspan=5, sticky=W)

entry_1 = Entry(root)
entry_2 = Entry(root)
entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)

button_1 = Button(root, text="Inloggen", command= loginButton)
button_1.grid(row=2, column=1)

canvas = Canvas(root, width=300, height=325)
canvas.grid(row=4, column=3)
dia = canvas.create_rectangle(0,0,350,350, fill="black")
root.mainloop()