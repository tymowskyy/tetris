from os import terminal_size
import pygame
from settings import *
import csv
import random


class BoardManager:
    def __init__(self):
        self.generate_board()
        self.load_blocks()
        self.generate_queue()
        self.generate_block()

    def generate_board(self):
        self.board = [[0 for j in range(SIZE_X)] for i in range(SIZE_Y)]

    def remove_full_lines(self):
        lines = self.get_full_lines()
        for i in lines:
            self.board.pop(i)
            self.board.insert(-1, [0 for i in range(SIZE_Y)])

    def get_full_lines(self):
        to_remove = []
        for index, i in enumerate(self.board):
            if not 0 in i:
                to_remove.append(index)
        return to_remove

    def load_blocks(self):
        self.blocks = []
        with open(BLOCKS_PATH, 'r') as csv_file:
            blocks_file = list(csv.reader(csv_file))

        for i in range(len(blocks_file)):
            if i % 16 == 0:
                self.blocks.append([])
            if i % 4 == 0:
                self.blocks[-1].append([])
            self.blocks[-1][-1].append(list(map(lambda x: x == '1', blocks_file[i])))

    def generate_queue(self):
        self.queue = [i for i in range(7)]
        random.shuffle(self.queue)

    def generate_block(self):
        self.block_pos = STARTING_POS
        self.block_kind = self.queue[0]
        self.queue.pop(0)
        if len(self.queue) == 0:
            self.generate_queue()

    def is_possible(self, kind, pos, rot):
        for i in range(4): # X
            for j in range(4): # Y
                if not self.blocks[kind][rot][j][i]:
                    continue
                if pos[0] + i < 0 or pos[0] + i >= SIZE_X or pos[1] - j < 0:
                   return False
                if pos[1] - j < SIZE_Y:
                    if self.board[pos[1] - j][pos[0] + i]:
                        return False
        return True

    def move_block(self, pos):
        new_pos = (self.block_pos[0] + pos[0], self.block_pos[1] + pos[1])
        if self.is_possible(self.block_kind, new_pos, 0):
            self.block_pos = new_pos
            return True
        return False

    def save_block(self):
        for i in range(4):
            for j in range(4):
                if not self.blocks[self.block_kind][0][j][i]:
                    continue
                self.board[self.block_pos[1] - j][self.block_pos[0] + i] = self.block_kind+1