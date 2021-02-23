import pygame
import random

from pygame.locals import *
from typing import List, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        # PUT YOUR CODE HERE
        self.grid = self.create_grid(True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE
            self.draw_grid()
            self.grid = self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool=False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """

        if randomize:
            grid = [[random.randint(0, 1) for x in range(self.cell_width)] for i in range(self.cell_height)]
        else:
            grid = [[0 for x in range(self.cell_width)] for i in range(self.cell_height)]
        return grid

    def draw_grid(self) -> None:
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'), pygame.Rect(j*self.cell_size, i*self.cell_size, self.cell_width*self.cell_size, self.cell_height*self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), pygame.Rect(j*self.cell_size, i*self.cell_size, self.cell_width*self.cell_size, self.cell_height*self.cell_size))

        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        pass

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """

        cells = []

        startW = cell[1]-1
        endW = cell[1]+1
        if (cell[1] == 0):
            startW = 0
        elif (cell[1] == self.cell_width-1):
            endW = cell[1]

        startH = cell[0]-1
        endH = cell[0]+1
        if (cell[0] == 0):
            startH = 0
        elif (cell[0] == self.cell_height-1):
            endH = cell[0]
        
        for i in range(startH, endH+1):
            for j in range(startW, endW+1):
                if not ((cell[0] == i) and (cell[1] == j)):
                    cells.append(self.grid[i][j])

        return cells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = []
        for i in range(self.cell_height):
            new_cell = []
            for j in range(self.cell_width):
                if self.grid[i][j] == 0:
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
