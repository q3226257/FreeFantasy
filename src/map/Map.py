import tmx
from tmx import *
from pygame import *
import pygame

# 用来记录当前坐标
location = (0, 0)


class Map:
    def __init__(self):
        self.map: TileMap = None

    def update(self, fps):
        pass

    def get_enter_location(self) -> (int, int):
        pass

    def append_layer(self, layer):
        self.map.layers.append(layer)

    def set_focus(self, x, y):
        self.map.set_focus(x, y)


class Tower(Map):
    NAME = "tower"
    SRC_FILE = "resource/palletTown.tmx"
    INIT_LOCATION = (0, 0)

    def __init__(self, screen: Surface):
        super().__init__()
        global location
        location = self.INIT_LOCATION
        self.map: tmx.TileMap = tmx.load(self.SRC_FILE, screen.get_size())
        super().set_focus(location[0], location[1])
        self.screen = screen

    def update(self, fps):
        self.map.update(fps)
        self.map.draw(self.screen)
        pygame.display.flip()
        super().set_focus(location[0], location[1])

    def get_enter_location(self):
        return 100, 100
