import pygame
import sys,random,os,json,math
pygame.init()

SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
DEFAULT_WINDOW_WIDTH = 1280
DEFAULT_WINDOW_HEIGHT = 720
SNAKE_SIZE = 20
SNAKE_TUPLE = (SNAKE_SIZE,SNAKE_SIZE)
FPS = 5

BLACK = 'black'
BLUE = 'blue'
WHITE = 'white'
GREEN = 'green'
YELLOW = 'yellow'

DEFAULT_KEYS = {
     "UP":1073741906,
     "DOWN":1073741905,
     "LEFT":1073741904,
     "RIGHT":1073741903
}

class Main:
    def __init__(self):
        super().__init__()
        self.fps = FPS
        self.clock = pygame.time.Clock()
        self.window_width = DEFAULT_WINDOW_WIDTH
        self.window_height = DEFAULT_WINDOW_HEIGHT
        self.window_width_center = self.window_width // 2
        self.window_height_center = self.window_height // 2
        self.surface = pygame.display.set_mode((DEFAULT_WINDOW_WIDTH,DEFAULT_WINDOW_HEIGHT),pygame.SCALED)
        pygame.display.set_caption('Snake')
        self.font_title = pygame.font.Font('fonts/arcadeclassic.ttf',80)
        self.font_subtitle = pygame.font.Font('fonts/arcadeclassic.ttf',60)
        self.font_title_outline = pygame.font.Font('fonts/arcadeclassic.ttf',86)
        self.font_score = pygame.font.Font('fonts/arcadeclassic.ttf',40)
        self.running = True
        self.fullscreen = False
        self.music = pygame.mixer.music
        self.music.load('sounds/game_music2.mp3')
        self.music.set_volume(0.4)
        self.game_keys = DEFAULT_KEYS
        

    def run(self):
        self.randsnake = RandSnake()
        self.scoreboard = ScoreBoard()
        self.scoreboard.load()
        self.load_keys()
        self.music.play(-1,0.0)
        while self.running:
            self.events()
            self.screen()
            pygame.display.flip()
            self.clock.tick(self.fps)
        self.scoreboard.save()
        pygame.quit()
        sys.exit()

    def load_keys(self):  
        if os.path.isfile('data/config'):
            with open('data/config', 'r') as file:
                try:
                    self.game_keys = json.load(file)
                except:
                    self.game_keys = DEFAULT_KEYS

        print(self.game_keys)
        # return self.game_keys

    def screen(self):
        self.surface.fill(BLUE)
        pygame.draw.rect(self.surface,WHITE,((0,0),(DEFAULT_WINDOW_WIDTH,DEFAULT_WINDOW_HEIGHT)),1)
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
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.VIDEORESIZE:
                pygame.display._resize_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.music.stop()
                    self.game = Game(self.surface,self.fullscreen,self.game_keys)
                    self.game.run()
                    self.scoreboard.check_score(self.game.score)
                    self.scoreboard.save()
                    self.music.play()
                if event.key == pygame.K_k:
                    self.keysboard = Keys()
                    self.game_keys = self.keysboard.run()
                    print(self.game_keys)
                if event.key == pygame.K_q:
                    self.running = False
                if event.key == pygame.K_f:
                    if self.fullscreen == True:
                        self.fullscreen = False 
                    else:
                        self.fullscreen = True
                    pygame.display.toggle_fullscreen()

