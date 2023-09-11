from state import State
from rect import Shape
from player import Player
from rect import Shape
import pygame
from npc import NPC
import math

class Main(State):
    def __init__(self, game):

        #Initial setup
        State.__init__(self, game)
        self.game = game
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = game.SCREEN_WIDTH, game.SCREEN_HEIGHT
        self.player = Player(game)

        #Graphics
        self.background = pygame.image.load("BACKGROUND.xcf")
        self.coinimg = "COIN.xcf"
        self.woodImg = "wood.xcf"
        self.brewImg = "brew.xcf"
        self.marketImg = "MARKET.xcf"
        self.font = pygame.font.SysFont(None, 30)

        #Game logic
        self.atMarket = False
        self.atBrew = False
        self.inInventory = False
        self.currentlyBrewing = False
        self.inControls = False
        self.enteringState = False
        self.time_entered_state = 0

        #NPC information
        self.npcRects = [pygame.Rect(100, 500, 100, 100), pygame.Rect(350, 120, 100, 100), pygame.Rect(900, 350, 100, 100)]
        self.npcs = [NPC(self.npcRects[0], "NPC1.xcf", self.game.screen, game), NPC(self.npcRects[1], "NPC2.xcf", self.game.screen, game), NPC(self.npcRects[2], "NPC3.xcf", self.game.screen, game)]
        self.medicineImages = ["medicine1.xcf", "medicine2.xcf", "Ointment.xcf"]
        self.medicineTypes = ["Penecillin", "Electuary", "Ointment"]
        self.npcPayment = 20

        #Market information      
        self.vinegarImg = pygame.image.load("vinegar.xcf").convert_alpha()
        self.potionImg = pygame.image.load("Potion.xcf").convert_alpha()
        self.honeyImg = pygame.image.load("Honey.xcf").convert_alpha()
        self.itemPrices = [10, 5, 15]
        self.marketListItems = ["Vinegar", "Potion", "Honey"]
        self.itemLocations = [pygame.rect.Rect(self.SCREEN_WIDTH/2 -250, self.SCREEN_HEIGHT/2, 100, 100), pygame.rect.Rect(self.SCREEN_WIDTH/2 - 50, self.SCREEN_HEIGHT/2, 100, 100), pygame.rect.Rect(self.SCREEN_WIDTH/2 + 150, self.SCREEN_HEIGHT/2, 100, 100)]
        self.itemSelected = [False, False, False]

        #Brewery information
        self.recipeIngredientsDisplay = {"Penecillin": ["Vinegar", "Rose", "Lavender"], "Electuary": ["Honey", "Mint", "Lavender"], "Ointment": ["Vinegar", "Honey", "Lavender"]}
        self.recipeIngredientsAmounts = [[2, 1, 3], [2, 3, 4], [3, 2, 2]]  #[[0, 0, 0],[0, 0, 0],[0, 0, 0]]
        self.recipeIngredientsImages = [["vinegar.xcf", "ROSE.xcf", "Lavender.xcf"], ["Honey.xcf", "MINT.xcf", "Lavender.xcf"], ["vinegar.xcf", "Honey.xcf", "Lavender.xcf"]]
        self.brewQueueImages = []
        self.brewQueueTimers = []
        self.brewQueueTypes = []

        #Rendering popups
        self.coins = []
        self.ingredients = []
        self.questsCompleted = []
        self.marketPopUpTimer = 0
        self.brewPopUpTimer = 0

    def update(self, actions):
        key = pygame.key.get_pressed()
        if actions["q"]:       
            self.player.hitting = True 
        
        if actions["r"]:       
            if self.player.checkPotion() and self.player.health < 100:
                self.player.addHealth()
