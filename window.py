# Imports tkinter
from tkinter import *

window = Tk()  # Initializes the window instance
window.geometry("1920x1080")  # Sets window size
window.title("Tic Tac Toe")   # Sets window title

icon = PhotoImage(file='TicTacToe.png')  # Turns a image into a photo image
window.iconphoto(True, icon)  # Sets window icon

window.mainloop()  # Places window on screen and listens for evernts
