from tkinter import *
from PIL import Image
from PIL import ImageTk
import random
import math
from game import Game, GameObject
from myButton import MyButton
from buttons import *
import gameGlobal

def returning_tower(string: str):
     if string == 'ArrowShooterTower':
          return ArrowShooterTower
     elif string == 'BulletShooterTower':
          return BulletShooterTower
     elif string == 'TackTower':
          return TackTower
     elif string == 'PowerTower':
          return PowerTower
     else:
          print("error in towers")

def returning_monster(string: str):
     if string == 'Monster1':
          return Monster1
     elif string == 'Monster2':
          return Monster2
     elif string == 'AlexMonster':
          return AlexMonster
     elif string == 'BenMonster':
          return BenMonster
     elif string == 'LeoMonster':
          return LeoMonster
     elif string == 'MonsterBig':
          return MonsterBig
     else:
          print("error in gameGlobal.monsters")     

def returning_block(string: int):
     if string == 'NormalBlock':
          return NormalBlock
     elif string == 'PathBlock':
          return PathBlock
     elif string == 'WaterBlock':
          return WaterBlock
     else:
          print("error in blocks")
class GameState:
     def __init__(self, money):
         self.money = gameGlobal.money
class TowerDefenseGame(Game):
     def __init__(self): #setting up the window for the game here
          super().__init__(title="Tower Defense Ultra Mode", width=gameGlobal.mapSize, height=gameGlobal.mapSize, timestep=10)

          self.displayboard = Displayboard(self)
          self.infoboard = Infoboard(self)
          self.towerbox = Towerbox(self)
          self.mouse = Mouse(self)
          self.gameMap = Map()
          self.wavegenerator = Wavegenerator(self)

          self.add_object(self.mouse)
          self.add_object(self.displayboard)
          self.add_object(self.wavegenerator)

          self.gameState = GameState(gameGlobal.money)
          self.run() 

     def update(self):
         super().update()
         for i in range(len(gameGlobal.projectiles)):
             try:
                 gameGlobal.projectiles[i].update()
             except:
                 pass
         for y in range(gameGlobal.gridSize):
             for x in range(gameGlobal.gridSize):
                 gameGlobal.blockGrid[x][y].update() #updates each block one by one by going to its 'def update():' command
         for i in range(len(gameGlobal.monsters)):
             try:
                 gameGlobal.monsters[i].update()
             except:
                 pass
               
         global monstersByHealth
         global monstersByHealthReversed
         global monstersByDistance
         global monstersByDistanceReversed
         global monstersListList
         monstersByHealth = sorted(gameGlobal.monsters, key=lambda x: x.health, reverse=True)
         monstersByDistance = sorted(gameGlobal.monsters, key=lambda x: x.distanceTravelled, reverse=True)
         monstersByHealthReversed = sorted(gameGlobal.monsters, key=lambda x: x.health, reverse=False)
         monstersByDistanceReversed = sorted(gameGlobal.monsters, key=lambda x: x.distanceTravelled, reverse=False)
         monstersListList = [monstersByHealth,monstersByHealthReversed,monstersByDistance,monstersByDistanceReversed]
         
         for y in range(gameGlobal.gridSize):
             for x in range(gameGlobal.gridSize):
                 if gameGlobal.towerGrid[x][y]:
                    gameGlobal.towerGrid[x][y].update() #updates each tower one by one by going to its 'def update():' command             
          
     def paint(self):
          super().paint()
          for y in range(gameGlobal.gridSize):
              for x in range(gameGlobal.gridSize):
                   if gameGlobal.towerGrid[x][y]:
                        gameGlobal.towerGrid[x][y].paint(self.canvas)
          for i in range(len(monstersByDistanceReversed)):
               monstersByDistanceReversed[i].paint(self.canvas)
          for i in range(len(gameGlobal.projectiles)):
              gameGlobal.projectiles[i].paint(self.canvas)
          if gameGlobal.displayTower:
               displayTower.paintSelect(self.canvas)
          self.displayboard.paint()

