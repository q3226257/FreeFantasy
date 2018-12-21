import tmx
from tmx import *
from pygame import *
from constant.Constant import *
import pygame

# 用来记录当前坐标
location = (0, 0)


class Map:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.map: TileMap = None


    def get_enter_location(self) -> (int, int):
        pass

    def append_layer(self, layer):
        self.map.layers.append(layer)

    def has_collide(self, rect):
        return self.map.layers[COLLISION_LAYER].collide(rect, CAN_MOVE)

    def set_focus(self, x, y):
        self.map.set_focus(x, y)

    def update(self, fps):
        self.map.update(fps)
        self.map.draw(self.screen)
        pygame.display.flip()
        self.set_focus(location[0], location[1])


class Tower(Map):
    NAME = "tower"
    SRC_FILE = "resource/palletTown.tmx"
    INIT_LOCATION = (0, 0)

    def __init__(self, screen: Surface):
        super().__init__(screen)
        global location
        location = self.INIT_LOCATION
        self.map: tmx.TileMap = tmx.load(self.SRC_FILE, screen.get_size())
        super().set_focus(location[0], location[1])
        self.screen = screen

    def get_enter_location(self):
        return 100, 100


class First(Map):
    NAME = "first"
    SRC_FILE = "tmx/my.tmx"
    INIT_LOCATION = (0, 0)

    def __init__(self, screen: Surface):
        super().__init__(screen)
        global location
        location = self.INIT_LOCATION
        self.map: tmx.TileMap = tmx.load(self.SRC_FILE, screen.get_size())
        self.screen = screen

    def get_enter_location(self):
        return 80, 180
