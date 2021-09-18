import gameGlobal

blockDictionary = ["NormalBlock", "PathBlock","WaterBlock"]
monsterDictionary = ["Monster1", "Monster2","AlexMonster","BenMonster","LeoMonster","MonsterBig"]
towerDictionary = {"Arrow Shooter":"ArrowShooterTower", "Bullet Shooter":"BulletShooterTower", "Tack Tower": "TackTower", "Power Tower": "PowerTower"}
towerCost = {"Arrow Shooter":150,"Bullet Shooter":150,"Tack Tower":150, "Power Tower":200}
towerGrid = [[None for y in range(gameGlobal.gridSize)] for x in range(gameGlobal.gridSize)]
pathList = []
spawnx = 0
spawny = 0
monsters = []
monstersByHealth = []
monstersByHealthReversed = []
monstersByDistance = []
monstersByDistanceReversed = []
monstersListList = [monstersByHealth,monstersByHealthReversed,monstersByDistance,monstersByDistanceReversed]
projectiles = []
health = 100
displayTower = None