class Map:
    def __init__(self):
        self.image = None
        self.loadMap("LeoMap")
    def loadMap(self,mapName):
        self.drawnMap = Image.new("RGBA", (gameGlobal.mapSize, gameGlobal.mapSize), (255,255,255,255))
        self.mapFile = open("texts/mapTexts/"+mapName+".txt","r")
        self.gridValues = list(map(int, (self.mapFile.read()).split()))
        for y in range(gameGlobal.gridSize):
              for x in range(gameGlobal.gridSize):
                   self.blockNumber = self.gridValues[gameGlobal.gridSize*y + x]

                   self.blockType = returning_block(gameGlobal.blockDictionary[self.blockNumber])

                   gameGlobal.blockGrid[x][y] = self.blockType(x*gameGlobal.blockSize+gameGlobal.blockSize/2,y*gameGlobal.blockSize+gameGlobal.blockSize/2,self.blockNumber,x,y) #creates a grid of Blocks
                   gameGlobal.blockGrid[x][y].paint(self.drawnMap)
        self.drawnMap.save("images/mapImages/"+mapName+".png")
        self.image = Image.open("images/mapImages/"+mapName+".png")
        self.image = ImageTk.PhotoImage(self.image)
          
    def saveMap(self):
        self.mapFile = open("firstMap.txt","w")
        for y in range(gameGlobal.gridSize):
              for x in range(gameGlobal.gridSize):
                  self.mapFile.write(gameGlobal.blockGrid[x][y].blockType + " ")
        self.mapFile.close()

    def paint(self, canvas):
         canvas.create_image(0,0, image = self.image, anchor = NW)


class Wavegenerator(GameObject):
     def __init__(self,game):
          self.game = game
          self.done = False
          self.currentWave = []
          self.currentMonster = 0
          self.direction = None
          self.gridx = 0
          self.gridy = 0
          self.findSpawn()
          self.decideMove()
          self.ticks = 1
          self.maxTicks = 2
          self.waveFile = open("texts/waveTexts/WaveGenerator2.txt","r")

     def getWave(self):
          self.game.displayboard.nextWaveButton.canPress = False
          self.currentMonster = 1
          self.waveLine = self.waveFile.readline()
          if len(self.waveLine) == 0:
               self.done = True
          else:
               self.currentWave = self.waveLine.split()
               self.currentWave = list(map(int, self.currentWave))
               self.maxTicks = self.currentWave[0]

     def findSpawn(self):
          global spawnx
          global spawny
          for x in range(gameGlobal.gridSize):
               if isinstance(gameGlobal.blockGrid[x][0], PathBlock):
                    self.gridx = x
                    spawnx = x*gameGlobal.blockSize + gameGlobal.blockSize/2
                    spawny = 0
                    return
          for y in range(gameGlobal.gridSize):
               if isinstance(gameGlobal.blockGrid[0][y], PathBlock):
                    self.gridy = y
                    spawnx = 0
                    spawny = y*gameGlobal.blockSize + gameGlobal.blockSize/2
                    return
          
     def move(self):
        gameGlobal.pathList.append(self.direction)
        if self.direction == 1:
               self.gridx += 1
        if self.direction == 2:
               self.gridx -= 1
        if self.direction == 3:
               self.gridy +=1
        if self.direction == 4:
               self.gridy -=1
        self.decideMove()

     def decideMove(self):
         if self.direction != 2 and self.gridx < gameGlobal.gridSize-1 and self.gridy >= 0 and self.gridy <= gameGlobal.gridSize-1:
            if isinstance(gameGlobal.blockGrid[self.gridx+1][self.gridy], PathBlock):
                self.direction = 1
                self.move()
                return
            
         if self.direction != 1 and self.gridx > 0 and self.gridy >= 0 and self.gridy <= gameGlobal.gridSize-1:
            if isinstance(gameGlobal.blockGrid[self.gridx-1][self.gridy], PathBlock):
                self.direction = 2
                self.move()
                return

         if self.direction != 4 and self.gridy < gameGlobal.gridSize-1 and self.gridx >= 0 and self.gridx <= gameGlobal.gridSize-1:
            if isinstance(gameGlobal.blockGrid[self.gridx][self.gridy+1], PathBlock):
                self.direction = 3
                self.move()
                return
                        
         if self.direction != 3 and self.gridy > 0 and self.gridx >= 0 and self.gridx <= gameGlobal.gridSize-1:
            if isinstance(gameGlobal.blockGrid[self.gridx][self.gridy-1], PathBlock):
                self.direction = 4
                self.move()
                return

         gameGlobal.pathList.append(5)

     def spawnMonster(self):
          self.monsterType = returning_monster(gameGlobal.monsterDictionary[self.currentWave[self.currentMonster]])
          
          gameGlobal.monsters.append(self.monsterType(0))
          self.currentMonster = self.currentMonster + 1

     def update(self):
          if self.done:
               return

          if self.currentMonster == len(self.currentWave):
               self.game.displayboard.nextWaveButton.canPress = True
          else:
               self.ticks = self.ticks+1
               if self.ticks == self.maxTicks:
                    self.ticks = 0
                    self.spawnMonster()


