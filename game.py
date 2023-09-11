import pygame
import random
from mainscreen import Main
from title import Title
from farmscreen import FarmScreen                                     
from credits import Credits
from controls import Controls
from gameOver import gameOver

class Game():
    def __init__(self):

            #Initial screen setup
            pygame.init()
            pygame.mixer.init()
            self.gameClock = pygame.time.Clock()
            self.SCREEN_WIDTH,self.SCREEN_HEIGHT = 1280, 720
            self.GAME_W,self.GAME_H = 480, 270
            self.game_canvas = pygame.Surface((self.GAME_W,self.GAME_H))
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))

            #Graphics
            self.background = pygame.image.load("BACKGROUND.xcf")
            
            #Different states
            self.mainScreen = Main(self)
            self.farmScreen = FarmScreen(self)
            self.creditsScreen = Credits(self)
            self.controlsScreen = Controls(self)
            self.gameOverScreen = gameOver(self)
            self.titleScreen = Title(self)

            #Game logic variables
            self.running, self.playing = True, True
            self.actions = {"any": False, "e": False, "back": False, "escape": False, "w": False, "quit": False, "tab": False,"credits": False, "started": False, "left": False, "right": False, "up" : False, "down" : False, "action1" : False, "action2" : False, "start" : False, "q" : False, "controls" : False, "r" : False, "t": False}
            self.state_stack = []
            self.game_is_over = False

            #Music control
            self.songList = ["driftveil-city.mp3", "GreenGreens.mp3", "KirbyTheme.mp3", "GerudoValley.mp3"]
            self.nextUp = self.songList[:]

    def get_events(self):
        x, y = pygame.mouse.get_pos()            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(abs(x - self.SCREEN_WIDTH/2) <= 150 and abs(y- 360) <= 45):
                    self.actions["quit"] = True
                if(abs(x - self.SCREEN_WIDTH/2) <= 150 and abs(y- 240) <= 45):
                    self.actions['started'] = True 
                if(abs(x - self.SCREEN_WIDTH/2) <= 150 and abs(y- 480) <= 45):
                    self.actions['credits'] = True
                if(abs(x - 100) <= 100 and abs(y- 50) <= 50):
                    self.actions['back'] = True  
                if(abs(x - self.SCREEN_WIDTH/2) <= 150 and abs(y- 600) <= 45):
                    self.actions['controls'] = True   
            if event.type == pygame.KEYDOWN:
                self.actions["ANY"] = True
                if event.key == pygame.K_ESCAPE:
                    self.actions["escape"] = True
                if event.key == pygame.K_a:
                    self.actions['left'] = True
                if event.key == pygame.K_q:
                    self.actions["q"] = True
                if event.key == pygame.K_t:
                    self.actions["t"] = True
                if event.key == pygame.K_d:
                    self.actions['right'] = True
                if event.key == pygame.K_s:
                    self.actions['down'] = True
                if event.key == pygame.K_p:
                    self.actions['action1'] = True
                if event.key == pygame.K_o:
                    self.actions['action2'] = True    
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = True  
            if event.type == pygame.MOUSEBUTTONUP:
                self.actions["quit"] = False
                self.actions['started'] = False
                self.actions['credits'] = False
                self.actions['back'] = False
                self.actions['controls'] = False
            if event.type == pygame.KEYUP:
                self.actions["ANY"] = False
                if event.key == pygame.K_e:
                    self.actions['e'] = True
                if event.key == pygame.K_r:
                    self.actions['r'] = True
                if event.key == pygame.K_t:
                    self.actions['t'] = False
                if event.key == pygame.K_a:
                    self.actions['left'] = False
                if event.key == pygame.K_d:
                    self.actions['right'] = False
                if event.key == pygame.K_w:
                    self.actions['up'] = False
                if event.key == pygame.K_s:
                    self.actions['down'] = False
                if event.key == pygame.K_p:
                    self.actions['action1'] = False
                if event.key == pygame.K_q:
                    self.actions["q"] = False   
                if event.key == pygame.K_w:
                    self.actions["w"]  = True
                if event.key == pygame.K_o:
                    self.actions['action2'] = False
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = False  

    def update(self):
        self.state_stack[-1].update(self.actions)

    def render(self):
        self.state_stack[-1].render(self.screen)
        self.gameClock.tick(60)
        pygame.display.flip()

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

    def playMusic(self):
        if len(self.nextUp) <= 0:
            self.nextUp = self.songList[:]
        try:
            songToPlay = songToPlay = random.randint(0, len(self.nextUp)-1)
        except:
            songToPlay = 0
        pygame.mixer.music.load(self.nextUp[songToPlay])
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.3)
        self.nextUp.pop(songToPlay)
    def game_loop(self):
        while self.playing:
            self.get_events()
            self.update()
            self.render()
            self.farmScreen.runFarm()
            if not pygame.mixer.music.get_busy() and self.state_stack[-1] != self.farmScreen:
                self.playMusic()
            if self.game_is_over:
                self.mainScreen = Main(self)
                self.farmScreen = FarmScreen(self)
                self.game_is_over = False

g = Game()
c = Credits(g)
g.state_stack.append(g.titleScreen)
while g.running:
    g.game_loop()