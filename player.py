import pygame
from rect import Shape

#FIXME inventory shizz

class Player:
    def __init__(self, game):

        #Initial setup
        self.game = game
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = game.SCREEN_WIDTH, game.SCREEN_HEIGHT
        
        #Player information
        self.rect = pygame.rect.Rect(30, 30, 100, 100)
        self.health = 100
        self.gold = 40  
        self.facingRight = False
        self.hitting = False
        self.healthDecreasing = False
        self.isDead = False
        self.lastTimePoisoned = 0
        self.speed = 3
        
        #Graphics
        self.doctorFacingRight = "doctorFacingRight.xcf"
        self.doctorFacingLeft = "doctorFacingLeft.xcf"
        self.doctorHurtFacingRight = "doctor_hurt_facingRight.xcf"
        self.doctorHurtFacingLeft = "doctor_hurt_facingLeft.xcf"
        self.doctorHittingFacingRight = "doctor_hitting_facingRight.xcf"
        self.doctorHittingFacingLeft = "doctor_hitting_facingLeft.xcf"
        self.coinimg = "COIN.xcf"
        self.font = pygame.font.SysFont(None, 30)
        self.inventoryItemImages = ["Honey.xcf", "Potion.xcf", "vinegar.xcf", "Lavender.xcf", "ROSE.xcf", "MINT.xcf", "medicine1.xcf", "medicine2.xcf", "ointment.xcf"]

        #Inventory information
        self.inventory = {"Honey": 0, "Potion": 0, "Vinegar": 0, "Lavender": 0, "Rose": 0, "Mint": 0, "Penecillin": 0, "Electuary": 0, "Ointment": 0}
        self.itemNames = ["Honey", "Potion", "Vinegar", "Lavender", "Rose", "Mint", "Penecillin", "Electuary", "Ointment"]
        self.inventoryAmounts = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    def draw(self, screen):    
        if self.game.actions["q"]:
            self.hitting = True
        if self.facingRight:
            if self.hitting:
                img_surface = pygame.image.load(self.doctorHittingFacingRight).convert_alpha()
            else:
                img_surface = pygame.image.load(self.doctorFacingRight).convert_alpha()
            if self.healthDecreasing:
                if pygame.time.get_ticks() %1000 <= 100:
                    img_surface = pygame.image.load(self.doctorHurtFacingRight).convert_alpha()
        else:
            if self.hitting:
                img_surface = pygame.image.load(self.doctorHittingFacingLeft).convert_alpha()
            else: 
                img_surface = pygame.image.load(self.doctorFacingLeft).convert_alpha()
            if self.healthDecreasing:
                if pygame.time.get_ticks() %1000 <= 250:
                    img_surface = pygame.image.load(self.doctorHurtFacingLeft).convert_alpha()

        screen.blit(img_surface, self.rect)
        self.hitting =False

    def resetLocation(self, x, value):
        if value:
            self.rect.left = x
        else:
            self.rect.right = x

    def moveFarm(self, key, screen_w, screen_h):   
        if key[pygame.K_UP]:
            self.rect.move_ip(0, -self.speed)
        if key[pygame.K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if key[pygame.K_LEFT]:
            self.facingRight = False
            self.rect.move_ip(-self.speed, 0)        
        if key[pygame.K_RIGHT]:
            self.facingRight = True   
            self.rect.move_ip(self.speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_w:
            self.rect.right = screen_w
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_h:
            self.rect.bottom = screen_h     

    def moveMain(self, key, screen_w, screen_h):
        if key[pygame.K_UP]:
            if not(self.rect.top < 105 and self.rect.right > 670 and self.rect.left < 1155):
                self.rect.move_ip(0, -self.speed)

        if key[pygame.K_DOWN]:
            self.rect.move_ip(0, self.speed)

        if key[pygame.K_LEFT]:
            self.facingRight = False
            if not(self.rect.top <=100 and (self.rect.right > 670 and self.rect.left < 1155)):
                self.rect.move_ip(-self.speed, 0)
            else:
                if self.rect.left - 1155 > -5:
                    self.rect.left = 1160     
        if key[pygame.K_RIGHT]:
            self.facingRight = True 
            if not(self.rect.top <=100 and (self.rect.right > 670 and self.rect.left < 1155)):
                self.rect.move_ip(self.speed, 0)
            else:
                if 670 - self.rect.right < -5:
                    self.rect.left = 1155 
    
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_w:
            self.rect.right = screen_w
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_h:
            self.rect.bottom = screen_h   

    def showInventory(self, screen):
        inventory_img_surface = pygame.image.load("pack.xcf").convert_alpha()
        self.inventoryRect = pygame.rect.Rect(0, self.SCREEN_HEIGHT/4, 370, 280)
        screen.blit(inventory_img_surface, self.inventoryRect)

        offsetx = 0
        offsety = 0

        for x in range(9):
            #reset
            if x % 3 == 0 and x != 0:
                offsetx = 0
                offsety += 90
            img_surface = pygame.image.load(self.inventoryItemImages[x]).convert_alpha()
            transformed_img = pygame.transform.scale(img_surface, (50, 50))
            text_surface = self.font.render("X " + str(self.inventoryAmounts[x]), True, (0,0,0))
            transformed_txt = pygame.transform.scale(text_surface, (20, 20))
            img_rect = transformed_img.get_rect()
            text_rect = transformed_txt.get_rect()
            text_rect.topleft = (offsetx + 70, self.SCREEN_HEIGHT/4 + offsety+25)
            img_rect.topleft = (offsetx, self.SCREEN_HEIGHT/4 + offsety)
            
            screen.blit(transformed_img, img_rect)
            screen.blit(transformed_txt, text_rect)
            offsetx+=90
        #Health bar:
        Shape.drawRect(Shape, screen, self.SCREEN_HEIGHT-100, self.SCREEN_WIDTH - 100, 100, 100, (175,175,175))
        img_surface = pygame.image.load(self.coinimg).convert_alpha()
        screen.blit(img_surface, (self.SCREEN_WIDTH-100, self.SCREEN_HEIGHT-100))
        text_surface = self.font.render(str(self.gold), True, (0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.center = (self.SCREEN_WIDTH-120, 670)
        screen.blit(text_surface, text_rect)
    


    def displayHealth(self, screen):
        black_rect = pygame.rect.Rect(self.rect.x -10, self.rect.y -10, 10, 50)
        pygame.draw.rect(screen, (0, 0, 0), black_rect)
        rect = pygame.rect.Rect(self.rect.x, self.rect.y , 10, self.health/2)
        rect.bottomleft = black_rect.bottomleft

        if self.health > 60:
            pygame.draw.rect(screen, (0, 250, 0), rect)
        elif self.health >20:
            pygame.draw.rect(screen, (255, 219, 88), rect)
        else:
            pygame.draw.rect(screen, (255, 0, 0), rect)

    def addToInventory(self, item):
        for x in range(9):
            if self.itemNames[x] == item:
                self.inventory[item] = self.inventory[item] +1
                self.inventoryAmounts[list(self.inventory.keys()).index(item)] += 1

    def harvestPlant(self, cropLocations, types, cropTypes, size):
        for o in range(len(cropLocations)):
            if abs(self.rect.top - cropLocations[o][1]) <=100 and abs(self.rect.left - cropLocations[o][0]) <=100:
                cropLocations.pop(o)                
                self.inventory[cropTypes[types[o]]] += 1
                types.pop(o)
                size -= 1

    def loseHealth(self):
        self.health = self.health-5
        if self.health <= 0:
            self.isDead = True
            return True
        else:
            return False

    def playerHealthStatus(self):
        if self.healthDecreasing:
            self.speed = 2
            time = pygame.time.get_ticks() - self.lastTimePoisoned
            if (time) % 1000 < 5:
                return self.loseHealth()
            if (time)/1000 >= 15:
                self.healthDecreasing = False
        else:
            self.speed = 3
            return False

    def addHealth(self):
        self.healthDecreasing = False
        self.health += 20   
        if self.health > 100:
            self.health = 100

    def decreaseGold(self, amount):
        self.gold -= amount
    
    def increaseGold(self, amount):
        self.gold += amount

    def moveWithCollides(self, key, screen_w, screen_h, rect):    
        if key[pygame.K_UP]:
            self.rect.move_ip(0, -2)
            if self.rect.colliderect(rect):
                self.rect.top = rect.bottom
                self.rect.move_ip(0, 2)
        if key[pygame.K_DOWN]:
            self.rect.move_ip(0, 2)
            if self.rect.colliderect(rect):
                self.rect.bottom = rect.top
        if key[pygame.K_LEFT]:
            self.rect.move_ip(-2, 0)  
            self.facingRight = False
            if self.rect.colliderect(rect):
                self.rect.left = rect.right 
        if key[pygame.K_RIGHT]:
            self.facingRight = True
            self.rect.move_ip(2, 0)
            if self.rect.colliderect(rect):
                self.rect.right = rect.left 
   
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_w:
            self.rect.right = screen_w
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_h:
            self.rect.bottom = screen_h 

    def checkMaterials(self, ingredients, ingredient_amounts):
        if self.inventoryAmounts[list(self.inventory.keys()).index(ingredients[0])] >= ingredient_amounts[0] and self.inventoryAmounts[list(self.inventory.keys()).index(ingredients[1])] >= ingredient_amounts[1] and self.inventoryAmounts[list(self.inventory.keys()).index(ingredients[2])] >= ingredient_amounts[2]:
            self.inventoryAmounts[list(self.inventory.keys()).index(ingredients[0])] -= ingredient_amounts[0]
            self.inventoryAmounts[list(self.inventory.keys()).index(ingredients[1])] -= ingredient_amounts[1]
            self.inventoryAmounts[list(self.inventory.keys()).index(ingredients[2])] -= ingredient_amounts[2]
            return True
        return False
        
    def checkMedicine(self, num, type):
        if self.inventoryAmounts[list(self.inventory.keys()).index(type)] >= num:
            self.inventoryAmounts[list(self.inventory.keys()).index(type)] -= num
            return True
        else:
            return False
        
    def checkPotion(self):
        if self.inventoryAmounts[list(self.inventory.keys()).index("Potion")] > 0:
            return True
        else:
            return False
        
    def canPurchase(self, amount):
        if self.gold - amount >= 0:
            return True
        else:
            return False
