import pygame
from settings import *
import board_manager
import display_manager
from time import time

class Main:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.bm = board_manager.BoardManager()
        self.dm = display_manager.DisplayManager(self.win, self.bm)
        
        self.main_loop()

    def main_loop(self):
        clock = pygame.time.Clock()
        is_running = True

        self.space = False
        self.t_fstep = time()
        self.t_step = time()
        self.t_down = time()
        self.is_moving = False

        while is_running:
            self.t = time()
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
            
            self.keyboard(pygame.key.get_pressed())

        pygame.quit()

    def sideway(self, pos):
        if not self.is_moving:
            self.bm.move_block((pos, 0))
            self.bm.update_projection()
            self.is_moving = True
            self.t_fstep = self.t
        elif self.t - self.t_fstep >= FSTEP_DELAY and self.t - self.t_step >= STEP_DELAY and self.is_moving:
            self.bm.move_block((pos, 0))
            self.bm.update_projection()
            self.t_step = self.t

    def keyboard(self, key_input):
        if key_input[pygame.K_UP]:
            # rotate
            pass
        if key_input[pygame.K_LEFT]:
            self.sideway(-1)
        elif key_input[pygame.K_RIGHT]:
            self.sideway(1)

        else:
            self.is_moving = False

        if key_input[pygame.K_DOWN] and self.t - self.t_down >= STEP_DELAY:
            self.t_down = self.t
            if not self.bm.move_block((0, -1)):
                self.bm.save_block()
                self.bm.remove_full_lines()
                self.bm.generate_block()
        if key_input[pygame.K_SPACE] and not self.space:
            self.space = True
            self.bm.move_down()
            self.bm.save_block()
            self.bm.remove_full_lines()
            self.bm.generate_block()
        if not key_input[pygame.K_SPACE] and self.space:
            self.space = False
        self.dm.draw_board()

if __name__ == '__main__':
    Main()