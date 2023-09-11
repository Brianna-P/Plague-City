import random
import pygame

class NPC():
    def __init__(self, rect, img, screen, game):

        #Initial setup
        self.game = game
        self.screen = screen
        self.rect = rect

        #Graphics
        self.img = img
        self.font = pygame.font.SysFont(None, 30)
        self.BLACK = (0, 0, 0)
        self.chatImg = "chatBubble.xcf"
        self.requestImg = "requestBubble.xcf"

        #Requests Information
        self.hasPendingQuest = False
        self.medicines = ["Penecillin", "Electuary", "Ointment"]
        self.npcVoice = ""
        self.numOfMedicine = 0
        self.typeOfMedicine = ""
        self.firstSpawn = pygame.time.get_ticks()
        self.generateNpcRequests()

        #Moving logic
        self.startLocationX = self.rect.x +100
        self.startLocationY = self.rect.y +100
        self.direction = random.randint(0,1)
        self.y_directional = 1
        self.x_directional = 1
        self.moveable = True

    def draw(self):
        img_surface = pygame.image.load(self.img).convert_alpha()
        self.screen.blit(img_surface, self.rect)

    def talk(self, voiceLine):
        text_surface = self.font.render(voiceLine, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.rect.x, self.rect.y-50) #could be replaced
        self.screen.blit(text_surface, text_rect)
    
    def checkIfHasRequests(self):
        if not self.hasPendingQuest:
            self.generateNpcRequests()
            self.hasPendingQuest = True
        self.showRequest()
    
    def questIsCompleted(self):
        self.hasPendingRequest = False
        self.checkIfHasRequests()
    
    def showBubbles(self):
        chatRect = pygame.rect.Rect(self.rect.x + 25, self.rect.y - 55, 50, 50)
        chat_img_surface = pygame.image.load(self.chatImg).convert_alpha()
        self.screen.blit(pygame.transform.scale(chat_img_surface, (50, 50)), chatRect)
        text_surface = self.font.render("...", True, self.BLACK)
        text_rect = text_surface.get_rect()
        pygame.transform.scale(text_surface, (100, 100))
        text_rect.topleft = (self.rect.x+42, self.rect.y - 43)
        self.screen.blit(text_surface, text_rect)


    def showRequest(self):
        requestRect = pygame.rect.Rect(self.rect.x - 25, self.rect.y - 35, 150, 35)
        request_img_surface = pygame.image.load(self.requestImg).convert_alpha()
        self.screen.blit(pygame.transform.scale(request_img_surface, (150, 35)), requestRect)
        text_surface = self.font.render(self.npcVoice, True, self.BLACK)
        text_rect = text_surface.get_rect()
        pygame.transform.scale(text_surface, (100, 100))
        text_rect.topleft = (self.rect.x - 10, self.rect.y - 25)
        self.screen.blit(text_surface, text_rect)
        
    def generateNpcRequests(self):
        numberToRequest = 0
        mins = (pygame.time.get_ticks() - self.firstSpawn)/60000 

        if mins <= 2:
            numberToRequest = 1
        elif mins <= 4:
            numberToRequest = 2
        else:
            numberToRequest = 3

        typeOfMedicine = random.randint(0, 2)
        self.npcVoice = str(numberToRequest) + " " + self.medicines[typeOfMedicine]
        self.numOfMedicine = numberToRequest
        self.typeOfMedicine = self.medicines[typeOfMedicine]

    def npcMovement(self):
        if self.direction:
            #move x
            if not(self.rect.x == self.startLocationX):
                self.rect.x += self.x_directional
            else:
                self.x_directional = -1 * self.x_directional
                self.startLocationX = self.startLocationX+ (100 * self.x_directional)
                self.direction = False
        else:
            #move y
            if not(self.rect.y == self.startLocationY):
                self.rect.y += 1 * self.y_directional
            else:
                self.y_directional =  -1* self.y_directional
                self.startLocationY = self.startLocationY+ (100 * self.y_directional)
                self.direction = True