import pygame,sys,random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
SNAKE_SIZE = 20
FPS = 5

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
        self.board = (11,101,WINDOW_WIDTH-22,WINDOW_HEIGHT - 122)
        # pygame.draw.rect(self.screen,WHITE,(0,0,WINDOW_WIDTH,WINDOW_HEIGHT),1)
        pygame.draw.rect(self.screen,WHITE,(10,100,WINDOW_WIDTH-20,WINDOW_HEIGHT-120),1)
        self.snake_group = pygame.sprite.Group()
        self.person_group = pygame.sprite.Group()
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
        self.person = Person(self)
        self.snake_group.add(snake)
        # self.person_group.add(person)
        
        while self.running:
            self.screen.fill(BLUE,self.board,0)
            self.events()
            self.snake_group.update(self.direction)
            self.person_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
            
class Snake(pygame.sprite.Sprite):
    def __init__(self,game,x=640,y=400):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.draw.rect(game.screen,WHITE,((self.x,self.y),(SNAKE_SIZE,SNAKE_SIZE)))
        
    def move(self,direction):
        match direction:
            case 'LEFT':
                self.x -= 20
            case 'RIGHT':
                self.x += 20
            case 'UP':
                self.y -= 20
            case 'DOWN':
                self.y += 20
            case _:
                print('No MATCH')
        
        self.rect.move_ip(self.x,self.y)
        self.rect = pygame.draw.rect(game.screen,WHITE,((self.x,self.y),(SNAKE_SIZE,SNAKE_SIZE)))
    
    def check_collisions(self):
        if pygame.sprite.spritecollide(self,game.person_group,True):
            game.screen.fill(BLUE,(game.person.x,game.person.y,20,20),0)
            game.person = Person(game)
            
            
        
    def update(self,direction):
        self.move(direction)
        self.check_collisions()
        

class Person(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.image = pygame.image.load('person2.png')
        self.rect = self.image.get_rect()
        self.x = random.randint(20,WINDOW_WIDTH - 40)
        self.y = random.randint(100,WINDOW_HEIGHT-40)
        self.rect.topleft = (self.x,self.y)
        game.person_group.add(self)

if __name__=='__main__':
    game = Game()  
    game.run()

 