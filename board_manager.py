from settings import *
import csv
import random


class BoardManager:
    def __init__(self):
        self.generate_board()
        self.load_blocks()
        self.load_offsets()
        self.generate_queue()
        self.generate_block()
        self.holded = 0
        self.score = 0
        self.lines = 0
        self.tspins = 0
        self.level = 1

    def generate_board(self):
        self.board = [[0 for j in range(SIZE_X)] for i in range(SIZE_Y)]

    def remove_full_lines(self):
        lines = self.get_full_lines()
        lines.reverse()
        for i in lines:
            self.board.pop(i)
            self.board.insert(SIZE_Y-1, [0 for i in range(SIZE_X)])
        if len(lines) > 0:
            self.score += LINE_SCORES[len(lines)-1] * self.level
            if self.lines//LINES_TO_NEXT_LEVEL != (self.lines + len(lines))//LINES_TO_NEXT_LEVEL:
                self.level+=1
            self.lines += len(lines)

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

    def load_offsets(self):
        self.offsets = [[],[]]
        for (index, path) in zip([0, 1], [IOFFSETS_PATH, JLTSZOFFSETS_PATH]):
            with open(path, 'r') as csv_file:
                reader = csv.reader(csv_file)
                for i in reader:
                    ii = list(map(int, i))
                    self.offsets[index].append([(ii[0], ii[1]), (ii[2], ii[3]), (ii[4], ii[5]), (ii[6], ii[7])])

    def generate_queue(self):
        self.queue = [i for i in range(7)]
        random.shuffle(self.queue)

    def generate_block(self):
        self.block_pos = STARTING_POS
        self.block_kind = self.queue[0]
        self.block_rot = 0
        while not self.is_possible(self.block_kind, self.block_pos, self.block_rot):
            self.block_pos = (self.block_pos[0], self.block_pos[1] + 1)
        self.queue.pop(0)
        if len(self.queue) == 0:
            self.generate_queue()
        self.update_projection()

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
        if self.is_possible(self.block_kind, new_pos, self.block_rot):
            self.block_pos = new_pos
            self.tspins = 0
            return True
        return False

    def save_block(self):
        for i in range(4):
            for j in range(4):
                if not self.blocks[self.block_kind][self.block_rot][j][i]:
                    continue
                if self.block_pos[1] - j >= SIZE_Y:
                    return True
                self.board[self.block_pos[1] - j][self.block_pos[0] + i] = self.block_kind+1
        return False
    def update_projection(self):
        for i in range(self.block_pos[1], -1, -1):
            if not self.is_possible(self.block_kind, [self.block_pos[0], i], self.block_rot):
                self.block_proj = i+1
                return

    def move_down(self):
        self.score += (self.block_pos[1] - self.block_proj) * 2
        self.block_pos = [self.block_pos[0], self.block_proj]

    def rotate(self):
        is_i = False
        if self.block_kind == 1: # O
            return False
        elif self.block_kind == 0: # I
            is_i=True    
        for dir in [0, 1]:
            for i in [(0, 0)] + self.offsets[not is_i][self.block_rot*2 + dir]:
                new_pos = [self.block_pos[0] + i[0], self.block_pos[1] + i[1]]
                new_rot = (self.block_rot-1)%4 if dir else (self.block_rot+1)%4
                if self.is_possible(self.block_kind, new_pos, new_rot):
                    self.block_pos = new_pos
                    self.block_rot = new_rot
                    self.update_projection()
                    if self.is_tspin():
                        self.tspins += 1
                    else:
                        self.tspins = 0

                    return True
        return False

    def hold(self):
        self.tspins = 0
        tmp = self.holded
        self.holded = self.block_kind+1
        if tmp != 0:
            self.queue.insert(0, tmp-1)
        self.generate_block()

    def is_tspin(self):
        if self.block_kind != 2:
            return False
        zeros = 0
        for i in [0, 2]:
            for j in [0, 2]:
                new_pos = [self.block_pos[0]+i, self.block_pos[1]-j]
                if new_pos[0] >= 0 and new_pos[0] < SIZE_X and new_pos[1] >= 0 and new_pos[1] < SIZE_Y:
                    if self.board[new_pos[1]][new_pos[0]] == 0:
                        zeros+=1
        return zeros <= 1