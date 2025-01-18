import pygame
import sys,random,os,json
pygame.init()

SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
DEFAULT_WINDOW_WIDTH = 1280//2
DEFAULT_WINDOW_HEIGHT = 720//2
SNAKE_SIZE = (20,20)
FPS = 5

BLACK = 'black'
BLUE = 'blue'
WHITE = 'white'
GREEN = 'green'
YELLOW = 'yellow'

class Main(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.fps = FPS
        self.clock = pygame.time.Clock()
        self.fullscreen = False
        self.window_width = DEFAULT_WINDOW_WIDTH
        self.window_height = DEFAULT_WINDOW_HEIGHT
        self.last_size = (self.window_width,self.window_height)
        self.window_width_center = self.window_width // 2
        self.window_height_center = self.window_height // 2
        self.surface = pygame.display.set_mode((self.window_width,self.window_height),pygame.WINDOWMAXIMIZED)
        pygame.display.set_caption('Snake')
        self.font_title = pygame.font.Font('fonts/arcadeclassic.ttf',80)
        self.font_title_outline = pygame.font.Font('fonts/arcadeclassic.ttf',86)
        self.font_score = pygame.font.Font('fonts/arcadeclassic.ttf',40)
        self.running = True
        

    def run(self):
        self.randsnake = RandSnake()
        self.scoreboard = ScoreBoard()
        self.scoreboard.load()
        while self.running:
            self.events()
            self.screen()
            
            pygame.display.update()
            self.clock.tick(self.fps)
        self.scoreboard.save()
        pygame.quit()
        sys.exit()

    def screen(self):
        self.surface.fill(BLUE)
        self.randsnake.run(self.window_width,self.window_height)
        self.render_text('SNAKE',self.font_title_outline,BLACK,'CENTER',(self.window_width_center,100))
        self.render_text('SNAKE',self.font_title,GREEN,'CENTER',(self.window_width_center,100))
        self.scoreboard.show(self.window_width_center)
        self.render_text('Press   P   to   play',self.font_score,YELLOW,'CENTER',(self.window_width_center,self.window_height - 180))
        self.render_text('Press   K   to   define   keys',self.font_score,YELLOW,'CENTER',(self.window_width_center,self.window_height - 140))
        self.render_text('Press   F   to   toggle   full   screen',self.font_score,YELLOW,'CENTER',(self.window_width_center,self.window_height - 100))
        self.render_text('Press   Q   to   quit',self.font_score,YELLOW,'CENTER',(self.window_width_center,self.window_height - 60))

    def render_text(self,text,font,color,position,coord):
        text = font.render(text,True,color)
        text_rect = text.get_rect()
        if position == 'CENTER':
            text_rect.center = coord
        elif position == 'TOPLEFT':
            text_rect.topleft = coord
        self.surface.blit(text,text_rect)

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.fullscreen = False
            if pygame.display.is_fullscreen() == True:
                pygame.display.toggle_fullscreen()
            self.update_video()
        else:
            self.fullscreen = True
            if pygame.display.is_fullscreen() == False:
                pygame.display.toggle_fullscreen()
            self.update_video()

    def update_video(self, width = 0, height = 0):
        if width > 0:
            if width < DEFAULT_WINDOW_WIDTH or height < DEFAULT_WINDOW_HEIGHT:
                self.window_width = DEFAULT_WINDOW_WIDTH
                self.window_height = DEFAULT_WINDOW_HEIGHT 
            else:
                self.window_width = width
                self.window_height = height
            self.last_size = (self.window_width,self.window_height)
        if self.fullscreen:
            self.window_width = SCREEN_WIDTH
            self.window_height = SCREEN_HEIGHT
            self.surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.FULLSCREEN)
        else:
            (self.window_width,self.window_height) = self.last_size
            self.surface = pygame.display.set_mode(self.last_size,pygame.RESIZABLE)
        pygame.display.update()
        self.window_width_center = self.window_width//2
        self.window_height_center = self.window_height//2
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.VIDEORESIZE:
                if not self.fullscreen:
                    self.update_video(event.w,event.h)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.game = Game(self.surface,self.fullscreen)
                    self.game.run()
                if event.key == pygame.K_k:
                    keys = Keys()
                    keys.run()
                if event.key == pygame.K_q:
                    self.running = False
                if event.key == pygame.K_f:
                    self.toggle_fullscreen()

