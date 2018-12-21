import tmx
from pygame import *
import pygame
from map.Map import *
from character.HeroInfo import *
from constant.Constant import *
import math

"""
精灵组 pygame.sprite.AbstractGroup
精灵 pygame.sprite.Sprite
可以将精灵加入到精灵组一起进行update操作

tmx.TileMap 可以调用 layers.append()
将精灵或者精灵组加入到图层，以便进行update

"""

LEFT = "LEFT"
RIGHT = "RIGHT"
DOWN = "DOWN"
UP = "UP"

# 先创建一个地图精灵组
hero_sprites = tmx.SpriteLayer()


class Model(pygame.sprite.Sprite):
    def split_image(self, ):
        img = pygame.image.load(self.img_path)
        return dict(
            DOWN=[img.subsurface((0, 0), (64, 64)), img.subsurface((64, 0), (64, 64))],
            UP=[img.subsurface((0, 64), (64, 64)), img.subsurface((64, 64), (64, 64))],
            LEFT=[img.subsurface((0, 128), (64, 64)), img.subsurface((64, 128), (64, 64))],
            RIGHT=[img.subsurface((0, 192), (64, 64)), img.subsurface((64, 192), (64, 64))])

    def __init__(self, img_path, rect, info: BaseInfo, *groups):
        super(Model, self).__init__(hero_sprites, *groups)
        self.img_path = img_path
        # 一些必要属性
        self.images = self.split_image()
        # self.imageDefault = self.image.copy()
        self.image = self.images[DOWN][0]
        self.rect = rect
        # 该模型的属性
        self.info = info
        # 装载精灵的地图
        self.c_map: Map = None
        self.hold_times = 0
        self.threshold_times = 10

    # 进入一个新的地图
    def go(self, go_map: Map):
        self.c_map = go_map
        go_map.append_layer(hero_sprites)
        go_map.set_focus(self.rect.centerx, self.rect.centery)

    # 行走
    def walk(self, dt):
        """
        行走操作
        :param dt:更新间隔时间
        """
        self.c_map.set_focus(self.rect.centerx, self.rect.centery)

        press_key = pygame.key.get_pressed()
        last_rect = self.rect.copy()

        dis = int(dt * self.info.speed + 1)

        def rel_walk(direct):
            self.hold_times += 1
            self.check_update_img(self.images[direct])
            if direct == UP:
                self.rect.top -= dis
            elif direct == DOWN:
                self.rect.top += dis
            elif direct == LEFT:
                self.rect.left -= dis
            elif direct == RIGHT:
                self.rect.left += dis

        if press_key[pygame.K_UP]:
            rel_walk(UP)
        elif press_key[pygame.K_DOWN]:
            rel_walk(DOWN)
        elif press_key[pygame.K_LEFT]:
            rel_walk(LEFT)
        elif press_key[pygame.K_RIGHT]:
            rel_walk(RIGHT)
        else:
            pass
        # if len(self.c_map.has_collide(collide_rect)) <= 0:
        #     self.rect = last_rect

    # 每帧更新
    def update(self, dt):
        # 行走
        self.walk(dt)

    def check_update_img(self, direct_img):
        if self.hold_times > self.threshold_times:
            self.hold_times = 0
            if self.image == direct_img[0]:
                self.image = direct_img[1]
            else:
                self.image = direct_img[0]


class Warrior(Model):
    def __init__(self, left_top: (int, int), *groups):
        img_path = 'resource/sprites/player.png'
        rect = pygame.Rect((left_top[0], left_top[1]), (64, 64))
        super(Warrior, self).__init__(img_path, rect, XiangYu(), *groups)
