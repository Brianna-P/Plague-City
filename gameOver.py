from state import State
import pygame

class gameOver(State):
    def __init__(self, game):

        #Initial setup
        State.__init__(self, game)
        self.screen = self.game.screen
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = game.SCREEN_WIDTH, game.SCREEN_HEIGHT
        self.prev_state = None

        #Graphics
        self.background = pygame.image.load("end.xcf")
        self.font = pygame.font.SysFont(None, 30)
        self.BLACK = (0, 0, 0)

    def update(self, actions):
        if actions["ANY"]:
                self.exit_state()
                self.game.state_stack.clear()
                self.game.state_stack.append(self.game.titleScreen)
            
    def render(self, screen):
        screen.fill((211,211,211))
        pygame.display.set_caption("GAME OVER")
        screen.blit(pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0, 0))
        text_surface = self.font.render("GAME OVER! You KILLED the villagers!!! Press any button to continue", True, (0,0,0))
        text_rect = text_surface.get_rect()
        pygame.transform.scale(text_surface, (100, 100))
        text_rect.topleft = (self.SCREEN_WIDTH/2 -400, self.SCREEN_HEIGHT/2 -310)
        self.screen.blit(text_surface, text_rect)

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()