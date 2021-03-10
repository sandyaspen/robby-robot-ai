import random

import numpy as np

class Grid:

    def __init__(self) -> None:
        self.grid = np.zeros((10,10), dtype=int)
        self.robby_pos = 0, 0
        self.scatter_cans()
        self.random_robby()

    def scatter_cans(self):
        self.grid = np.zeros((10,10), dtype=int)
        with np.nditer(self.grid, op_flags=['readwrite']) as grid:
            for square in grid:
                if random.random() < 0.5:
                    square[...] = 1
                else:
                    square[...] = 0
    
    def check_done(self):
        if self.grid.sum() == 2: #Only robby is left
            return True
        return False

    def random_robby(self):
        x = random.randrange(0, 10)
        y = random.randrange(0, 10)
        self.move_robby(x,y)
        return x, y

    def remove_can(self):
        x, y = self.robby_pos
        if self.grid[x,y] % 2 == 1:
            self.grid[x,y] -= 1
            return True
        else:
            return False

    def move_robby(self, x, y):
        if (x < 0) or (x > 9) or (y < 0) or (y > 9):
            return False
        self.grid[self.robby_pos[0], self.robby_pos[1]] -= 2
        self.robby_pos = x, y
        self.grid[self.robby_pos[0], self.robby_pos[1]] += 2
        return True
    
    def move_robby_north(self):
        x, y = self.robby_pos
        return self.move_robby(x, y+1)
    
    def move_robby_south(self):
        x, y = self.robby_pos
        return self.move_robby(x, y-1)
    
    def move_robby_east(self):
        x, y = self.robby_pos
        return self.move_robby(x+1, y)
    
    def move_robby_west(self):
        x, y = self.robby_pos
        return self.move_robby(x-1, y)
    
    def sense_position(self, x, y):
        if (x < 0) or (x > 9):
            return -1
        elif (y < 0) or (y > 9):
            return -1
        elif self.grid[x,y] % 2 == 1:
            return 1
        else:
            return 0
    
    def sense_west(self):
        x, y = self.robby_pos
        return self.sense_position(x-1, y)

    def sense_east(self):
        x, y = self.robby_pos
        return self.sense_position(x+1, y)

    def sense_north(self):
        x, y = self.robby_pos
        return self.sense_position(x, y+1)

    def sense_south(self):
        x, y = self.robby_pos
        return self.sense_position(x, y-1)

    def sense_current(self):
        x, y= self.robby_pos
        return self.sense_position(x, y)