class ScoreBoard(Main):
    def __init__(self):
        super().__init__()
        self.score_array = []
    
    def show(self,width_center):
        x_user = width_center - 170
        x_score = width_center + 40
        y_score = 150
        for [user,score] in self.score_array:
            self.render_text(user,self.font_score,GREEN,'TOPLEFT',(x_user,y_score))
            self.render_text(str(score),self.font_score,YELLOW,'TOPLEFT',(x_score,y_score))
            y_score += 60

    def load(self):
        if os.path.isfile('data/score'):
            with open('data/score', 'r') as file:
                self.score_array = json.load(file)
                self.score_array = sorted(self.score_array,key=lambda x:x[1],reverse=True)

    def save(self):
        with open('data/score','w') as outfile:
            json.dump(self.score_array,outfile)
            outfile.close()
    
class RandSnake(Main):
    def __init__(self):
        super().__init__()
        self.memory = []
        self.first_run = True
        self.x = self.window_width_center
        self.y = self.window_height_center
        self.count = 0
        self.direction = 'RIGHT'
        self.collision = ''
        self.color = WHITE
    
    def run(self,window_width,window_height):
        window_width_center = window_width//2
        window_height_center = window_height//2
        if self.first_run:
            for snake in range(20):
                self.x = window_width_center - (20*snake)
                self.y = window_height_center
                pygame.draw.rect(self.surface,self.color,((self.x,self.y),SNAKE_SIZE))
                self.memory.append((self.x,self.y))
            self.first_run = False
        else:
            for snake in range(20):
                if snake==0:
                    (self.x,self.y) = self.memory[snake]
                    idx = random.randint(0,1)
                    if self.count == 0:
                        self.count = random.randint(1,20)
                        if self.direction in ['LEFT','RIGHT']:
                                self.direction = ['UP','DOWN'][idx]
                        else:
                            self.direction = ['LEFT','RIGHT'][idx]
                        
                    if self.collision !='':
                        self.direction = self.collision
                        self.collision = ''
                    else:
                        if self.x < 40:
                            self.collision = 'RIGHT'
                            if self.y < window_height_center:
                                self.direction = 'DOWN'
                            else:
                                self.direction = 'UP'
                        if self.x > window_width - 40:
                            self.collision = 'LEFT'
                            if self.y < window_height_center:
                                self.direction = 'DOWN'
                            else:
                                self.direction = 'UP'
                        if self.y < 40:
                            self.collision = 'DOWN'
                            if self.x < window_width_center:
                                self.direction = 'RIGHT'
                            else:
                                self.direction = 'LEFT'
                        if self.y > window_height - 40:
                            self.collision = 'UP'
                            if self.x < window_width_center:
                                self.direction = 'RIGHT'
                            else:
                                self.direction = 'LEFT'

                    for idx in range(len(self.memory)-1,-1,-1):
                        self.memory[idx] = self.memory[idx-1]

                    match self.direction:
                        case 'LEFT':
                            self.x-=20
                        case 'RIGHT':
                            self.x+=20
                        case 'UP':
                            self.y-=20
                        case 'DOWN':
                            self.y+=20
                    self.count-=1
                    pygame.draw.rect(self.surface,self.color,((self.x,self.y),SNAKE_SIZE))
                    self.memory[snake] = (self.x,self.y)
                else:
                    (self.x,self.y) = self.memory[snake]
                    pygame.draw.rect(self.surface,self.color,((self.x,self.y),SNAKE_SIZE))

class Keys(Main):
    def __init__(self):
        pass

    def run(self):
        print('Keys Screen')

class Game(Main):
    def __init__(self,surface,fullscreen):
        super().__init__()
        self.gameon = True
        self.snake_size = 20
        self.surface = surface
        self.fullscreen = fullscreen
        self.window_width = pygame.display.Info().current_w
        self.window_height = pygame.display.Info().current_h
        self.window_width_center = self.window_width//2
        self.window_height_center = self.window_height//2


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameon = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pass
                if event.key == pygame.K_DOWN:
                    pass
                if event.key == pygame.K_LEFT:
                    pass
                if event.key == pygame.K_RIGHT:
                    pass
                if event.key == pygame.K_q:
                    self.gameon = False
    
    def screen(self):
        self.surface.fill(BLUE)
        if self.fullscreen:
            self.board = pygame.draw.rect(self.surface,YELLOW,((self.window_width_center - 620,self.window_height_center - 300),(1240,600)),1)
        else:
            self.board = pygame.draw.rect(self.surface,YELLOW,((20,100),(self.window_width-40,self.window_height-120)),1)

    
    def run(self):
        while self.gameon:
            self.screen()
            self.events()
            pygame.display.flip()


if __name__== '__main__':
    main = Main()
    main.run()

  