class Infoboard:
     def __init__(self, game):
          self.canvas = Canvas(master = game.frame, width = 162, height = 174, bg = "gray", highlightthickness = 0)
          self.canvas.grid(row = 0, column = 1)
          self.image = ImageTk.PhotoImage(Image.open("images/infoBoard.png"))
          self.canvas.create_image(0,0 , image = self.image, anchor = NW)
          self.currentButtons = []
     
     def buttonsCheck(self, click, x, y):
          if click:
               for i in range(len(self.currentButtons)):
                     if self.currentButtons[i].checkPress(click, x, y):
                          self.displaySpecific()
                          return
                     
     def displaySpecific(self):
          self.canvas.delete(ALL) #clear the screen
          self.canvas.create_image(0,0, image = self.image, anchor = NW)
          self.currentButtons = []
          if displayTower== None:
               return
          
          self.towerImage = ImageTk.PhotoImage(Image.open("images/towerImages/"+displayTower.__class__.__name__+"/"+str(displayTower.level)+ ".png"))
          self.canvas.create_text(80,75,text = displayTower.name, font = ("times",20))
          self.canvas.create_image(5,5 , image = self.towerImage, anchor = NW)
          
          if issubclass(displayTower.__class__, TargetingTower):
               
              self.currentButtons.append(TargetButton(26,30,35,39,0))
              self.canvas.create_text(37,28,text = "> Health", font = ("times",12), fill = "white", anchor = NW)
                                    
              self.currentButtons.append(TargetButton(26,50,35,59,1))
              self.canvas.create_text(37,48,text = "< Health", font = ("times",12), fill = "white", anchor = NW)
                                                                       
              self.currentButtons.append(TargetButton(92,50,101,59,2))
              self.canvas.create_text(103,48,text = "> Distance", font = ("times",12), fill = "white", anchor = NW)

              self.currentButtons.append(TargetButton(92,30,101,39,3))
              self.canvas.create_text(103,28,text = "< Distance", font = ("times",12), fill = "white", anchor = NW)
 


              self.currentButtons.append(StickyButton(10,40,19,49))
              self.currentButtons.append(SellButton(5,145,78,168))
              if displayTower.upgradeCost:
                   self.currentButtons.append(UpgradeButton(82,145,155,168))
                   self.canvas.create_text(120,157,text = "Upgrade: "+ str(displayTower.upgradeCost), font = ("times",12), fill = "light green", anchor = CENTER)

              self.canvas.create_text(28,146,text = "Sell", font = ("times",22), fill = "light green", anchor = NW)
              
              self.currentButtons[displayTower.targetList].paint(self.canvas)
              if displayTower.stickyTarget == True:
                   self.currentButtons[4].paint(self.canvas)

     def displayGeneric(self):
          self.currentButtons = []
          if gameGlobal.selectedTower == "<None>":
               self.text = None
               self.towerImage = None
          else:
               self.text = gameGlobal.selectedTower + " cost: " + str(gameGlobal.towerCost[gameGlobal.selectedTower])
               self.towerImage = ImageTk.PhotoImage(Image.open("images/towerImages/"+gameGlobal.towerDictionary[gameGlobal.selectedTower]+"/1.png"))
          self.canvas.delete(ALL) #clear the screen
          self.canvas.create_image(0,0, image = self.image, anchor = NW)
          self.canvas.create_text(80,75,text = self.text)
          self.canvas.create_image(5,5 , image = self.towerImage, anchor = NW)
          
class Displayboard:
    def __init__(self, game):
          self.canvas = Canvas(master = game.frame, width = 600, height = 80, bg = "gray", highlightthickness = 0)
          self.canvas.grid(row = 2, column = 0)
          self.healthbar = Healthbar()
          self.moneybar = Moneybar()
          self.nextWaveButton = NextWaveButton(game)
          self.paint()
    def update(self):
        self.healthbar.update()
        self.moneybar.update()
    
    def paint(self):         
          self.canvas.delete(ALL) #clear the screen
          self.healthbar.paint(self.canvas)
          self.moneybar.paint(self.canvas)
          self.nextWaveButton.paint(self.canvas,gameGlobal.monsters)
               

