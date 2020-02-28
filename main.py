import pygame

pygame.init()

screen_width = 800
screen_height = 500

display_surface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

bird_image = pygame.image.load('./images/bird.png')
gravity = .6

class Bird():
    def __init__(self):
        self.x = 70
        self.y = screen_height//2
        self.angle = 0
        self.y_vel = 0
        self.image = bird_image

    def rotate_image(self):
        # Calculate the angle based on the bird's position and the height of the screen
        self.angle = (self.y-(screen_height/2)) / (screen_height/2) * -90
        self.image = pygame.transform.rotate(bird_image, self.angle)

def main():
    clock = pygame.time.Clock()
    score = 0
    bird = Bird()

    while True:

        display_surface.fill((201, 242, 242))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.y_vel = -15 * gravity 
            
        display_surface.blit(bird.image, (int(bird.x), int(bird.y)))

        bird.y_vel += gravity
        bird.y += bird.y_vel
        
        bird.rotate_image()

        pygame.display.update()
        clock.tick(60)


main()