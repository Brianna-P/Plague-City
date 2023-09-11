from state import State
from enemy import Enemy
import pygame
import random

class FarmScreen(State):
    def __init__(self, game):

        #Initial setup
        State.__init__(self, game)
        self.game = game
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = game.SCREEN_WIDTH, game.SCREEN_HEIGHT
        
        #Graphics
        self.background = pygame.image.load("BACKGROUND_CITY.xcf")
        self.font = pygame.font.SysFont(None, 30)
        self.coinImg = "COIN.xcf"
        self.bonk_sound = pygame.mixer.Sound("bonk.mp3")
        
        #Crop information
        self.cropImages = [ "MINT.xcf", "ROSE.xcf", "Lavender.xcf"]
        self.cropTypes = ["Mint", "Rose", "Lavender"]
        self.types = []
        self.cropRects = []
        self.cropLocations = []
        self.currentNumCrops = 0
        self.maxCrops = 15
        self.radius = 10
        self.makeCrops(10)
        
        #Enemy information
        self.enemy = Enemy(game)
        self.enemy.makeEnemies(4, True)

        #Game logic
        self.inInventory = False
        self.inControls = False

        #Render popups
        self.coinFadingTimers = []
        self.plantFadingTimers = []

    def enter_state(self):
        pygame.mixer.music.pause
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
            self.player = self.prev_state.player
            self.player.resetLocation(5, True)
        self.game.state_stack.append(self)
        pygame.mixer.music.load("KingDedede.mp3")
        pygame.mixer.music.play(-1)

    def exit_state(self):
        self.game.state_stack.pop()
        self.player.resetLocation(1265, False)
        pygame.mixer.music.pause()

    def update(self, actions):
        key = pygame.key.get_pressed()
        self.player.moveFarm(key, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        if self.player.rect.left < 1:
            self.inInventory = False
            self.exit_state()

        
        if actions["r"]:       
            if self.player.checkPotion() and self.player.health < 100:
                self.player.addHealth()
                self.player.inventoryAmounts[list(self.player.inventory.keys()).index("Potion")] -= 1
        if actions["e"]:
            if self.inInventory:
                self.inInventory = False
            else:
                self.inInventory = True
        if actions["escape"]:
            if self.inControls:
                self.inControls = False
            else:
                self.inControls = True

        if self.player.playerHealthStatus():
            self.game.game_is_over = True
            self.game.gameOverScreen.enter_state()
                
        self.game.actions["r"] = False 
        self.game.actions["e"] = False
        self.game.actions["escape"] = False

    def render(self, screen):
        self.checkOverlap(self.game.actions)

        screen.fill((211,211,211))
        pygame.display.set_caption("LOCATION: CITY OUTSKIRTS")
        screen.blit(pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0, 0))
        self.putCrops(screen)
        self.enemy.putEnemies(screen)
        self.enemyMovement()
        self.player.draw(screen)
        self.player.displayHealth(screen)

        if self.inInventory:
            self.player.showInventory(screen)

        if len(self.coinFadingTimers) > 0:
            self.renderRatDrop()

        if len(self.plantFadingTimers) > 0:
            self.renderPlantDrop()
            
        if self.inControls:
            self.game.controlsScreen.renderControls()
 
    def runFarm(self):
        if pygame.time.get_ticks() % 20000 <=  10 and self.enemy.numEnemies < 8:
            self.enemy.makeEnemies(random.randint(1,2), False)
        if pygame.time.get_ticks() % 15000 <= 10 and self.currentNumCrops < 12:
            self.makeCrops(2)

    def makeCrops(self, currentNumCrops):
        for i in range(currentNumCrops):
            num = random.randint(0, 99)
            if num < 24:
                type = 0
            elif num < 49:
                type = 1
            else:
                type = 2
            self.types.append(type)
            xx = random.randint(0, 1180)
            yy = random.randint(30, 620)
            self.cropRects.append(pygame.rect.Rect(xx, yy, 50, 50))
            self.cropLocations.append([xx, yy])
            self.currentNumCrops += 1

    def putCrops(self, screen):
        for x in range(self.currentNumCrops):
            img_surface = pygame.image.load(self.cropImages[self.types[x]]).convert_alpha()
            conformed = pygame.transform.scale(img_surface, (50, 50))
            screen.blit(conformed, self.cropRects[x])

    def checkOverlap(self, actions):
        for x in range(self.currentNumCrops):
            if self.cropRects[x].colliderect(self.player.rect):
                if actions["q"]:
                    xx = self.cropRects[x].x
                    yy = self.cropRects[x].y
                    img = self.cropImages[self.types[x]]
                    self.plantFadingTimers.append([xx, yy, pygame.time.get_ticks(), img])
                    self.cropRects.pop(x) 
                    self.player.addToInventory(self.cropTypes[self.types[x]])
                    self.types.pop(x)
                    self.currentNumCrops -= 1
                break
        for x in range(len(self.enemy.enemyRects)):
            if self.enemy.enemyRects[x].colliderect(self.player.rect):
                if actions["q"]:
                    self.bonk_sound.play()
                    self.bonk_sound.set_volume(0.9)
                    dropCoinChance = random.randint(0, 1)  
                    if (dropCoinChance == 1):
                        xx = self.enemy.enemyRects[x].x
                        yy = self.enemy.enemyRects[x].y
                        self.coinFadingTimers.append([xx, yy, pygame.time.get_ticks()])
                        self.player.increaseGold(5)

                    self.enemy.enemyRects.pop(x)
                    self.enemy.numEnemies -= 1
                    self.enemy.Locations.pop(x)
                    break

                enemy_center = self.enemy.enemyRects[x].center
                player_center = self.player.rect.center
                if (abs(enemy_center[0] - player_center[0]) <= 50) and (abs(enemy_center[1] - player_center[1]) <= 50):
                    if not self.player.healthDecreasing:
                        self.player.healthDecreasing = True
                        self.player.lastTimePoisoned = pygame.time.get_ticks()
    
    def enemyMovement(self):
        for x in range(len(self.enemy.enemyRects)):
            x_distance = abs(self.player.rect.x - self.enemy.enemyRects[x].x)
            y_distance = abs(self.player.rect.y - self.enemy.enemyRects[x].y)
            if x_distance <= 200 and y_distance <= 200:
                self.enemy.move_towards_player(self.player, x)
            else:
                self.enemy.moveEnemiesRandom(x) 

    def renderFadingImage(self, x, y, screen, amount, img):
        text_surface = self.font.render("+" + str(amount), True, (0,0,0))
        text_rect = text_surface.get_rect()
        pygame.transform.scale(text_surface, (50, 50))
        text_rect.topleft = (x, y)
        img_surface = pygame.image.load(img).convert_alpha()
        img_rect = pygame.rect.Rect(x, y, 100, 100)
        screen.blit(pygame.transform.scale(img_surface, (50, 50)), img_rect)
        screen.blit(text_surface, text_rect)

    def renderRatDrop(self):
        for x in range(len(self.coinFadingTimers)):
            if (pygame.time.get_ticks() - self.coinFadingTimers[x][2])/1000 < 1:
                self.renderFadingImage(self.coinFadingTimers[x][0], self.coinFadingTimers[x][1], self.game.screen, 5, self.coinImg)
                self.coinFadingTimers[x][1] -= 1
            else:
                self.coinFadingTimers.pop(x)
                break

    def renderPlantDrop(self):
        for x in range(len(self.plantFadingTimers)):
            if (pygame.time.get_ticks() - self.plantFadingTimers[x][2])/1000 < 1:
                self.renderFadingImage(self.plantFadingTimers[x][0], self.plantFadingTimers[x][1], self.game.screen, 1, self.plantFadingTimers[x][3])
                self.plantFadingTimers[x][1] -= 1
            else:
                self.plantFadingTimers.pop(x)
                break