class Towerbox:
     def __init__(self, game):
          self.game = game
          self.box = Listbox(master =game.frame, selectmode = "SINGLE", font = ("times",18), height = 18, width = 13, bg = "gray", fg = "dark blue", bd = 1, highlightthickness = 0)
          self.box.insert(END, "<None>")
          for i in gameGlobal.towerDictionary:
               self.box.insert(END, i)
          for i in range(50):
               self.box.insert(END, "<None>")
          self.box.grid(row = 1, column = 1, rowspan = 2)
          self.box.bind("<<ListboxSelect>>", self.onselect)
     def onselect(self,event):
          global displayTower
          gameGlobal.selectedTower = str(self.box.get(self.box.curselection()))
          displayTower = None
          self.game.infoboard.displayGeneric()
class Mouse(GameObject):
     def __init__(self,game): #when i define a "Mouse", this is what happens
          self.game = game
          self.x = 0
          self.y = 0
          self.gridx = 0
          self.gridy = 0
          self.xoffset = 0
          self.yoffset = 0
          self.pressed = False
          game.root.bind("<Button-1>", self.clicked) #whenever left mouse button is pressed, go to def released(event)
          game.root.bind("<ButtonRelease-1>", self.released) #whenever left mouse button is released, go to def released(event)
          game.root.bind("<Motion>", self.motion) #whenever left mouse button is dragged, go to def released(event)
          self.image = Image.open("images/mouseImages/HoveringCanPress.png")
          self.image = ImageTk.PhotoImage(self.image) 
          self.canNotPressImage = Image.open("images/mouseImages/HoveringCanNotPress.png")
          self.canNotPressImage = ImageTk.PhotoImage(self.canNotPressImage) 
          
     def clicked(self, event):
        self.pressed = True #sets a variable
        self.image = Image.open("images/mouseImages/Pressed.png")
        self.image = ImageTk.PhotoImage(self.image) 
        
     def released(self, event):
        self.pressed = False
        self.image = Image.open("images/mouseImages/HoveringCanPress.png")
        self.image = ImageTk.PhotoImage(self.image) 

     def motion(self, event):
          if event.widget == self.game.canvas:
               self.xoffset = 0
               self.yoffset = 0
          elif event.widget == self.game.infoboard.canvas:
               self.xoffset = gameGlobal.mapSize
               self.yoffset = 0
          elif event.widget == self.game.towerbox.box:
               self.xoffset = gameGlobal.mapSize
               self.yoffset = 174
          elif event.widget == self.game.displayboard.canvas:
               self.yoffset = gameGlobal.mapSize
               self.xoffset = 0
          self.x = event.x +self.xoffset#sets the "Mouse" x to the real mouse's x
          self.y = event.y +self.yoffset#sets the "Mouse" y to the real mouse's y
          if self.x < 0: self.x = 0
          if self.y < 0: self.y = 0
          self.gridx = int((self.x-(self.x%gameGlobal.blockSize))/gameGlobal.blockSize)
          self.gridy = int((self.y-(self.y%gameGlobal.blockSize))/gameGlobal.blockSize)

     def update(self):
          if self.gridx >= 0 and self.gridx <= gameGlobal.gridSize-1 and self.gridy >= 0 and self.gridy <= gameGlobal.gridSize-1:
               gameGlobal.blockGrid[self.gridx][self.gridy].hoveredOver(self.pressed, self.game)
          else:
               self.game.displayboard.nextWaveButton.checkPress(self.pressed, self.x-self.xoffset, self.y-self.yoffset,gameGlobal.monsters)
               self.game.infoboard.buttonsCheck(self.pressed, self.x-self.xoffset, self.y-self.yoffset)
     def paint(self, canvas):
          if self.gridx >= 0 and self.gridx <= gameGlobal.gridSize-1 and self.gridy >= 0 and self.gridy <= gameGlobal.gridSize-1:
               if gameGlobal.blockGrid[self.gridx][self.gridy].canPlace:
                    canvas.create_image(self.gridx*gameGlobal.blockSize,self.gridy*gameGlobal.blockSize, image = self.image, anchor = NW)
               else:
                    canvas.create_image(self.gridx*gameGlobal.blockSize,self.gridy*gameGlobal.blockSize, image = self.canNotPressImage, anchor = NW)
     
               
