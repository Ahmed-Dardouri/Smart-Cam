import tkinter as tk

import os



root = tk.Tk()
def alg1():
   os.system('python algo1.py')
def alg2():
   print("algorithme 2")
def alg3():
   print("algorithme 3")
canvas = tk.Canvas(root,height = 250,width = 500)
canvas.pack()
frame = tk.Frame(root,bg = "#a6c8ff")
frame.place(relwidth = 1,relheight=1)
button1 = tk.Button(frame, text ="algo1", command = alg1)
button1.place(relx = 0.1,rely = 0.1,relwidth = 0.2,relheight = 0.5)
button2 = tk.Button(frame, text ="algo2", command = alg2)
button2.place(relx = 0.4,rely = 0.1,relwidth = 0.2,relheight = 0.5)
button3 = tk.Button(frame, text ="algo3", command = alg3)
button3.place(relx = 0.7,rely = 0.1,relwidth = 0.2,relheight = 0.5)

root.mainloop()