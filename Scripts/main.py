import pygame
from settings import *

class Main:
    def __init__(self):
        self.init_pygame()
        self.main_loop()

    def init_pygame(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))

    def main_loop(self):
        clock = pygame.time.Clock()
        is_running = True
        while is_running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
            
            key_input = pygame.key
            if key_input[pygame.K_UP]:
                # rotate
                pass
            if key_input[pygame.K_LEFT]:
                # move left
                pass
            elif key_input[pygame.K_RIGHT]:
                # move right
                pass
            if key_input[pygame.K_DOWN]:
                pass
            
        pygame.quit()

if __name__ == '__main__':
    Main()