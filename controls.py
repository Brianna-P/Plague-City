from state import State
from rect import Shape
import pygame

class Controls(State):
    def __init__(self, game):

        #Initial setup
        State.__init__(self, game)
        self.game = game
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = game.SCREEN_WIDTH, game.SCREEN_HEIGHT

        #Graphics
        self.background = pygame.image.load("title.xcf")
        self.font = pygame.font.SysFont(None, 30)
        self.BLACK = (0, 0, 0)

        #Controls information
        self.possibleMoves = ["Q - Harvest Plant/Kill Enemy", "W - Open market/Show Brewing Station (in close proximity)", "E - Display Inventory", "R - Take Potion"]
        self.welcomeMsg = ["Welcome to Plague City! The rats are spreading disease and you,", "the Doctor, must save the townspeople by fulfilling their medicinal requests.", "Beware of rat bites!", "Find ingredients at the City Outskirts and at Bants' Market,", "and brew medicine at the cauldron.", "Good luck, Plague Doctor!", " "]

    def render(self, display):
        display.fill((211,211,211))
        pygame.display.set_caption("CONTROLS")
        self.game.screen.blit(pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0, 0))
        self.backButton()
        mousePos = pygame.mouse.get_pos()
        Shape.drawCircle(Shape, self.game.screen, (211, 211, 211), mousePos, 10)
        self.renderControls()
        
    def renderControls(self):
        cobbleRect = pygame.rect.Rect(self.SCREEN_WIDTH/2 -400, self.SCREEN_HEIGHT/2 -310, 800, 620)
        cobble_img_surface = pygame.image.load("cobbleAndBlack.xcf").convert_alpha()
        self.game.screen.blit(pygame.transform.scale(cobble_img_surface, (800, 620)), cobbleRect)

        increment = 100
        for x in range(len(self.welcomeMsg)):
            if x == 2 or x == 5:
                intro_surface = self.font.render(self.welcomeMsg[x], True, (139,0,0))
                Shape.drawRect(Shape, self.game.screen, self.SCREEN_WIDTH/2 - 400/2, increment - 50/2, 400, 50, (0,0,0))
            else: 
                intro_surface = self.font.render(self.welcomeMsg[x], True, (255,255,255))
            intro_rect = intro_surface.get_rect()
            intro_rect.center = (self.SCREEN_WIDTH/2, increment)
            self.game.screen.blit(intro_surface, intro_rect)
            increment += 50

        for x in range(len(self.possibleMoves)):
            text_surface = self.font.render(self.possibleMoves[x], True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.center = (self.SCREEN_WIDTH/2, increment)
            self.game.screen.blit(text_surface, text_rect)
            increment += 50

    def update(self, actions):
        if actions["back"]:
            self.game.state_stack.pop()
      
    def backButton(self):
        buttonRect = pygame.rect.Rect(0,  0, 200, 100)
        button_img_surface = pygame.image.load("woodButton.xcf").convert_alpha()
        self.game.screen.blit(pygame.transform.scale(button_img_surface, (200, 100)), buttonRect)
        text_surface = self.font.render("BACK", True, (0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.center = (100, 50)
        self.game.screen.blit(text_surface, text_rect)