class ScoreBoard(Main):
    def __init__(self):
        super().__init__()
        self.score_array = []
        self.sound_typing = pygame.mixer.Sound('sounds/typing2.mp3')
    
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

    def check_score(self,score):
        print(self.score_array)
        n_scores = len(self.score_array)
        if not n_scores or n_scores<5:
            self.add_highscore(score)
        else:
            for idx,arr in enumerate(self.score_array):
                if arr[1]<score:
                    self.add_highscore(score,idx)
                    break
        print(self.score_array)     

    def add_highscore(self,score,idx=0):
        name = self.get_name(score)
        print('name ' + name)
        self.score_array.insert(idx,[name,score])
        if len(self.score_array) > 5:
            self.score_array.pop()
        print(self.score_array)
        self.score_array = sorted(self.score_array,key=lambda x:x[1],reverse=True)

    def get_name(self,score):
        self.scoreon = True
        text = []
        while self.scoreon:
            self.surface.fill(BLUE)
            self.render_text('SNAKE',self.font_title_outline,BLACK,'CENTER',(self.window_width_center,100))
            self.render_text('SNAKE',self.font_title,GREEN,'CENTER',(self.window_width_center,100))
            self.render_text('New Score',self.font_title,GREEN,'CENTER',(self.window_width_center,250))
            for event in pygame.event.get():    
                if event.type == pygame.KEYDOWN:
                    self.sound_typing.play()
                    key_alpha = pygame.key.name(event.key)
                    if event.key == pygame.K_RETURN:
                        self.scoreon = False
                    elif event.key == pygame.K_BACKSPACE:
                        if len(text) > 0:
                            text.pop()
                    elif event.key == pygame.K_SPACE:
                        text.append(' ')
                    elif key_alpha.isalnum():
                        if len(text)<8:
                            text.append(key_alpha)                          
                text_str = ''.join(text)
                self.render_text(text_str,self.font_title,YELLOW,'CENTER',(self.window_width_center,400))
                pygame.display.flip()
        return text_str

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
                pygame.draw.rect(self.surface,self.color,((self.x,self.y),SNAKE_TUPLE))
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
                    pygame.draw.rect(self.surface,self.color,((self.x,self.y),SNAKE_TUPLE))
                    self.memory[snake] = (self.x,self.y)
                else:
                    (self.x,self.y) = self.memory[snake]
                    pygame.draw.rect(self.surface,self.color,((self.x,self.y),SNAKE_TUPLE))

class Keys(Main):
    def __init__(self):
        super().__init__()
        self.positions = [250,350,450,550]
        self.keys = ['','','','']
        self.keycode = [0,0,0,0]
        self.count = -1
        self.close_message = ''
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keyson = False
                elif event.key == pygame.K_BACKSPACE:
                    self.keys[self.count] = ''
                    self.keycode[self.count] = 0
                    self.count -= 1
                elif event.key == pygame.K_RETURN:
                    if self.count == 3:
                        self.game_keys = self.save_keys()
                        self.keyson = False
                    else:
                        self.count += 1
                        self.keys[self.count] = pygame.key.name(event.key)
                        self.keycode[self.count] = event.key
                else:
                    self.count += 1
                    self.keys[self.count] = pygame.key.name(event.key)
                    self.keycode[self.count] = event.key        
        if self.count == 3 and self.keyson:
            self.close_message = 'Press Enter to Save or Esc to exit'

    def save_keys(self):
        self.game_keys = {
            "UP":self.keycode[0],
            "DOWN":self.keycode[1],
            "LEFT":self.keycode[2],
            "RIGHT":self.keycode[3]
        }
        print(self.game_keys)
        with open('data/config','w') as outfile:
            json.dump(self.game_keys,outfile)
            outfile.close()
        return self.game_keys

    def screen(self):
        self.surface.fill(BLUE)
        self.render_text('SNAKE',self.font_title_outline,BLACK,'CENTER',(self.window_width_center,100))
        self.render_text('SNAKE',self.font_title,GREEN,'CENTER',(self.window_width_center,100))
        self.render_text('Press the key to select',self.font_score,GREEN,'CENTER',(self.window_width_center,170))
        self.render_text('UP',self.font_score,GREEN,'TOPLEFT',(300,250))
        self.render_text(self.keys[0],self.font_score,YELLOW,'TOPLEFT',(500,250))
        self.render_text('DOWN',self.font_score,GREEN,'TOPLEFT',(300,350))
        self.render_text(self.keys[1],self.font_score,YELLOW,'TOPLEFT',(500,350))
        self.render_text('LEFT',self.font_score,GREEN,'TOPLEFT',(300,450))
        self.render_text(self.keys[2],self.font_score,YELLOW,'TOPLEFT',(500,450))
        self.render_text('RIGHT',self.font_score,GREEN,'TOPLEFT',(300,550))
        self.render_text(self.keys[3],self.font_score,YELLOW,'TOPLEFT',(500,550))
        self.render_text(self.close_message,self.font_score,YELLOW,'CENTER',(self.window_width_center,650))


    def run(self):
        self.keyson = True
        while self.keyson:
            self.events()
            self.screen()
            pygame.display.flip()
        return self.game_keys

