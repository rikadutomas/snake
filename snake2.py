import pygame,sys,random,json,os

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
        self.data = {}
        pygame.display.set_caption('Snake 2')
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.screen.fill(BLUE)
        self.clock = pygame.time.Clock()
        self.fps = FPS
        self.fps_paused = 0
        self.running = True
        self.board = (21,101,WINDOW_WIDTH-42,WINDOW_HEIGHT - 122)
        self.snake_group = pygame.sprite.Group()
        self.person_group = pygame.sprite.Group()
        self.direction = 'RIGHT'
        self.snake_array = []
        self.prev_x = 0
        self.prev_y = 0
        self.font_score = pygame.font.Font('arcadeclassic.ttf',20)
        self.font_arcade = pygame.font.Font('arcadeclassic.ttf',80)
        self.font_arcade_small = pygame.font.Font('arcadeclassic.ttf',40)

        self.sound_game_over = pygame.mixer.Sound('sounds/game-over.mp3')
        self.music = pygame.mixer.music
        self.music.load('sounds/game_music2.mp3')
        self.music.set_volume(0.4)
        self.music_intro = self.music = pygame.mixer.music
        self.music_intro.load('sounds/game_music.mp3')
        self.music_intro.set_volume(0.4)

        font = self.font_arcade.render('Snake 2',True,GREEN)
        font_rect = font.get_rect()
        font_rect.center = (WINDOW_WIDTH//2,50)
        self.screen.blit(font,font_rect)

        self.count_person = 0
        self.score = 0
        self.level = 1

        self.paused = False
        self.over = False
        
        self.random_counter = 0
        self.init_x = WINDOW_WIDTH/2
        self.init_y = WINDOW_HEIGHT/2
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction in ['LEFT','RIGHT']:
                    self.direction = 'UP'
                if event.key == pygame.K_DOWN and self.direction in ['LEFT','RIGHT']:
                    self.direction = 'DOWN'
                if event.key == pygame.K_LEFT and self.direction in ['UP','DOWN']:
                    self.direction = 'LEFT'
                if event.key == pygame.K_RIGHT and self.direction in ['UP','DOWN']:
                    self.direction = 'RIGHT'
                if event.key == pygame.K_g:
                    self.game_over()
                if event.key == pygame.K_ESCAPE:
                    if self.paused == False:
                        self.music.pause()
                        self.game_paused()
                    else:
                        self.music.unpause()
                        self.paused = False
    
    def intro_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.music_intro.stop()
                    self.run()

    def move_snakes(self):
        for idx,snake in enumerate(self.snake_array):
            if idx == 0:
                (x,y) = snake.position()
                self.prev_x = x
                self.prev_y = y
                match self.direction:
                    case 'LEFT':
                        x -= 20
                    case 'RIGHT':
                        x += 20
                    case 'UP':
                        y -= 20
                    case 'DOWN':
                        y += 20
                snake.move(x,y)
            else:
                x = self.prev_x
                y = self.prev_y
                (self.prev_x,self.prev_y) = snake.position()
                snake.move(x,y)
        
    def game_over(self,msg=''):
        self.over = True
        font = self.font_arcade.render('GAME OVER',True,GREEN)
        font_rect = font.get_rect()
        font_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)
        self.screen.blit(font,font_rect)
        
        if msg:
            font = self.font_arcade_small.render(msg,True,WHITE)
            font_rect = font.get_rect()
            font_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2 + 100)
            self.screen.blit(font,font_rect)
        
        pygame.display.flip()
        self.music.stop()
        self.sound_game_over.play()

        self.paused = True
        while self.running:
            self.events()

    def game_paused(self):
        font = self.font_arcade.render('PAUSE',True,GREEN)
        font_rect = font.get_rect()
        font_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)
        self.screen.blit(font,font_rect)
        
        pygame.display.flip()
        self.paused = True
        while self.paused:
            self.events()
        
    def update_score(self):
        self.screen.fill(BLUE,(20,70,200,30))
        self.screen.fill(BLUE,(WINDOW_WIDTH-150,70,200,30))

        str_level = 'Level  {}'.format(self.level)
        str_score = 'Score  {}'.format(self.score)

        level = self.font_score.render(str_level,True,WHITE)
        level_rect = level.get_rect()
        level_rect.topleft = (20,70)
        self.screen.blit(level,level_rect)

        level = self.font_score.render(str_score,True,WHITE)
        level_rect = level.get_rect()
        level_rect.topleft = (WINDOW_WIDTH - 150,70)
        self.screen.blit(level,level_rect)

    def high_score(self):
        pass 
    
    def run(self):
        Snake(self)
        self.person = Person(self)
        pygame.draw.rect(self.screen,WHITE,(20,100,WINDOW_WIDTH-40,WINDOW_HEIGHT-120),1)
        self.music.play(-1,0.0) 
        while self.running:
            self.screen.fill(BLUE,self.board,0)
            self.events()
            self.move_snakes()
            self.person_group.draw(self.screen)
            self.update_score()
            pygame.display.flip()
            self.high_score()
            if self.paused:
                self.clock.tick(self.fps_paused)
            else:
                self.clock.tick(self.fps)

    def load_score_to_screen(self):
        row = 150
        quarter = WINDOW_WIDTH/6
        self.data = dict(sorted(self.data.items(), key=lambda x:x[1],reverse=True))
        for (key,value) in self.data.items():
            data = self.font_arcade_small.render(key,True,WHITE)
            data_rect = data.get_rect()
            data_rect.topleft = (quarter*2, row)
            self.screen.blit(data,data_rect)
            
            data = self.font_arcade_small.render(str(value),True,WHITE)
            data_rect = data.get_rect()
            data_rect.topleft = (quarter*3, row)
            self.screen.blit(data,data_rect)
            row += 50


        data = self.font_arcade_small.render('Press    P    to   start   playing',True,GREEN)
        data_rect = data.get_rect()
        data_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT - 100)
        self.screen.blit(data,data_rect)
    
    def run_intro_snake(self):
        if self.random_counter == 0:
            self.random_counter = random.randint(1,10)
            leftright = random.randint(0,1)
            if self.direction in ['LEFT','RIGHT'] :
                self.direction = ['UP','DOWN'][leftright]
            else:
                self.direction = ['LEFT','RIGHT'][leftright]
        print(self.random_counter)
        print(self.direction)
        for count in range(10):
            match self.direction:
                case 'LEFT':
                    self.init_x-=20
                case 'RIGHT':
                    self.init_x+=20
                case 'UP':
                    self.init_y-=20
                case 'DOWN':
                    self.init_y+=20
            if count==0:
                pygame.draw.rect(self.screen,WHITE,(self.init_x,self.init_y,20,20))
            else:
                pass
        self.random_counter-=1

    def load_intro_screen(self):
        self.screen.fill(BLUE,self.board,0)
        self.run_intro_snake()
        self.load_score_to_screen()
         


    def load_score(self):
        if os.path.exists('score'):
            with open('score', 'r') as openfile:
                self.data = json.load(openfile)

    def save_score(self):
        json_object = json.dumps(self.data, indent=4)
        with open('score', 'w') as outfile:
            outfile.write(json_object)
             

    def init(self):
        self.load_score()
        self.music_intro.play(-1,0.0)
        while True:
            
            self.load_intro_screen()
            self.intro_events()
            pygame.display.flip()
        
        self.save_score()
            