class Healthbar:
     def __init__(self):
          self.text = str(gameGlobal.health)
     
     def update(self):
        self.text = str(gameGlobal.health)
     
     def paint(self, canvas):
          canvas.create_text(40, 40, text="Health: " + self.text,fill="black")
     

class Moneybar:
     def __init__(self):
          self.text = str(gameGlobal.money)
     
     def update(self):
        self.text = str(gameGlobal.money)
     
     def paint(self, canvas):
          canvas.create_text(240, 40, text="Money: " + self.text,fill="black")

class Projectile:
     def __init__(self,x,y,damage,speed):
        self.hit = False
        self.x = x
        self.y = y
        self.speed = gameGlobal.blockSize/2
        self.damage = damage
        self.speed = speed
        #self.image = Image.open("images/projectileImages/"+self.__class__.__name__+ ".png")
        #self.image = ImageTk.PhotoImage(self.image) 

     def update(self):
          try:
             if target.alive == False:
                  gameGlobal.projectiles.remove(self)
                  return
          except:
               if self.hit:
                  self.gotMonster()
               self.move()
               self.checkHit()

     def gotMonster(self):
        self.target.health -= self.damage
        gameGlobal.projectiles.remove(self)
        
     def paint(self,canvas):
         canvas.create_image(self.x,self.y,image = self.image)
     

class TrackingBullet(Projectile):
    def __init__(self,x,y,damage,speed,target):
          super().__init__(x,y, damage,speed)
          self.target = target
          self.image = Image.open("images/projectileImages/bullet.png")
          self.image = ImageTk.PhotoImage(self.image) 
        
    def move(self):
        self.length = ((self.x-(self.target.x))**2 + (self.y-(self.target.y))**2)**0.5
        self.x += self.speed*((self.target.x)-self.x)/self.length
        self.y += self.speed*((self.target.y)-self.y)/self.length
        
    def checkHit(self):
        if self.speed**2 > (self.x-(self.target.x))**2 + (self.y-(self.target.y))**2:
            self.hit = True

class PowerShot(TrackingBullet):
    def __init__(self,x,y,damage,speed,target,slow):
         super().__init__(x,y, damage,speed,target)
         self.slow = slow
         self.image = Image.open("images/projectileImages/powerShot.png")
         self.image = ImageTk.PhotoImage(self.image)

    def gotMonster(self):
        self.target.health -= self.damage
        if self.target.movement > (self.target.speed)/self.slow:
             self.target.movement = (self.target.speed)/self.slow
        gameGlobal.projectiles.remove(self) 
        
class AngledProjectile(Projectile):
     def __init__(self,x,y,damage,speed,angle,givenRange):
          super().__init__(x,y,damage,speed)
          self.xChange = speed*math.cos(angle)
          self.yChange = speed*math.sin(-angle)
          self.range = givenRange
          self.image = Image.open("images/projectileImages/arrow.png")
          self.image = ImageTk.PhotoImage(self.image.rotate(math.degrees(angle)))
          self.target = None
          self.speed = speed
          self.distance = 0

     def checkHit(self):
          for i in range(len(gameGlobal.monsters)):
               if (gameGlobal.monsters[i].x-self.x)**2+(gameGlobal.monsters[i].y-self.y)**2 <= (gameGlobal.blockSize)**2:
                    self.hit = True
                    self.target = gameGlobal.monsters[i]
                    return
               
     def gotMonster(self):
        self.target.health -= self.damage
        self.target.tick = 0
        self.target.maxTick = 5
        gameGlobal.projectiles.remove(self)

     def move(self):
          self.x += self.xChange
          self.y += self.yChange
          self.distance += self.speed
          if self.distance >= self.range:
               gameGlobal.projectiles.remove(self)
          
         
