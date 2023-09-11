import pygame

class Shape:
    def drawRect(self, screen, x, y, w, h, color):    
        self.rect = pygame.rect.Rect(x, y, w, h)
        pygame.draw.rect(screen, color, self.rect)

    def drawCircle(self, screen, color, pos, d):    
        pygame.draw.circle(screen, color, pos, 10)