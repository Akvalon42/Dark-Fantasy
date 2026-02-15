import pygame as pg
import pygame_menu
import random


pg.init()
pg.mixer.init()
from game import Game
from constanta import *
class Menu:
    def __init__(self):
        self.surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame_menu.themes.THEME_GREEN.widget_font = pygame_menu.font.FONT_FIRACODE
        self.menu = pygame_menu.Menu(
            height=SCREEN_HEIGHT,
            width=SCREEN_WIDTH,
            theme=pygame_menu.themes.THEME_GREEN,
            title="dark sails"

        )
        self.quality = "easy"


        self.menu.add.selector("Сложность:", [
            ('легкий', 1),
            ("средний", 2),
            ("хардкор", 3)],
                               onchange=self.set_quality)
        self.menu.add.button("НАЧАТЬ ИГРУ", self.start_game)
        self.menu.add.button("ВЫЙТИ В МЕНЮ", pygame_menu.events.EXIT)



        self.run()



    def set_quality(self, selected, value):
        match value:
            case 1: self.quality = "easy"
            case 2: self.quality = "middle"
            case 3: self.quality = "hard"


    def start_game(self):
        Game(self.quality)

    def quit_game(self):
        quit()

    def run(self):
        self.menu.mainloop(self.surface)


if __name__ == "__main__":
    menu_app = Menu()