class Tower:
     def __init__(self,x,y,gridx,gridy):
          self.upgradeCost = None
          self.level = 1
          self.range = 0
          self.clicked = False
          self.x = x
          self.y = y
          self.gridx = gridx
          self.gridy = gridy
          self.image = Image.open("images/towerImages/"+self.__class__.__name__+"/1.png")
          self.image = ImageTk.PhotoImage(self.image) 

     def update(self):
          pass

     def upgrade(self):
          self.level = self.level+1
          self.image = Image.open("images/towerImages/"+self.__class__.__name__+"/"+str(self.level)+".png")
          self.image = ImageTk.PhotoImage(self.image)
          self.nextLevel()

     def sold(self):
          gameGlobal.towerGrid[self.gridx][self.gridy] = None

     def paintSelect(self,canvas):
          canvas.create_oval(self.x-self.range,self.y-self.range,self.x + self.range,self.y + self.range,fill=None, outline = "white")
 
     def paint(self, canvas):
          canvas.create_image(self.x,self.y, image = self.image, anchor = CENTER)

class ShootingTower(Tower):
     def __init__(self,x,y,gridx,gridy):
        super().__init__(x,y,gridx,gridy)
        self.bulletsPerSecond = None
        self.ticks = 0
        self.damage = 0
        self.speed = None

     def update(self):
          self.prepareShot()
              
class TargetingTower(ShootingTower):
    def __init__(self,x,y,gridx,gridy):
        super().__init__(x,y,gridx,gridy)
        self.target = None
        self.targetList = 0
        self.stickyTarget = False
    
    def prepareShot(self):
          self.checkList = monstersListList[self.targetList]
          if self.ticks != 20/self.bulletsPerSecond:
               self.ticks += 1
          if self.stickyTarget == False:
               for i in range(len(self.checkList)):
                  if (self.range+gameGlobal.blockSize/2)**2 >= (self.x-self.checkList[i].x)**2 + (self.y-self.checkList[i].y)**2:
                      self.target = self.checkList[i]
          if self.target:
              if self.target.alive and (self.range +gameGlobal.blockSize/2) >= ((self.x-self.target.x)**2 + (self.y-self.target.y)**2)**0.5:
                  if self.ticks >= 20/self.bulletsPerSecond:
                      self.shoot()
                      self.ticks = 0
              else:
                  self.target = None
          elif self.stickyTarget == True:
              for i in range(len(self.checkList)):
                  if (self.range+gameGlobal.blockSize/2)**2 >= (self.x-self.checkList[i].x)**2 + (self.y-self.checkList[i].y)**2:
                      self.target = self.checkList[i]
        

class ArrowShooterTower(TargetingTower):
     def __init__(self,x,y,gridx,gridy):
          super().__init__(x,y,gridx,gridy)
          self.name = "Arrow Shooter"
          self.infotext = "ArrowShooterTower at [" + str(gridx) + "," + str(gridy) + "]."
          self.range = gameGlobal.blockSize*10
          self.bulletsPerSecond = 1
          self.damage = 10
          self.speed = gameGlobal.blockSize
          self.upgradeCost = 50

     def nextLevel(self):
          if self.level == 2:
               self.upgradeCost = 100
               self.range = gameGlobal.blockSize*11
               self.damage = 12
          elif self.level == 3:
               self.upgradeCost = None
               self.bulletsPerSecond = 2
          
     def shoot(self):
        self.angle = math.atan2(self.y- self.target.y,self.target.x-self.x)
        gameGlobal.projectiles.append(AngledProjectile(self.x , self.y, self.damage, self.speed, self.angle,self.range+gameGlobal.blockSize/2))
          
class BulletShooterTower(TargetingTower):
     def __init__(self,x,y,gridx,gridy):
          super().__init__(x,y,gridx,gridy)
          self.name = "Bullet Shooter"
          self.infotext = "BulletShooterTower at [" + str(gridx) + "," + str(gridy) + "]."
          self.range = gameGlobal.blockSize*6
          self.bulletsPerSecond = 4
          self.damage = 5
          self.speed = gameGlobal.blockSize/2

     def shoot(self):
          gameGlobal.projectiles.append(TrackingBullet(self.x , self.y, self.damage, self.speed, self.target))

class PowerTower(TargetingTower):
     def __init__(self,x,y,gridx,gridy):
          super(PowerTower,self).__init__(x,y,gridx,gridy)
          self.name = "Power Tower"
          self.infotext = "PowerTower at [" + str(gridx) + "," + str(gridy) + "]."
          self.range = gameGlobal.blockSize*8
          self.bulletsPerSecond = 10
          self.damage = 1
          self.speed = gameGlobal.blockSize
          self.slow = 3

     def shoot(self):
          gameGlobal.projectiles.append(PowerShot(self.x , self.y, self.damage, self.speed, self.target,self.slow))
 
