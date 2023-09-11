from state import State
from rect import Shape
import pygame

class Credits(State):
    def __init__(self, game):

        #Initial setup
        State.__init__(self, game)
        self.game = game
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = game.SCREEN_WIDTH, game.SCREEN_HEIGHT

        #Graphics
        self.background = pygame.image.load("title.xcf")
        self.font = pygame.font.SysFont(None, 30)
        self.BLACK = (0, 0, 0)
        self.creditsMessages = ["We hope you enjoyed our first game,", "Thank you for playing!!", "Created by: Brianna Patten and Harivansh Luchmun"]

        #Button information
        self.buttonLabels = ["PATTEN AND HARBAN", "BACK" ]
        self.buttonLocations = [[self.SCREEN_HEIGHT/2 - self.SCREEN_HEIGHT/6, 300, 240], [self.SCREEN_HEIGHT/2 + self.SCREEN_HEIGHT/6, 300, 480]]
        self.buttonHeight = 90

    def render(self, display):
        display.fill((211,211,211))
        pygame.display.set_caption("CREDITS")
        display.blit(pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0, 0))
        mousePos = pygame.mouse.get_pos()
        Shape.drawCircle(Shape, self.game.screen, (211, 211, 211), mousePos, 10)
        self.backButton()
        cobbleRect = pygame.rect.Rect(self.SCREEN_WIDTH/2 -400, self.SCREEN_HEIGHT/2 -310, 800, 620)
        cobble_img_surface = pygame.image.load("cobble.xcf").convert_alpha()
        self.game.screen.blit(pygame.transform.scale(cobble_img_surface, (800, 620)), cobbleRect)
        increment = self.SCREEN_HEIGHT / 3
        for x in range(len(self.creditsMessages)):
            text_surface = self.font.render(self.creditsMessages[x], True, (0,0,0))
            text_rect = text_surface.get_rect()
            text_rect.center = (self.SCREEN_WIDTH/2, increment)
            self.game.screen.blit(text_surface, text_rect)
            increment += 100
        
    def update(self, actions):
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(abs(x - self.SCREEN_WIDTH/2) <= 150 and abs(y- self.buttonLocations[1][2]) <= 45):
                    self.game.exit_state()
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
