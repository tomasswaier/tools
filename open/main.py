import sys
import tkinter 
from PIL import ImageTk,Image
from tkinter import Label
tk=tkinter.Tk()
def main(img):
  panel=Label(tk,image=img)
  panel.pack(side="bottom",fill="both",expand= True )
  tk.mainloop()


img=ImageTk.PhotoImage(Image.open(sys.argv[1]))
main(img)
