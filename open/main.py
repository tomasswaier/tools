import sys
import tkinter 
from PIL import ImageTk,Image
from tkinter import Label
import webbrowser


#initialize tkinter in case it's an image
tk=tkinter.Tk()
def displayImage(img):

  panel=Label(tk,image=img)
  panel.pack(side="bottom",fill="both",expand= True )
  tk.mainloop()


def main(file):
  #split the input file and match it with correct type
  #I dont belive use of magic library is necesary
  fileType=str(file).split(".")

  
  match fileType[1]:
    case "html":
      webbrowser.open(file,new=2)
    case "jpg"|"png":
      img=ImageTk.PhotoImage(Image.open(file))
      displayImage(img)



main(sys.argv[1])