class Game(Main):
    def __init__(self,surface,fullscreen,game_keys):
        super().__init__()
        self.fps = FPS
        self.gameon = True
        self.snake_size = SNAKE_SIZE
        self.surface = surface
        self.fullscreen = fullscreen
        self.clock = pygame.time.Clock()
        self.window_width = pygame.display.Info().current_w
        self.window_height = pygame.display.Info().current_h
        self.window_width_center = self.window_width//2
        self.window_height_center = self.window_height//2
        self.x = self.window_width_center
        self.y = self.window_height_center
        self.snake_group = pygame.sprite.Group()
        self.person_group = pygame.sprite.Group()
        self.direction = ['UP','DOWN','LEFT','RIGHT'][random.randint(0,3)]
        self.gameover = False
        self.gamepaused = False
        self.font_score = pygame.font.Font('fonts/arcadeclassic.ttf',20)
        self.music = pygame.mixer.music
        self.music.load('sounds/game_music.mp3')
        self.music.set_volume(0.4)
        self.sound_game_over = pygame.mixer.Sound('sounds/game-over.mp3')
        self.sound_get_person = pygame.mixer.Sound('sounds/get_person.mp3')
        self.sound_next_level = pygame.mixer.Sound('sounds/next_level.mp3')
        self.level = 1
        self.score = 0
        self.count_person = 1
        self.game_keys = game_keys

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameon = False
            if event.type == pygame.KEYDOWN:
                if self.gameover:
                    if event.key == pygame.K_RETURN:
                        self.gameon = False
                elif self.gamepaused:
                    if event.key == pygame.K_ESCAPE:
                        self.gamepaused = False
                    if event.key == pygame.K_q:
                        self.gamepaused = False
                        self.gameon = False
                else:
                    if event.key == pygame.K_ESCAPE:
                        self.game_paused()
                    if self.direction in ['LEFT','RIGHT']:
                        if event.key == self.game_keys['UP']:
                            self.direction = 'UP'
                        if event.key == self.game_keys['DOWN']:
                            self.direction = 'DOWN'
                    if self.direction in ['UP','DOWN']:
                        if event.key == self.game_keys['LEFT']:
                            self.direction = 'LEFT'
                        if event.key == self.game_keys['RIGHT']:
                            self.direction = 'RIGHT'
                    
    def screen(self):
        self.surface.fill(BLUE)
        self.board = pygame.draw.rect(self.surface,YELLOW,((20,100),(DEFAULT_WINDOW_WIDTH-40,DEFAULT_WINDOW_HEIGHT-120)),1)
        self.render_text('SNAKE',self.font_title_outline,BLACK,'CENTER',(self.window_width_center,60))
        self.render_text('SNAKE',self.font_title,GREEN,'CENTER',(self.window_width_center,60))

    def move_snake(self):
        # print((self.x,self.y))
        match self.direction:
            case 'UP':
                self.y -= SNAKE_SIZE
            case 'DOWN':
                self.y += SNAKE_SIZE
            case 'LEFT':
                self.x -= SNAKE_SIZE
            case 'RIGHT':
                self.x += SNAKE_SIZE

        self.person_group.update()
        self.person_group.draw(self.surface)
        for idx,snake in enumerate(self.snake_group):
            if idx == 0:
                previous_x = snake.x
                previous_y = snake.y
                snake.update(self.x,self.y)
            else:
                x = previous_x
                y = previous_y
                previous_x = snake.x
                previous_y = snake.y
                snake.update(x,y)
        self.snake_group.draw(self.surface)

    def check_collisions(self):
        for snake in self.snake_group:
            if pygame.sprite.spritecollide(snake,self.person_group,True):
                new_person = Person()
                self.person_group.add(new_person)
                new_snake = Snake(self.x,self.y)
                self.snake_group.add(new_snake)
                self.sound_get_person.play()
                self.count_person += 1
                self.score += 5*self.level
                if self.count_person == 5:
                    self.level +=1
                    self.count_person = 0
                    self.fps += 1
                    self.sound_next_level.play()

            if pygame.sprite.spritecollide(snake,self.snake_group,False):
                collider = pygame.sprite.spritecollide(snake,self.snake_group,False)[0]
                # print(collider)
                if collider!=snake:
                    self.game_over('snake')

            if snake.x in [0,DEFAULT_WINDOW_WIDTH - 20] or snake.y in [80,DEFAULT_WINDOW_HEIGHT - 20]:
                self.game_over('wall')

    def game_over(self,reason):
        self.gameover = True
        self.music.stop()
        self.sound_game_over.play()
        self.render_text('GAME   OVER',self.font_title_outline,BLACK,'CENTER',(self.window_width_center,200))
        self.render_text('GAME   OVER',self.font_title,GREEN,'CENTER',(self.window_width_center,200))
        if reason == 'wall':
            self.render_text('You   crashed  against   the   wall',self.font_title,GREEN,'CENTER',(self.window_width_center,280))
        if reason == 'snake':
            self.render_text('You   crashed  against   yourself',self.font_title,GREEN,'CENTER',(self.window_width_center,280))
        self.render_text('Press   Enter   to   continue',self.font_subtitle,GREEN,'CENTER',(self.window_width_center,480))

        pygame.display.flip()
        while self.gameon:
            self.events()

    def game_paused(self):
        self.gamepaused = True
        self.render_text('GAME   PAUSED',self.font_title_outline,BLACK,'CENTER',(self.window_width_center,200))
        self.render_text('GAME   PAUSED',self.font_title,GREEN,'CENTER',(self.window_width_center,200))
        self.render_text('Press   ESC   to   continue',self.font_subtitle,GREEN,'CENTER',(self.window_width_center,480))
        self.render_text('Press   Q   to   quit',self.font_subtitle,GREEN,'CENTER',(self.window_width_center,400))
        pygame.display.flip()
        while self.gamepaused:
            self.events()

    def update_score(self):
        text_level = 'Level  {}'.format(self.level)
        text_score = 'Score  {}'.format(self.score)
        self.render_text(text_level,self.font_score,YELLOW,'TOPLEFT',(20,80))
        self.render_text(text_score,self.font_score,YELLOW,'TOPLEFT',(DEFAULT_WINDOW_WIDTH - 150,80))
    
    def run(self):
        print(self.fullscreen)
        if self.fullscreen:
            pygame.display.toggle_fullscreen()
        self.snake = Snake(self.x,self.y)
        self.snake_group.add(self.snake)
        self.person = Person()
        self.person_group.add(self.person)
        self.music.play()
        print(self.game_keys)
        while self.gameon:
            self.events()
            self.screen()
            self.move_snake()
            self.check_collisions()
            self.update_score()
            pygame.display.flip()
            self.clock.tick(self.fps)
        

class Snake(pygame.sprite.Sprite,Game):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('picture/snake_round.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.x = x
        self.y = y
    
    def update(self,x,y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Person(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('picture/person2.png')
        self.rect = self.image.get_rect()
        self.width_floor = (DEFAULT_WINDOW_WIDTH-40)//20
        self.height_floor = (DEFAULT_WINDOW_HEIGHT-140)//20
        self.x = random.randint(2,self.width_floor)*20
        self.y = random.randint(6,self.height_floor)*20
        self.rect.topleft = (self.x,self.y)


if __name__== '__main__':
    main = Main()
    main.run()

  