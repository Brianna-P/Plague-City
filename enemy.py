import pygame
import random
import math

class Enemy():
    def __init__(self, game):

        #Initial setup
        self.game = game
        self.rect = pygame.rect.Rect(30, 30, 50, 50)
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = game.SCREEN_WIDTH, game.SCREEN_HEIGHT
        
        #Graphics
        self.ratImgFacingLeft = "ratFacingLeft.xcf"
        self.ratImgFacingRight = "ratFacingRight.xcf"

        #Game logic
        self.speed = 1.5
        self.facingRight = False
        self.numEnemies = 0
        self.maxEnemies = 10
        self.Locations =[]
        self.enemyRects = []
        self.enemyTargets = []

    def makeEnemies(self, num, beginnning):
        for x in range(num):
            xx =0
            if beginnning:
                xx = random.randint(100, 1100)
            else:
                xx = 1200
            yy = random.randint(100, 620)
            self.enemyRects.append(pygame.rect.Rect(xx, yy, 50, 50))
            self.Locations.append([xx, yy, 50, 50])
            self.numEnemies +=1
            self.enemyTargets.append([xx, yy])

    def putEnemies(self, screen):
        for enemy in range(self.numEnemies):
            if self.facingRight:
                img_surface = pygame.image.load(self.ratImgFacingRight).convert_alpha()
            else:
                img_surface = pygame.image.load(self.ratImgFacingLeft).convert_alpha()
            screen.blit(img_surface, self.enemyRects[enemy])    

    def move_towards_player(self, player, num):
        dx, dy = player.rect.left - self.enemyRects[num].x, player.rect.top - self.enemyRects[num].y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist  
        self.enemyRects[num].x += dx * self.speed 
        self.enemyRects[num].y += dy * self.speed

    def generateNewSpot(self, x):
        xx = random.randint(0, 1200)
        yy = random.randint(0, 670)
        self.enemyTargets[x] = [xx, yy]

    def moveEnemiesRandom(self,x):
        dx, dy = self.enemyTargets[x][0] - self.enemyRects[x].x, self.enemyTargets[x][1] - self.enemyRects[x].y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        else:
            self.generateNewSpot(x)
        self.enemyRects[x].x += dx * self.speed
        self.enemyRects[x].y += dy * self.speed