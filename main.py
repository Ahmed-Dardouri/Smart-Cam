import tkinter as tk
import os
from PIL import Image, ImageTk


root = tk.Tk()
def alg1():
   os.system('python algo1.py')
def alg2():
   print("algorithme 2")
def alg3():
   print("algorithme 3")
root.title("Smart-Cam GUI")
canvas = tk.Canvas(root,height = 400,width = 530)
canvas.pack()

bgimg = Image.open('are.png')
img = ImageTk.PhotoImage(bgimg)
bglabel = tk.Label(root, image = img)
bglabel.place(relwidth = 1,relheight = 1)



frame = tk.Frame(root, bg ="#1d1c18")
frame.place(relx = 0.1, rely = 0.65,relwidth = 0.8,relheight=0.3)
button1 = tk.Button(frame, text ="Face Recognition", command = alg1, bg = "#1d1c18", fg = "#ffd148")
button1.place(relx = 0.025,rely = 0.1,relwidth = 0.3,relheight = 0.5)
button2 = tk.Button(frame, text ="Mask Detection", command = alg2, bg = "#1d1c18", fg = "#ffd148")
button2.place(relx = 0.35,rely = 0.1,relwidth = 0.3,relheight = 0.5)
button3 = tk.Button(frame, text ="Door State", command = alg3 , bg = "#1d1c18", fg = "#ffd148")
button3.place(relx = 0.675,rely = 0.1,relwidth = 0.3,relheight = 0.5)

root.mainloop()