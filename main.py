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
        
        self.init_values()
        self.main_loop()

    def init_values(self):
        self.space = False
        self.t_fstep = time()
        self.t_step = time()
        self.t_down = time()
        self.t_touching = time()
        self.t_move = time()
        self.t_fall = time()
        self.up = False
        self.is_moving = False
        self.dir = -1
        self.hold = False
        self.fall_d = FALL_DELAY

    def main_loop(self):
        clock = pygame.time.Clock()
        is_running = True

        while is_running:
            self.t = time()
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
            self.keyboard(pygame.key.get_pressed())
            self.is_touching = not self.bm.is_possible(self.bm.block_kind, [self.bm.block_pos[0], self.bm.block_pos[1]-1], self.bm.block_rot)
            if self.is_touching:
                if self.t - self.t_touching >= TOUCHING_DELAY or self.t - self.t_move >= IMMOBILITY_DELAY:
                    self.place()
            else:
                self.t_touching = self.t
            
            if self.t - self.t_fall >= self.fall_d:
                self.move_down()

        pygame.quit()

    def sideway(self, pos):
        if not self.is_moving or self.dir!=pos:
            if self.bm.move_block((pos, 0)):
                self.dir = pos
                self.bm.update_projection()
                self.is_moving = True
                self.t_fstep = self.t
                self.t_move = self.t
        elif self.t - self.t_fstep >= FSTEP_DELAY and self.t - self.t_step >= STEP_DELAY and self.is_moving:
            if self.bm.move_block((pos, 0)):
                self.bm.update_projection()
                self.t_step = self.t
                self.t_move = self.t

    def keyboard(self, key_input):
        if key_input[pygame.K_UP] and not self.up:
            if self.bm.rotate():
                self.up = True
                self.t_move = self.t
        if not key_input[pygame.K_UP] and self.up:
            self.up = False
        if key_input[pygame.K_LEFT]:
            self.sideway(-1)
        elif key_input[pygame.K_RIGHT]:
            self.sideway(1)

        else:
            self.is_moving = False

        if key_input[pygame.K_DOWN] and self.t - self.t_down >= STEP_DELAY:
            if self.move_down():
                self.bm.score+=1

        if key_input[pygame.K_SPACE] and not self.space:
            self.space = True
            self.bm.move_down()
            self.place()
        elif not key_input[pygame.K_SPACE] and self.space:
            self.space = False

        if key_input[pygame.K_c] and not self.hold:
            self.hold = True
            self.bm.hold()

        self.dm.draw_board()

    def move_down(self):
        self.t_down = self.t
        if not self.bm.move_block((0, -1)):
            return False
        self.t_move = self.t
        self.t_fall = self.t
        return True

    def place(self):
        if self.bm.tspins>0:
            if self.bm.tspins <= 3:
                self.bm.score += TSPINS_SCORE[self.bm.tspins-1]
            else:
                self.bm.score += TSPINS_SCORE[2]
            self.bm.tspins = 0
        self.hold = False
        self.is_touching = False
        self.bm.save_block()
        self.bm.remove_full_lines()
        self.bm.generate_block()
        self.t_fall = self.t
        if self.bm.level >= MIN_DELAY_LEVEL:
            self.fall_d = 0
        else:
            self.fall_d = FALL_DELAY * (MIN_DELAY_LEVEL + 1 - self.bm.level) / MIN_DELAY_LEVEL
         

if __name__ == '__main__':
    Main()