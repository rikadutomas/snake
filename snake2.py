import pygame,sys,random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 10

BLUE = 'blue'
WHITE = 'white'
GREEN = 'green'
RED = 'red'
MAGENTA = 'magenta'

class Game:
    def __init__(self):
        pygame.display.set_caption('Snake 2')
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.screen.fill(BLUE)
        self.clock = pygame.time.Clock()
        self.fps = FPS
        self.running = True
        pygame.draw.rect(self.screen,WHITE,(0,0,WINDOW_WIDTH,WINDOW_HEIGHT),1)
        self.board = pygame.draw.rect(self.screen,WHITE,(10,100,WINDOW_WIDTH-20,WINDOW_HEIGHT - 120),1)
        self.board_center = self.board.center
        self.snake_group = pygame.sprite.Group()
        self.direction = 'RIGHT'
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.direction = 'UP'
                if event.key == pygame.K_DOWN:
                    self.direction = 'DOWN'
                if event.key == pygame.K_LEFT:
                    self.direction = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    self.direction = 'RIGHT'
        

    def run(self):
        snake = Snake(self)
        self.snake_group.add(snake)
        while self.running:
            self.events()
            self.snake_group.update(self.direction)
            pygame.display.flip()
            self.clock.tick(self.fps)
            
class Snake(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.x = 640
        self.y = 400
        self.snake = pygame.draw.rect(game.screen,WHITE,((self.x,self.y),(20,20)))
    
    def update(self,direction):
        match direction:
            case 'LEFT':
                self.x -= 20
            case 'RIGHT':
                print('match RIGHT')
                self.x += 20
            case 'UP':
                self.y -= 20
            case 'DOWN':
                self.y += 20
            case _:
                print('No MATCH')
        
        pygame.draw.rect(game.screen,WHITE,((self.x,self.y),(20,20)))


class Person(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.person = pygame.image.load('person2.png')



if __name__=='__main__':
    game = Game()  
    game.run()

 