import pygame
from pygame.locals import *
from sys import exit

pygame.init()

screen = pygame.display.set_mode((1600,800))
rect1 = Rect(50, 60, 50, 50)
rect2=rect1.copy()
x=0
y=0
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key==K_LEFT:
                x= -5
                y= 0
                print('Left')
                rect2.move_ip(x,y)
            if event.key == K_RIGHT:
                x= 5
                y= 0
                print('Right')
                rect2.move_ip(x,y)
            if event.key == K_UP:
                x = 0
                y = -5
                print('Up')
                rect2.move_ip(x,y)
            if event.key == K_DOWN:
                x = 0
                y = 5
                print('Down')
                rect2.move_ip(x,y)
    print(rect2)
    screen.fill((127,127,127))
    pygame.draw.rect(screen, (255,0,0), rect1, 1)
    pygame.draw.rect(screen, (0,0,255), rect2, 5)
    pygame.display.update()

pygame.quit()
