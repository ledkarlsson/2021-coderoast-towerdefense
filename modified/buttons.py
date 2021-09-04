from myButton import MyButton

class StickyButton(MyButton):

    def pressed(self,displayTower):
         if displayTower.stickyTarget == False:
             displayTower.stickyTarget = True
         else:
             displayTower.stickyTarget = False

class SellButton(MyButton):
             
    def pressed(self,displayTower):
         displayTower.sold()
         displayTower = None

class UpgradeButton(MyButton):
             
    def pressed(self,money,displayTower):
         if money >= displayTower.upgradeCost:
              money -= displayTower.upgradeCost
              displayTower.upgrade()

class TargetButton(MyButton):
    def __init__(self, x, y, xTwo, yTwo, myType):
        super().__init__( x, y, xTwo, yTwo)
        self.type = myType
     
class NextWaveButton:
     def __init__(self,game):
          self.game = game
          self.x = 450
          self.y = 25
          self.xTwo = 550
          self.yTwo = 50
          self.canPress = True

     def is_within_bounds(self, x: int, y: int):
          return self.x <= x <= self.xTwo and self.y <= y <= self.yTwo

     def checkPress(self, click, x, y,monsters):
          if not self.is_within_bounds(x=x, y=y):
               return
          if self.canPress and click and len(monsters) == 0:
               self.game.wavegenerator.getWave()

     def paint(self, canvas,monsters):
          if self.canPress and len(monsters) == 0:
               self.color = "blue"
          else:
               self.color = "red"
          canvas.create_rectangle(self.x, self.y, self.xTwo, self.yTwo, fill=self.color, outline = self.color) #draws a rectangle where the pointer is
          canvas.create_text(500,37,text = "Next Wave")


