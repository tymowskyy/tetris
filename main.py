import pygame
from settings import *
import board_manager
import display_manager

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
        while is_running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
            
            key_input = pygame.key.get_pressed()
            if key_input[pygame.K_UP]:
                # rotate
                pass
            if key_input[pygame.K_LEFT]:
                self.bm.move_block((-1, 0))
                self.bm.update_projection()
                pass
            elif key_input[pygame.K_RIGHT]:
                self.bm.move_block((1, 0))
                self.bm.update_projection()
            if key_input[pygame.K_DOWN]:
                if not self.bm.move_block((0, -1)):
                    self.bm.save_block()
                    self.bm.remove_full_lines()
                    self.bm.generate_block()
            if key_input[pygame.K_SPACE]:
                self.bm.move_down()
                self.bm.save_block()
                self.bm.remove_full_lines()
                self.bm.generate_block()
            
            self.dm.draw_board()

        pygame.quit()


if __name__ == '__main__':
    Main()