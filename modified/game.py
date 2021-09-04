import tkinter as tk
from typing import Optional


class Game():
     def __init__(self, title: str, width: int, height: int, timestep: int = 50):
          self.root = tk.Tk()  # saying this window will use tkinter
          self.root.title(title)
          self.running = True  # creating a variable RUN. does nothing yet.hu
          self.root.protocol("WM_DELETE_WINDOW", self.end)
          self.frame = tk.Frame(master=self.root)
          self.frame.grid(row=0, column=0)
          self.timestep = timestep
          self.running = False
          self.timer_id: Optional[str] = None

          # actually creates a window and puts our frame on it
          self.canvas = tk.Canvas(master=self.frame, width=width,
                               height=height, bg="white", highlightthickness=0)
          # makes the window called "canvas" complete
          self.canvas.grid(row=0, column=0, rowspan=2, columnspan=1)

     def run(self):
          self.running = True
          self._run()
          self.root.mainloop() #starts running the tkinter graphics loop          

     def _run(self):
          self.update()
          self.paint()
          if self.running:
               self.timer_id = self.root.after(self.timestep, self._run) # does a run of the function every timestep/1000 of a second

     def end(self):
          self.running = False
          if self.timer_id is not None:
               self.root.after_cancel(self.timer_id)
          self.root.destroy()  # closes the game window and ends the program
     
     def update(self):
          self.mouse.update()
          self.wavegenerator.update()
          self.displayboard.update()

     def paint(self):
          self.canvas.delete(tk.ALL) #clear the screen
          self.gameMap.paint(self.canvas)
          self.mouse.paint(self.canvas) #draw the mouse dot by going to its 'def paint(canvas):' command
