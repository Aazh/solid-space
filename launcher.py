from tkinter import *
import engine
import balltracker

def open_balltracker():
    balltracker.main()

def open_engine():
    engine.main()

def quit():
    root.destroy()


root = Tk()
root.geometry('130x100')

balltracker_button = Button(text = "Balltracker", command = open_balltracker).pack()
engine_button = Button(text = "Engine", command = open_engine).pack()
quit_button = Button(text = "Quit", command = quit).pack()
root.mainloop()