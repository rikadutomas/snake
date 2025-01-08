import pygame,sys,random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_WIDTH_CENTER = WINDOW_WIDTH//2
WINDOW_HEIGHT_CENTER = WINDOW_HEIGHT//2
SNAKE_SIZE = (20,20)
FPS = 5

BLUE = 'blue'
WHITE = 'white'
GREEN = 'green'
RED = 'red'
MAGENTA = 'magenta'

class Main:
    def __init__(self):
        self.fps = FPS
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Snake')
        self.font_title = pygame.font.Font('arcadeclassic.ttf',80)
        self.running = True

    def run(self):
        self.randsnake = RandSnake()
        while self.running:
            self.screen()
            self.events()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def screen(self):
        self.surface.fill(BLUE)
        self.randsnake.run()
        # self.render_text('SNAKE',self.font_title,GREEN,'CENTER',(WINDOW_WIDTH_CENTER,100))


    def render_text(self,text,font,color,position,coord):
        text = font.render(text,True,color)
        text_rect = text.get_rect()
        if position == 'CENTER':
            text_rect.center = coord
        elif position == 'TOPLEFT':
            text_rect.topleft = coord
        self.surface.blit(text,text_rect)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game = Game()
                    game.run()
                if event.key == pygame.K_k:
                    keys = Keys()
                    keys.run()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


class RandSnake(Main):
    def __init__(self):
        super().__init__()
        self.memory = []
        self.first_run = True
        self.x = WINDOW_WIDTH_CENTER
        self.y = WINDOW_HEIGHT_CENTER
        self.count = 0
        self.direction = 'RIGHT'
        self.collision = ''
    
    def run(self):
        if self.first_run:
            for snake in range(20):
                self.x = WINDOW_WIDTH_CENTER - (20*snake)
                self.y = WINDOW_HEIGHT_CENTER
                pygame.draw.rect(self.surface,WHITE,((self.x,self.y),SNAKE_SIZE))
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
                            if self.y < WINDOW_HEIGHT_CENTER:
                                self.direction = 'DOWN'
                            else:
                                self.direction = 'UP'
                        if self.x > WINDOW_WIDTH - 40:
                            self.collision = 'LEFT'
                            if self.y < WINDOW_HEIGHT_CENTER:
                                self.direction = 'DOWN'
                            else:
                                self.direction = 'UP'
                        if self.y < 40:
                            self.collision = 'DOWN'
                            if self.x < WINDOW_WIDTH_CENTER:
                                self.direction = 'RIGHT'
                            else:
                                self.direction = 'LEFT'
                        if self.y > WINDOW_HEIGHT - 40:
                            self.collision = 'UP'
                            if self.x < WINDOW_WIDTH_CENTER:
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
                    pygame.draw.rect(self.surface,WHITE,((self.x,self.y),SNAKE_SIZE))
                    self.memory[snake] = (self.x,self.y)

                else:
                    (self.x,self.y) = self.memory[snake]
                    pygame.draw.rect(self.surface,WHITE,((self.x,self.y),SNAKE_SIZE))

class Keys(Main):
    def __init__(self):
        pass

    def run(self):
        print('Keys Screen')


class Game(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

    def run(self):
        print('Im Running Game')  

if __name__== '__main__':
    pygame.init()
    main = Main()
    main.run()

  