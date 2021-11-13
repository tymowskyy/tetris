import pygame
from settings import *


class BoardManager:
    def __init__(self):
        self.generate_board()

    def generate_board(self):
        self.board = [[0 for j in range(SIZE_Y)] for i in range(SIZE_X)]

    def remove_full_lines(self):
        lines = self.get_full_lines()
        lines.reverse()
        for i in lines:
            self.board.pop(i)
            self.board.insert(-1, [0 for i in range(SIZE_Y)])
        print(self.board)

    def get_full_lines(self):
        to_remove = []
        for index, i in enumerate(self.board):
            if not 0 in i:
                to_remove.append(index)
        return to_remove
