import pygame
from src.map.Map import *
from src.character.HeroModel import *

maps = {}


def start():
    c_map = maps.get(Tower.NAME)
    if c_map is None:
        c_map = First(screen)
        war = Warrior(c_map.get_enter_location())
        war.go(c_map)
        maps[Tower.NAME] = c_map

    c_map.update(clock.tick(60))


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Pyllet Town")
    clock = pygame.time.Clock()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("exit")
                exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("exit2")
                exit(0)
        start()
