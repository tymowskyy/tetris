import pygame
from settings import *


class DisplayManager:
    def __init__(self, win, bm):
        self.win = win
        self.bm = bm
        self.load_sprites()
        self.draw_board()

    def load_sprites(self):
        sprite_sheet = pygame.image.load(TILES_PATH)
        self.tiles = []
        for i in range(15):
            self.tiles.append(self.get_sprite(sprite_sheet, i))

    def get_sprite(self, sheet, index):
        image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
        image.blit(sheet, (0, 0), (index * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT))
        return image

    def get_tile(self, index, projection):
        if projection:
            return self.tiles[index * 2 + 2]
        else:
            return self.tiles[index * 2 + 1]

    def draw_board(self):
        self.draw_tiles()
        self.draw_block()
        pygame.display.flip()

    def draw_tiles(self):
        for i in range(SIZE_X):
            for j in range(SIZE_Y):
                self.draw_tile((i*TILE_WIDTH, (SIZE_Y-j-1)*TILE_HEIGHT), self.bm.board[i][j])
    
    def draw_tile(self, pos, col):
        if col==0:
            self.win.blit(self.tiles[0], pos)
        else:
            self.win.blit(self.get_tile(col-1, 0), pos)
    
    def draw_block(self):
        for i in range(4):
            for j in range(4):
                if self.bm.blocks[self.bm.block_kind][0][j][i]:
                    self.draw_tile(((self.bm.block_pos[0] + i) * TILE_WIDTH, (SIZE_Y - self.bm.block_pos[1] + j - 1) * TILE_WIDTH), self.bm.block_kind+1)
        