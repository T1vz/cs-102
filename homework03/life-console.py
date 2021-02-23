import curses
from curses.textpad import rectangle
import time

from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife, speed: int=10) -> None:
        super().__init__(life)

        self.speed = speed

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        rectangle(screen, 0,0, self.life.rows+1, self.life.cols+1)
        pass

    def draw_grid(self, screen) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    screen.addch(i+1, j+1, '*')
                else:
                    screen.addch(i+1, j+1, ' ')
        pass

    def run(self) -> None:
        screen = curses.initscr()
        running = True
        while running:  
            self.draw_borders(screen)
            self.draw_grid(screen)

            if self.life.is_changing and self.life.is_max_generations_exceeded:
               self.life.step()
            else:
                running = False
            screen.refresh()
            time.sleep(1/self.speed)
        curses.endwin()
        pass

life = GameOfLife((20, 20), max_generations=255)
ui = Console(life)
ui.run()