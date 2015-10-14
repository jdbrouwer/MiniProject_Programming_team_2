import pyqrcode
from tkinter import *
from PIL import Image,ImageTk


root = Tk()
root.geometry("600x400")
url = pyqrcode.create("http://google.com")
url.png("QrCode1.png", scale=8)
print(url.terminal(quiet_zone=1))
load = Image.open("QrCode1.png")
render = ImageTk.PhotoImage(load)
img = Label(root,image=render)
img.image = render
img.place(x=0,y=0)

root.mainloop()