class Snake(pygame.sprite.Sprite):
    def __init__(self,game,x=640,y=400):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.draw.rect(game.screen,WHITE,((self.x,self.y),(SNAKE_SIZE,SNAKE_SIZE)))
        game.snake_group.add(self)
        game.snake_array.append(self)
        self.sound_person = pygame.mixer.Sound('sounds/get_person.mp3')
        self.sound_level = pygame.mixer.Sound('sounds/next_level.mp3')
    
    def move(self,x,y):
        game.screen.fill(BLUE,(self.x,self.y,20,20),0)
        self.x = x
        self.y = y
        self.rect.move_ip(self.x,self.y)
        self.rect = pygame.draw.rect(game.screen,WHITE,((self.x,self.y),(SNAKE_SIZE,SNAKE_SIZE)))
        self.check_collisions()
    
    def check_collisions(self):
        if pygame.sprite.spritecollide(self,game.person_group,True):
            game.screen.fill(BLUE,(game.person.x,game.person.y,20,20),0)
            game.person = Person(game)
            self.sound_person.play()
            Snake(game,game.prev_x,game.prev_y)
            game.count_person += 1
            if game.count_person % 5 == 0:
                game.fps += 1
                game.level += 1
                self.sound_level.play()
            game.score += game.level * game.count_person
            
        if pygame.sprite.spritecollide(self,game.snake_group,False):
            collide_group = pygame.sprite.spritecollide(self,game.snake_group,False)      
            if collide_group[0] != self:
                game.game_over('You have crashed  against  yourself')

        if self.x < 21 or self.x > WINDOW_WIDTH-41 or self.y < 101 or self.y > WINDOW_HEIGHT - 41:
            game.game_over('You  have crashed  against  the  wall')

                   
    def position(self):
        return (self.x,self.y)
        

class Person(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.image = pygame.image.load('person2.png')
        self.rect = self.image.get_rect()
        self.x = random.randint(20,WINDOW_WIDTH - 40)
        self.y = random.randint(100,WINDOW_HEIGHT-40)
        self.rect.topleft = (self.x,self.y)
        game.person_group.add(self)



if __name__== '__main__':
    pygame.init()
    game = Game()
    game.init()


 