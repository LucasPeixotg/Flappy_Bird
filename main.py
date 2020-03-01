import pygame
from random import random
from math import cos, sin, radians, floor

pygame.init()

screen_width = 1000
screen_height = 700

display_surface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

bird_image = pygame.image.load('./images/medium_bird.png')
gravity = .9

class Bird():
    def __init__(self):
        self.y = screen_height//2
        self.angle = 45
        self.y_vel = 0
        self.image = bird_image
        self.width = bird_image.get_width()
        self.height = bird_image.get_height()
        self.x = -self.width

    def rotate_image(self):
        # Calculate the angle based on the bird's position and the height of the screen
        self.angle = (self.y-(screen_height/2)) / (screen_height/2) * -90
        self.image = pygame.transform.rotate(bird_image, self.angle)

    def get_center(self):
        y_center = self.y + sin(radians(45+self.angle)) * (((self.width**2 + self.height**2)**(1/2))/2)
        x_center = self.x + cos(radians(45-self.angle)) * (((self.width**2 + self.height**2)**(1/2))/2)

        if self.angle < 0:
            x_center = self.x + cos(radians(45+self.angle)) * (((self.width**2 + self.height**2)**(1/2))/2)
        if self. angle < 0:
            y_center = self.y + sin(radians(45-self.angle)) * (((self.width**2 + self.height**2)**(1/2))/2)

        return (round(x_center), round(y_center))

class Pipe():
    def __init__(self, hole_size, width):
        self.x = int(screen_width)
        self.width = int(width)
        self.y_hole_init = int(((7*screen_height/8)-hole_size)*random())
        self.hole_size = int(hole_size)

def check_colision(bird, pipe):
    # check x colision
    x_colision = False
    bird_center = bird.get_center()
    
    if bird_center[0] + bird.width/2 > pipe.x and bird_center[0] - bird.width/2 < pipe.x + pipe.width:
        x_colision = True
    
    # check y colision
    y_colision = False
    if bird_center[1] + bird.height/2 > (pipe.y_hole_init + pipe.hole_size) or bird_center[1] - bird.height/2 < pipe.y_hole_init:
        y_colision = True

    return x_colision and y_colision

def game_over(score, green, blue, c_color):
    clock = pygame.time.Clock()

    SCREEN_GREEN = green
    SCREEN_BLUE = blue
    C_TIME_COLOR = c_color

    SHOW_RESTART_TEXT = True

    restart_font = pygame.font.SysFont("comicsansms", 20)
    restart_text = restart_font.render("Press any key to restart", True, (255, 255, 255))

    score_font = pygame.font.SysFont("comicsansms", 60)
    score_text = score_font.render("SCORE: " + str(score), True, (255, 255, 255))

    while True:
        display_surface.fill((0, round(SCREEN_GREEN), round(SCREEN_BLUE)))

        SCREEN_BLUE += C_TIME_COLOR
        SCREEN_GREEN += C_TIME_COLOR

        if SCREEN_GREEN <= 50 or SCREEN_GREEN >= 224:
            C_TIME_COLOR *= -1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                main()

        if SHOW_RESTART_TEXT:
            display_surface.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + restart_text.get_height()))
        
        display_surface.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - score_text.get_height()))

        SHOW_RESTART_TEXT = not SHOW_RESTART_TEXT

        pygame.display.update()
        clock.tick(1)


def main():
    DRAW_COLISION = False

    clock = pygame.time.Clock()
    score = 0
    bird = Bird()

    pipes_list = []
    
    PIPE_HOLE_SIZE = bird.height*5
    PIPE_WIDTH = bird.width * 2
    pipes_list.append(Pipe(PIPE_HOLE_SIZE, PIPE_WIDTH))

    SCREEN_VEL = 2
    LENGTH_BIAS = 1.01

    SCORE = 0

    font = pygame.font.SysFont("comicsansms", 60)

    SCREEN_GREEN = 224
    SCREEN_BLUE = 255
    C_TIME_COLOR = -.05

    while True:

        display_surface.fill((0, round(SCREEN_GREEN), round(SCREEN_BLUE)))

        SCREEN_BLUE += C_TIME_COLOR
        SCREEN_GREEN += C_TIME_COLOR

        if SCREEN_GREEN <= 50 or SCREEN_GREEN >= 224:
            C_TIME_COLOR *= -1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    bird.y_vel = - 10 * (bird.height/100 + 1) * gravity  
                elif event.key == pygame.K_c:
                    DRAW_COLISION = not DRAW_COLISION
                elif event.key == pygame.K_r:
                    main()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()

        if DRAW_COLISION:
            pygame.draw.circle(display_surface, (200, 0, 0), bird.get_center(), int(bird.width/2))
            pygame.draw.rect(display_surface, (200, 0, 0), (0, bird.get_center()[1], int(screen_width), 3))
            pygame.draw.rect(display_surface, (200, 0, 0), (bird.get_center()[0], 0, 3, screen_height))
            
        display_surface.blit(bird.image, (int(bird.x), int(bird.y)))

        # Update Bird
        bird.y_vel += gravity
        bird.y += bird.y_vel
        
        bird.rotate_image()

        colision = check_colision(bird, pipes_list[0])
        
        if colision:
            game_over(SCORE, SCREEN_GREEN, SCREEN_BLUE, C_TIME_COLOR)

        if bird.x < 3*bird.width:
            bird.x += 2


        # Update Pipes
        for pipe in pipes_list:
            if pipe.x < -pipe.width:
                pipes_list.pop(pipes_list.index(pipe))
                SCORE += 1
                continue

            pygame.draw.rect(display_surface, (0,255,0), (floor(pipe.x), 0, pipe.width, pipe.y_hole_init))
            pygame.draw.rect(display_surface, (0,225,0), (floor(pipe.x), 0, pipe.width//4, pipe.y_hole_init))
            pygame.draw.rect(display_surface, (0,215,0), (floor(pipe.x), 0, pipe.width//6, pipe.y_hole_init))
            
            pygame.draw.rect(display_surface, (0,255,0), (floor(pipe.x), pipe.y_hole_init+pipe.hole_size, floor(pipe.width), screen_height-(pipe.y_hole_init+pipe.hole_size)))
            pygame.draw.rect(display_surface, (0,225,0), (floor(pipe.x), pipe.y_hole_init+pipe.hole_size, floor(pipe.width/4), screen_height-(pipe.y_hole_init+pipe.hole_size)))
            pygame.draw.rect(display_surface, (0,215,0), (floor(pipe.x), pipe.y_hole_init+pipe.hole_size, floor(pipe.width/6), screen_height-(pipe.y_hole_init+pipe.hole_size)))

            pipe.x -= SCREEN_VEL

        if pipes_list[len(pipes_list) - 1].x < (screen_width - 4 * PIPE_WIDTH - LENGTH_BIAS):
            pipes_list.append(Pipe(PIPE_HOLE_SIZE, PIPE_WIDTH))
            SCREEN_VEL += .3
            LENGTH_BIAS += .3


        score_text = font.render(str(SCORE), True, (255, 255, 255))
        display_surface.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 5))

        pygame.display.update()
        clock.tick(60)


main()