from tkinter import *


class Game():
     def __init__(self, title: str, width: int, height: int, timestep: int = 50):
          self.root = Tk()  # saying this window will use tkinter
          self.root.title(title)
          self.running = True  # creating a variable RUN. does nothing yet.hu
          self.root.protocol("WM_DELETE_WINDOW", self.end)
          self.frame = Frame(master=self.root)
          self.frame.grid(row=0, column=0)
          self.timestep = timestep

          # actually creates a window and puts our frame on it
          self.canvas = Canvas(master=self.frame, width=width,
                               height=height, bg="white", highlightthickness=0)
          # makes the window called "canvas" complete
          self.canvas.grid(row=0, column=0, rowspan=2, columnspan=1)

     def run(self):
          if not self.running:  # always going to be true for now
               return
          self.update()  # calls the function 'def update(self):'
          self.paint()  # calls the function 'def paint(self):'

          # does a run of the function every 50/1000 = 1/20 of a second
          self.root.after(self.timestep, self.run)

     def end(self):
        self.root.destroy()  # closes the game window and ends the program
     
     def update(self):
          self.mouse.update()
          self.wavegenerator.update()
          self.displayboard.update()

     def paint(self):
          self.canvas.delete(ALL) #clear the screen
          self.gameMap.paint(self.canvas)
          self.mouse.paint(self.canvas) #draw the mouse dot by going to its 'def paint(canvas):' command
