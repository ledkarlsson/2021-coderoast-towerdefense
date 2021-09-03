from tkinter import *

class Game():
     def __init__(self, mapSize: int):
          self.root=Tk() #saying this window will use tkinter
          self.root.title("Tower Defense Ultra Mode")
          self.running=True #creating a variable RUN. does nothing yet.hu
          self.root.protocol("WM_DELETE_WINDOW", self.end)
          self.frame = Frame(master= self.root)
          self.frame.grid(row = 0, column = 0)

          self.canvas = Canvas(master = self.frame, width=mapSize, height=mapSize, bg = "white", highlightthickness = 0) #actually creates a window and puts our frame on it
          self.canvas.grid(row = 0,column = 0,rowspan = 2, columnspan = 1) #makes the window called "canvas" complete
          
     def run(self):
          if not self.running: #always going to be true for now
               return
          self.update() #calls the function 'def update(self):'
          self.paint() #calls the function 'def paint(self):'
          
          self.root.after(50, self.run) #does a run of the function every 50/1000 = 1/20 of a second

     def end(self):
        self.root.destroy() #closes the game window and ends the program
