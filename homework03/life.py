import pathlib
import random
import json

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    
    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool=False) -> Grid:
        if randomize:
            grid = [[random.randint(0, 1) for x in range(self.cols)] for i in range(self.rows)]
        else:
            grid = [[0 for x in range(self.cols)] for i in range(self.rows)]
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        cells = []

        startW = cell[1]-1
        endW = cell[1]+1
        if (cell[1] == 0):
            startW = 0
        elif (cell[1] == self.cols-1):
            endW = cell[1]

        startH = cell[0]-1
        endH = cell[0]+1
        if (cell[0] == 0):
            startH = 0
        elif (cell[0] == self.rows-1):
            endH = cell[0]
        
        for i in range(startH, endH+1):
            for j in range(startW, endW+1):
                if not ((cell[0] == i) and (cell[1] == j)):
                    cells.append(self.curr_generation[i][j])

        return cells

    def get_next_generation(self) -> Grid:
        new_grid = []
        for i in range(self.rows):
            new_cell = []
            for j in range(self.cols):
                if self.curr_generation[i][j] == 0:
                    if self.get_neighbours((i, j)).count(1) == 3:
                        new_cell.append(1)
                    else:
                        new_cell.append(0)
                else:
                    if self.get_neighbours((i, j)).count(1) == 2 or self.get_neighbours((i, j)).count(1) == 3:
                        new_cell.append(1)
                    else:
                        new_cell.append(0)
            new_grid.append(new_cell)

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations+=1
        pass

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations > self.max_generations:
            return False
        else:
            return True

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.prev_generation == self.curr_generation:
            return False
        else:
            return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        f = open(filename, 'r')
        game_status = json.load(f)

        life = GameOfLife((game_status['rows'], game_status['cols']), randomize=False, max_generations = game_status['max_generations'])
        life.prev_generation = game_status['prev_generation']
        life.curr_generation = game_status['curr_generation']
        life.generations = game_status['generations']

        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        game_status = {
            'rows': self.rows,
            'cols': self.cols,
            'max_generations': self.max_generations,
            'prev_generation': self.prev_generation,
            'curr_generation': self.curr_generation,
            'generations': self.generations
        }

        f = open(filename, 'w')
        json.dump(game_status, f)
        pass