#FIXME if we wanna remove inventory dict from player change this
                self.player.inventoryAmounts[list(self.player.inventory.keys()).index("Potion")] -= 1
        
        if not(self.atMarket or self.atBrew):
            self.player.moveMain(key, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
        if self.player.rect.right > 1279:
            self.atMarket, self.inInventory, self.atBrew = False, False, False
            self.game.farmScreen.enter_state()

        if actions["e"]:
            if self.inInventory:
                self.inInventory = False
            else:
                self.inInventory = True

        if actions["w"]: 
            if self.atBrew:
                self.atBrew = False
            else:
                if self.player.rect.left < 165 and self.player.rect.top > 230 and self.player.rect.top < 390: #and self.player.rect.top < 100
                    self.atBrew = True
            if self.atMarket:
                self.atMarket = False
            else:
                if self.player.rect.left < 1000 and self.player.rect.right > 830 and self.player.rect.top < 170: #and self.player.rect.top < 100
                    self.atMarket = True  
        
        if actions["escape"]:
            self.enteringState = False
            if self.inControls:
                self.inControls = False
            else:
                self.inControls = True
        
        self.game.actions["escape"] = False 
        self.game.actions["w"] = False 
        self.game.actions["e"] = False
        self.game.actions["r"] = False

        if self.player.playerHealthStatus():
            self.game.game_is_over = True
            self.game.gameOverScreen.enter_state()

    def render(self, screen):
        screen.fill((211,211,211))
        pygame.display.set_caption("LOCATION: BLACK PLAGUE CITY")
        screen.blit(pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0, 0))
        
        #PLAYER
        self.player.draw(screen)
        self.player.displayHealth(self.game.screen)

        #NPC
        for x in range(len(self.npcs)):
            self.npcs[x].draw()
            if self.npcs[x].moveable:
                self.npcs[x].npcMovement()
        self.npcOverlap(self.game.actions)

        #INVENTORY
        if self.inInventory:
           self.player.showInventory(self.game.screen)

        #MARKET:
        if self.atMarket:
            self.showMarketScreen(self.game.screen)

        #BREWERY
        if self.atBrew:
            self.showBrewScreen(self.game.screen)

        #BREW QUEUE
        if self.currentlyBrewing:
            Shape.drawRect(Shape, screen, 0, 0, 175, 55, (0, 0, 0))
            Shape.drawRect(Shape, screen, 0, 0, 170, 50, (211, 211, 211))
            Shape.drawRect(Shape, screen, 55, 0, 10, 50, (0, 0, 0))
            if len(self.brewQueueTimers) > 0:
                self.renderBrewQueue(screen)
        if self.inControls:
            self.game.controlsScreen.renderControls()
 
        if (pygame.time.get_ticks() - self.brewPopUpTimer)/1000 <2 and self.brewPopUpTimer != 0:
            self.popUp("Insufficient Materials!")
        if (pygame.time.get_ticks() - self.marketPopUpTimer)/1000 <2 and self.marketPopUpTimer != 0:
            self.popUp("Not Enough Gold!")
        
        if len(self.coins) >0:
            self.renderCoinsSpent(screen)
        if len(self.ingredients) >0:
            self.renderBrewPlantsUsed()
        if len(self.questsCompleted) > 0:
            self.npcQuestCompleted()

        if self.enteringState:
            if pygame.time.get_ticks()/1000 - self.time_entered_state < 5:
                Shape.drawRect(Shape, screen, self.SCREEN_WIDTH/2 - 325/2, self.SCREEN_HEIGHT/2 - 75/2, 325, 75, (0,255,255))
                woodRect = pygame.rect.Rect(self.SCREEN_WIDTH/2 - 300/2, self.SCREEN_HEIGHT/2 - 50/2, 300, 50)
                wood_img_surface = pygame.image.load(self.woodImg).convert_alpha()
                screen.blit(pygame.transform.scale(wood_img_surface, (300, 50)), woodRect)
                instructions_surface = self.font.render("For instructions, press ESC", True, (0,0,0))
                instructions_rect = instructions_surface.get_rect()
                pygame.transform.scale(instructions_surface, (300, 50))
                instructions_rect.topleft = (self.SCREEN_WIDTH/2 - 300/2 + 10, self.SCREEN_HEIGHT/2 - 50/2 + 10)
                screen.blit(instructions_surface, instructions_rect)
            else:
                self.enteringState = False
            
    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)
        self.enteringState = True
        self.time_entered_state = pygame.time.get_ticks()/1000

    def showBrewScreen (self, screen):
        Shape.drawRect(Shape, self.game.screen, self.SCREEN_WIDTH/2 - 400, self.SCREEN_HEIGHT/2 -250, 800, 600, (250,250,250))
        brew_img_surface = pygame.image.load(self.brewImg).convert_alpha()
        self.brewRect = pygame.rect.Rect(self.SCREEN_WIDTH/2 -400, self.SCREEN_HEIGHT/2 -250, 800, 600)
        screen.blit(brew_img_surface, self.brewRect)

        locationIncrement = -250
        for x in range(3): 
            text_surface = self.font.render(self.medicineTypes[x], True, (0,0,0))
            text_rect = text_surface.get_rect()
            text_rect.center = (self.SCREEN_WIDTH/2+ locationIncrement +50, self.SCREEN_HEIGHT/2 + 150)
            screen.blit(text_surface, text_rect)
            locationIncrement += 200

        screen.blit(pygame.image.load(self.medicineImages[0]), self.itemLocations[0])
        screen.blit(pygame.image.load(self.medicineImages[1]), self.itemLocations[1])
        screen.blit(pygame.image.load(self.medicineImages[2]), self.itemLocations[2])                
        
        counter = 0
        index = 0
        for key in self.recipeIngredientsDisplay:
            text_surface = self.font.render(key +":", True, (0,0,0))
            text_rect = text_surface.get_rect()
            xlocaiton = self.SCREEN_WIDTH/2 - 200 + counter
            text_rect.center =  (xlocaiton, 600)
            screen.blit(text_surface, text_rect)
            yincrement = 20
            for x in range(3):
                ingredient = self.font.render(self.recipeIngredientsDisplay[key][x] + " X " + str(self.recipeIngredientsAmounts[index][x]), True, (0,0,0,))
                ingredient_rect = ingredient.get_rect()
                ingredient_rect.center = (xlocaiton, 600+ 30 + yincrement )
                yincrement += 20
                screen.blit(ingredient, ingredient_rect)
            counter += 200
            index += 1
            
        #Event handling
        x, y = pygame.mouse.get_pos()
        if(abs(x - self.SCREEN_WIDTH/2 +200) <= 50 and abs(y- 410) <= 50):
            self.itemSelected[0] = True
        if(abs(x - self.SCREEN_WIDTH/2) <= 50 and abs(y- 410) <= 50):
            self.itemSelected[1] = True
        if(abs(x - self.SCREEN_WIDTH/2 - 200) <= 50 and abs(y- 410) <= 50):
            self.itemSelected[2] = True

        for x in range(3):
            if self.itemSelected[x]:
                self.itemLocations[x].top = self.SCREEN_HEIGHT/2 -50
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.player.checkMaterials(list(self.recipeIngredientsDisplay.values())[x], self.recipeIngredientsAmounts[x]):
                            self.currentlyBrewing = True
                            self.addToBrewQueue(x)
                            xx = self.itemLocations[x].x
                            yy = self.itemLocations[x].y
                            index = x
                            self.ingredients.append([xx, yy, pygame.time.get_ticks(), index])
                        else:
                            self.brewPopUpTimer = pygame.time.get_ticks()                            
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_w:
                            self.atBrew = False 
            else:
                self.itemLocations[x].top = self.SCREEN_HEIGHT/2
        #reset
        for x in range(3):
            self.itemSelected[x] = False

    def showMarketScreen(self, screen):
        self.marketRect = pygame.rect.Rect(self.SCREEN_WIDTH/2 -400, self.SCREEN_HEIGHT/2 -250, 800, 500)
        Shape.drawRect(Shape, self.game.screen, self.SCREEN_WIDTH/2 - 400, self.SCREEN_HEIGHT/2 -250, 800, 500, (250,250,250))
        market_img_surface = pygame.image.load(self.marketImg).convert_alpha()
        screen.blit(market_img_surface, self.marketRect)
        
        img_surface = pygame.image.load(self.coinimg).convert_alpha()
        transformed_img = pygame.transform.scale(img_surface, (50, 50))
        
        locationIncrement = -250
        for x in range(3): 
            #prices
            price_surface = self.font.render("X " + str(self.itemPrices[x]), True, (0,0,0))
            coin_rect = transformed_img.get_rect()
            text_rect = price_surface.get_rect()
            text_rect.center = (self.SCREEN_WIDTH/2+ locationIncrement +70, self.SCREEN_HEIGHT/2 + 125)
            coin_rect.center = (self.SCREEN_WIDTH/2 +locationIncrement +30, self.SCREEN_HEIGHT/2 +125)
            
            

            
            screen.blit(transformed_img, coin_rect)
            screen.blit(price_surface, text_rect)
            locationIncrement += 200

            type_surface = self.font.render(self.marketListItems[x], True, (0,0,0))
            type_rect = type_surface.get_rect()
            type_rect.center = (self.SCREEN_WIDTH/2+ locationIncrement -150, self.SCREEN_HEIGHT/2 + 170)
            screen.blit(type_surface, type_rect)

        screen.blit(self.vinegarImg, self.itemLocations[0])
        screen.blit(self.potionImg, self.itemLocations[1])
        screen.blit(self.honeyImg, self.itemLocations[2])

        #Event handling
        x, y = pygame.mouse.get_pos()
        if(abs(x - self.SCREEN_WIDTH/2 +200) <= 50 and abs(y- 410) <= 50):
            self.itemSelected[0] = True
        if(abs(x - self.SCREEN_WIDTH/2) <= 50 and abs(y- 410) <= 50):
            self.itemSelected[1] = True
        if(abs(x - self.SCREEN_WIDTH/2 - 200) <= 50 and abs(y- 410) <= 50):
            self.itemSelected[2] = True

        for x in range(3):
            if self.itemSelected[x]:
                self.itemLocations[x].top = self.SCREEN_HEIGHT/2 -50
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.player.canPurchase(self.itemPrices[x]):
                            self.player.decreaseGold(self.itemPrices[x])
                            xx = self.itemLocations[x].left
                            y = self.itemLocations[x].top
                            self.coins.append([pygame.time.get_ticks(), self.itemPrices[x] * -1, [xx, y]])
                            self.player.addToInventory(self.marketListItems[x])
                        else:
                            self.marketPopUpTimer = pygame.time.get_ticks()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_w:
                            self.atMarket = False
            else:
                self.itemLocations[x].top = self.SCREEN_HEIGHT/2
        #reset
        for x in range(3):
            self.itemSelected[x] = False

    def addToBrewQueue(self, num):
        self.brewQueueImages.append(self.medicineImages[num])
        self.brewQueueTypes.append(self.medicineTypes[num])
        self.brewQueueTimers.append(pygame.time.get_ticks())

    def renderBrewQueue(self, screen):
        currentTime = math.floor((pygame.time.get_ticks() - self.brewQueueTimers[0])/1000)
        if currentTime < 5:
            text_surface1 = self.font.render(str(5 - currentTime), True, (0,0,0))
            text_surface2 = self.font.render("Brewing..", True, (0,0,0))
            text_rect1 = text_surface1.get_rect()
            text_rect2 = text_surface2.get_rect()
            text_rect2.w, text_rect2.h = 100, 50
            text_rect2.center = (120, 40)
            temp = pygame.rect.Rect(0, 0, 70, 50)
            Shape.drawRect(Shape, screen, 0, 50, 175, 15, (0, 0, 0))
            pygame.draw.rect(screen, (0,250,0), pygame.Rect(0,50,170*(currentTime/5),10))
            
            img_surface = pygame.transform.scale(pygame.image.load(self.brewQueueImages[0]).convert_alpha(), (50, 50))
            screen.blit(img_surface, temp)
            screen.blit(text_surface1, text_rect1)
            screen.blit(text_surface2, text_rect2)
        else:
            self.player.addToInventory(self.brewQueueTypes[0])
            self.brewQueueTypes.pop(0)
            self.brewQueueImages.pop(0)
            self.brewQueueTimers.pop(0)
            if len(self.brewQueueTimers) > 0:
                self.brewQueueTimers[0] = pygame.time.get_ticks()
            else:
                self.currentlyBrewing = False

    def npcOverlap(self, actions):
        for x in range(3):
            if abs(self.npcRects[x].x - self.player.rect.x) <= 120 and abs(self.npcRects[x].y - self.player.rect.y) <= 120: 
                self.npcs[x].moveable = False
                if self.player.rect.colliderect(self.npcRects[x]):
                    if self.player.rect.right - self.npcRects[x].left <= 3:
                        self.player.rect.right = self.npcRects[x].left - 4
                    if self.npcRects[x].bottom - self.player.rect.top <= 3:
                        self.player.rect.top = self.npcRects[x].bottom + 4
                    if self.npcRects[x].right - self.player.rect.left <= 3:
                        self.player.rect.left = self.npcRects[x].right + 4
                    if self.player.rect.bottom - self.npcRects[x].top <= 3:
                        self.player.rect.bottom = self.npcRects[x].top - 4
                self.npcs[x].showRequest()
                if actions["t"] and self.player.checkMedicine(self.npcs[x].numOfMedicine, self.npcs[x].typeOfMedicine):
                    temp = "medicine"
                    for y in range(len(self.medicineTypes)):
                        if self.npcs[x].typeOfMedicine == self.medicineTypes[y]:
                            temp = self.medicineImages[y]
                            break
                    self.questsCompleted.append([self.npcs[x].numOfMedicine, temp, pygame.time.get_ticks(), self.player.rect.x, self.player.rect.y])
                    self.npcs[x].generateNpcRequests()
                    self.player.increaseGold(self.npcPayment)
            else:
                self.npcs[x].moveable = True 
                self.npcs[x].showBubbles()

    def popUp(self, msg):
        #Shape.drawRect(Shape,self.game.screen, self.SCREEN_WIDTH/2 -125, 0, 250, 40, (175,175,175))
        button_img_surface = pygame.image.load("woodButton.xcf").convert_alpha()
        buttonRect = button_img_surface.get_rect()
        buttonRect.center = (self.SCREEN_WIDTH/2- 50, 50)
        self.game.screen.blit(pygame.transform.scale(button_img_surface, (300, 100)), buttonRect)

        text_surface = self.font.render(msg, True, (0,0,0))
        text_rect = text_surface.get_rect()
        pygame.transform.scale(text_surface, (100, 100))
        text_rect.topleft = (self.SCREEN_WIDTH/2 - 115, 40)
        self.game.screen.blit(text_surface, text_rect)

    def renderFadingImage(self, x, y, screen, amount, img):
        text_surface = self.font.render(amount, True, (0,0,0))
        text_rect = text_surface.get_rect()
        pygame.transform.scale(text_surface, (50, 50))
        text_rect.topleft = (x, y)
        img_surface = pygame.image.load(img).convert_alpha()
        img_rect = pygame.rect.Rect(x, y, 100, 100)
        screen.blit(pygame.transform.scale(img_surface, (50, 50)), img_rect)
        screen.blit(text_surface, text_rect)
        
    def renderCoinsSpent(self, screen):
        for x in range(len(self.coins)):
            if (pygame.time.get_ticks() - self.coins[x][0])/1000 < 1:
                self.renderFadingImage(self.coins[x][2][0] + 20, self.coins[x][2][1] - 250, screen, "- " +str(self.coins[x][1]), self.coinimg)
                self.coins[x][2][1] -= 2
            else:
                self.coins.pop(x)
                break
    
    def npcQuestCompleted(self):
        for x in range(len(self.questsCompleted)):
            if (pygame.time.get_ticks() - self.questsCompleted[x][2])/1000 < 1:
                self.renderFadingImage(self.questsCompleted[x][3], self.questsCompleted[x][4], self.game.screen, "-"+ str(self.questsCompleted[x][0]), self.questsCompleted[x][1])
                self.renderFadingImage(self.questsCompleted[x][3], self.questsCompleted[x][4]+ 50, self.game.screen, "+" + str(self.npcPayment), self.coinimg)
                self.questsCompleted[x][4] -= 1
            else:
                self.questsCompleted.pop(x)
                break

    def renderBrewPlantsUsed(self):
        for x in range(len(self.ingredients)):
            if (pygame.time.get_ticks() - self.ingredients[x][2])/1000 < 1:
                #xx yy pypgame tick, index
                self.renderFadingImage(self.ingredients[x][0], self.ingredients[x][1], self.game.screen,"-" +str(self.recipeIngredientsAmounts[self.ingredients[x][3]][0]), self.recipeIngredientsImages[self.ingredients[x][3]][0])
                self.renderFadingImage(self.ingredients[x][0], self.ingredients[x][1] + 30, self.game.screen, "-" +str(self.recipeIngredientsAmounts[self.ingredients[x][3]][1]), self.recipeIngredientsImages[self.ingredients[x][3]][1])
                self.renderFadingImage(self.ingredients[x][0], self.ingredients[x][1]+ 60, self.game.screen, "-" +str(self.recipeIngredientsAmounts[self.ingredients[x][3]][2]), self.recipeIngredientsImages[self.ingredients[x][3]][2])
                self.ingredients[x][1] -= 2
                    
            else:
                self.ingredients.pop(x)
                break