class TackTower(TargetingTower):
     def __init__(self,x,y,gridx,gridy):
          super().__init__(x,y,gridx,gridy)
          self.name = "Tack Tower"
          self.infotext = "TackTower at [" + str(gridx) + "," + str(gridy) + "]."
          self.range = gameGlobal.blockSize*5
          self.bulletsPerSecond = 1
          self.damage = 10
          self.speed = gameGlobal.blockSize
          
     def shoot(self):
          for i in range(8):
             self.angle = math.radians(i*45)
             gameGlobal.projectiles.append(AngledProjectile(self.x , self.y, self.damage, self.speed, self.angle,self.range))
 
     
class Monster:
     def __init__(self,distance):
          self.alive = True
          self.image = None
          self.health = 0
          self.maxHealth = 0
          self.speed = 0.0
          self.movement = 0.0
          self.tick = 0
          self.maxTick = 1
          self.distanceTravelled = distance
          if self.distanceTravelled <=0:
               self.distanceTravelled = 0
          self.x,self.y = self.positionFormula(self.distanceTravelled)
          self.armor = 0
          self.magicresist = 0
          self.value = 0
          self.image = Image.open("images/monsterImages/"+self.__class__.__name__+ ".png")
          self.image = ImageTk.PhotoImage(self.image) 

     def update(self):
          if self.health <= 0:
               gameGlobal.money += self.value
               self.killed()
          self.move()

     def move(self):
          if self.tick >= self.maxTick:
               self.distanceTravelled += self.movement
               self.x,self.y = self.positionFormula(self.distanceTravelled)

               self.movement = self.speed
               self.tick = 0
               self.maxTick = 1
          self.tick+=1

     def positionFormula(self,distance):
         self.xPos = spawnx
         self.yPos = spawny + gameGlobal.blockSize/2
         self.blocks = int((distance-(distance%gameGlobal.blockSize))/gameGlobal.blockSize)
         if self.blocks != 0:
              for i in range(self.blocks):
                  if gameGlobal.pathList[i] == 1:
                      self.xPos += gameGlobal.blockSize
                  elif gameGlobal.pathList[i] == 2:
                      self.xPos -= gameGlobal.blockSize
                  elif gameGlobal.pathList[i] == 3:
                      self.yPos += gameGlobal.blockSize
                  else:
                      self.yPos -= gameGlobal.blockSize
         if distance%gameGlobal.blockSize != 0:
             if gameGlobal.pathList[self.blocks] == 1:
                 self.xPos += (distance%gameGlobal.blockSize)
             elif gameGlobal.pathList[self.blocks] == 2:
                 self.xPos -= (distance%gameGlobal.blockSize)
             elif gameGlobal.pathList[self.blocks] == 3:
                 self.yPos += (distance%gameGlobal.blockSize)
             else:
                 self.yPos -= (distance%gameGlobal.blockSize)
         if gameGlobal.pathList[self.blocks] == 5:
              self.gotThrough()
         return self.xPos,self.yPos

     def killed(self):
          self.die()

     def gotThrough(self):
          gameGlobal.health -= 1
          self.die()
              
     def die(self):
          self.alive = False
          gameGlobal.monsters.remove(self)

     def paint(self,canvas):
          canvas.create_rectangle(self.x-self.axis, self.y-3*self.axis/2, self.x+self.axis-1, self.y-self.axis-1, fill="red", outline = "black") 
          canvas.create_rectangle(self.x-self.axis+1, self.y-3*self.axis/2 +1, self.x-self.axis+(self.axis*2-2)*self.health/self.maxHealth, self.y-self.axis-2, fill="green", outline = "green")
          canvas.create_image(self.x,self.y, image = self.image, anchor = CENTER)
 


class Monster1(Monster):
     def __init__(self,distance):
          super().__init__(distance)
          self.maxHealth = 30
          self.health = self.maxHealth
          self.value = 5
          self.speed = float(gameGlobal.blockSize)/2
          self.movement = gameGlobal.blockSize/3
          self.axis = gameGlobal.blockSize/2
          
