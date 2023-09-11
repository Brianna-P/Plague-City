from state import State
from rect import Shape
from rect import Shape
import pygame

class Title(State):
    def __init__(self, game):

        #Initial setup
        State.__init__(self, game)
        self.game = game
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = game.SCREEN_WIDTH, game.SCREEN_HEIGHT

        #Graphics
        self.background = pygame.image.load("title.xcf")
        self.startImg = "Start.xcf"
        self.creditsImg = "Credits.xcf"
        self.controlsImg = "Controls.xcf"
        self.quitImg = "Quit.xcf"
        
        #Button set up
        self.font = pygame.font.SysFont(None, 30)
        self.BLACK = (0, 0, 0)

    def update(self, actions):
        if actions["quit"]:
            self.game.playing = False
            self.game.running = False
        if actions["started"]:
            self.game.mainScreen.enter_state()
        if actions["credits"]:
            self.game.creditsScreen.enter_state()
        if actions["controls"]:
            self.game.controlsScreen.enter_state()
        
    def render(self, display):
        display.fill((211,211,211))
        pygame.display.set_caption("PLAGUE CITY")
        display.blit(pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0, 0))

        #Start button
        img_surface = pygame.image.load(self.startImg).convert_alpha()
        rectum = pygame.rect.Rect(self.game.SCREEN_WIDTH/2 - 300/2, 240 - 90/2, 300, 90)
        display.blit(pygame.transform.scale(img_surface, (300, 90)), rectum)

        #Credits button
        img_surface = pygame.image.load(self.creditsImg).convert_alpha()
        rectum = pygame.rect.Rect(self.game.SCREEN_WIDTH/2 - 300/2, 480 - 90/2, 300, 90)
        display.blit(pygame.transform.scale(img_surface, (300, 90)), rectum)

        #Quit button
        img_surface = pygame.image.load(self.quitImg).convert_alpha()
        rectum = pygame.rect.Rect(self.game.SCREEN_WIDTH/2 - 300/2, 360 - 90/2, 300, 90)
        display.blit(pygame.transform.scale(img_surface, (300, 90)), rectum)

        #Controls button
        img_surface = pygame.image.load(self.controlsImg).convert_alpha()
        rectum = pygame.rect.Rect(self.game.SCREEN_WIDTH/2 - 300/2, 600 - 90/2, 300, 90)
        display.blit(pygame.transform.scale(img_surface, (300, 90)), rectum)
    
        mousePos = pygame.mouse.get_pos()
        Shape.drawCircle(Shape, self.game.screen, (211, 211, 211), mousePos, 10)
        
    def makeButton(self, screen, font, text, color, x, y):
        Shape.drawRect(Shape, screen, x - 300/2, y - 90/2, 300, 90, (175,175,175))
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        screen.blit(text_surface, text_rect)