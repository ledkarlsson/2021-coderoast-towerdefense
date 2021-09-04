class MyButton:
     def __init__(self, x, y, xTwo, yTwo):
        self.x = x
        self.y = y
        self.xTwo = xTwo
        self.yTwo = yTwo
     
     def checkPress(self, click, x, y):
        if x >=self.x and y >= self.y and x <= self.xTwo and y <= self.yTwo:
             self.pressed()
             return True
        return False

     def pressed(self):
         pass

     def paint(self, canvas):
        canvas.create_rectangle(self.x, self.y, self.xTwo, self.yTwo, fill="red", outline = "black")