class Monster2(Monster):
     def __init__(self,distance):
          super().__init__(distance)
          self.maxHealth = 50
          self.health = self.maxHealth
          self.value = 10
          self.speed = float(gameGlobal.blockSize)/4
          self.movement = float(gameGlobal.blockSize)/4
          self.axis = gameGlobal.blockSize/2

     def killed(self):
          gameGlobal.monsters.append(Monster1(self.distanceTravelled + gameGlobal.blockSize*(.5-random.random())))
          self.die()

class AlexMonster(Monster):
     def __init__(self,distance):
          super().__init__(distance)
          self.maxHealth = 500
          self.health = self.maxHealth
          self.value = 100
          self.speed = float(gameGlobal.blockSize)/5
          self.movement = float(gameGlobal.blockSize)/5
          self.axis = gameGlobal.blockSize

     def killed(self):
          for i in range(5):
               gameGlobal.monsters.append(Monster2(self.distanceTravelled + gameGlobal.blockSize*(.5-random.random())))
          self.die()

class BenMonster(Monster):
     def __init__(self,distance):
          super().__init__(distance)
          self.maxHealth = 200
          self.health = self.maxHealth
          self.value = 30
          self.speed = float(gameGlobal.blockSize)/4
          self.movement = float(gameGlobal.blockSize)/4
          self.axis = gameGlobal.blockSize/2

     def killed(self):
          for i in range(2):
               gameGlobal.monsters.append(LeoMonster(self.distanceTravelled + gameGlobal.blockSize*(.5-random.random())))
          self.die()

class LeoMonster(Monster):
     def __init__(self,distance):
          super().__init__(distance)
          self.maxHealth = 20
          self.health = self.maxHealth
          self.value = 2
          self.speed = float(gameGlobal.blockSize)/2
          self.movement = float(gameGlobal.blockSize)/2
          self.axis = gameGlobal.blockSize/4
          
class MonsterBig(Monster):
     def __init__(self,distance):
          super().__init__(distance)
          self.maxHealth = 1000
          self.health = self.maxHealth
          self.value = 10
          self.speed = float(gameGlobal.blockSize)/6
          self.movement = float(gameGlobal.blockSize)/6
          self.axis = 3*gameGlobal.blockSize/2

class Block:
     def __init__(self, x, y, blockNumber,gridx,gridy): #when i define a "Block", this is what happens
          self.x = x #sets Block x to the given 'x'
          self.y = y #sets Block y to the given 'y'
          self.canPlace = True
          self.blockNumber = blockNumber
          self.gridx = gridx
          self.gridy = gridy
          self.image = None
          self.axis = gameGlobal.blockSize/2

     def hoveredOver(self,click,game):
          if click == True:
               if gameGlobal.towerGrid[self.gridx][self.gridy]:
                    if gameGlobal.selectedTower == "<None>":
                        gameGlobal.towerGrid[self.gridx][self.gridy].clicked = True
                        global displayTower
                        displayTower = gameGlobal.towerGrid[self.gridx][self.gridy]
                        game.infoboard.displaySpecific()
               elif gameGlobal.selectedTower != "<None>" and self.canPlace == True and gameGlobal.money >= gameGlobal.towerCost[gameGlobal.selectedTower]:
                    self.towerType = returning_tower(gameGlobal.towerDictionary[gameGlobal.selectedTower])
                    gameGlobal.towerGrid[self.gridx][self.gridy] = self.towerType(self.x,self.y,self.gridx,self.gridy)
                    gameGlobal.money -= gameGlobal.towerCost[gameGlobal.selectedTower]
                    

     def update(self):
          pass

     def paint(self, draw):
          self.image = Image.open("images/blockImages/"+ self.__class__.__name__+".png")
          self.offset = (int(self.x - self.axis),int(self.y - self.axis))
          draw.paste(self.image, self.offset)
          self.image = None

class NormalBlock(Block):
     pass

class PathBlock(Block):
     def __init__(self,x,y,blockNumber,gridx,gridy):
          super().__init__(x,y,blockNumber,gridx,gridy)
          self.canPlace = False         

class WaterBlock(Block):
     def __init__(self,x,y,blockNumber,gridx,gridy):
          super().__init__(x,y,blockNumber,gridx,gridy)
          self.canPlace = False 

def main():
     game=TowerDefenseGame()

if __name__ == "__main__":
     main()
