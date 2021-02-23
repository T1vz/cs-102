import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        super().__init__(life)

        self.cell_size = cell_size

        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size

        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))
        pass

    def draw_grid(self) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'), pygame.Rect(j*self.cell_size, i*self.cell_size, self.life.cols*self.cell_size, self.life.rows*self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), pygame.Rect(j*self.cell_size, i*self.cell_size, self.life.cols*self.cell_size, self.life.rows*self.cell_size))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        pause = not pause

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button==1:
                        if pause:
                            x_pos, y_pos = pygame.mouse.get_pos()
                            cell_x = x_pos // self.cell_size
                            cell_y = y_pos // self.cell_size 

                            if self.life.curr_generation[cell_y][cell_x] == 1:
                                self.life.curr_generation[cell_y][cell_x] = 0
                            else: 
                                self.life.curr_generation[cell_y][cell_x] = 1
        
                            self.draw_grid()
                            self.draw_lines()
                            pygame.display.flip()
            if not pause:
                self.draw_grid()
                self.draw_lines()

                if self.life.is_changing and self.life.is_max_generations_exceeded:
                    self.life.step()
                else:
                    running = False
                pygame.display.flip()
                clock.tick(self.speed)
        pygame.quit()
        pass

life = GameOfLife((7, 7), True)
gui = GUI(life, 100)
gui.run()
gui.life.save('test.txt')