import tmx
from pygame import *
import pygame
from map.Map import *
from character.HeroInfo import *
from constant.Constant import *

LEFT = 1
RIGHT = 2
DOWN = 3
UP = 4


class Model(pygame.sprite.Sprite):
    def __init__(self, img_path, rect, info: BaseInfo, *groups):
        # 先创建一个地图精灵组
        self.layer = tmx.SpriteLayer()
        super(Model, self).__init__(self.layer, *groups)
        # 一些必要属性
        self.image = pygame.image.load(img_path)
        self.imageDefault = self.image.copy()
        self.image.scroll(0, -64)
        self.rect = rect
        # 该模型的属性
        self.info = info
        # 装载精灵的对象
        self.c_map: Map = None

    # 进入一个新的地图
    def go(self, go_map: Map):
        self.c_map = go_map
        go_map.append_layer(self.layer)
        go_map.set_focus(50, 50)

    # 行走
    def walk(self):
        self.c_map.set_focus(self.rect.centerx, self.rect.centery)

        if not self.info.control_walk_speed():
            return
        press_key = pygame.key.get_pressed()
        last_rect = self.rect.copy()
        collide_rect = self.rect.copy()

        def rel_walk(direct):
            if direct == UP:
                self.rect.top -= 8
            elif direct == DOWN:
                self.rect.top += 8
            elif direct == LEFT:
                self.rect.left -= 8
            elif direct == RIGHT:
                self.rect.left += 8

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
        if len(self.c_map.has_collide(collide_rect)) <= 0:
            self.rect = last_rect

    # 每帧更新
    def update(self, dt):
        # 行走
        self.walk()

    # def get_collide_rect(self):
    #     top = self.rect.top + 60
    #     return pygame.Rect(self.rect.left, top, self.rect.width, 5)


class Warrior(Model):
    def __init__(self, left_top: (int, int), *groups):
        img_path = 'resource/sprites/player.png'
        rect = pygame.Rect((left_top[0], left_top[1]), (64, 64))
        super(Warrior, self).__init__(img_path, rect, XiangYu(), *groups)


class Player(pygame.sprite.Sprite):
    def __init__(self, location, orientation, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('resource/sprites/player.png')
        self.imageDefault = self.image.copy()
        self.rect = pygame.Rect(location, (64, 64))
        self.orient = orientation
        self.holdTime = 0
        self.walking = False
        self.dx = 0
        self.step = 'rightFoot'
        # Set default orientation
        self.setSprite()

    def setSprite(self):
        # Resets the player sprite sheet to its default position
        # and scrolls it to the necessary position for the current orientation
        self.image = self.imageDefault.copy()
        if self.orient == 'up':
            self.image.scroll(0, -64)
        elif self.orient == 'down':
            self.image.scroll(0, 0)
        elif self.orient == 'left':
            self.image.scroll(0, -128)
        elif self.orient == 'right':
            self.image.scroll(0, -192)

    def update(self, dt):
        key = pygame.key.get_pressed()
        # Setting orientation and sprite based on key input:
        if key[pygame.K_UP]:
            if not self.walking:
                if self.orient != 'up':
                    self.orient = 'up'
                    self.setSprite()
                self.holdTime += dt
        elif key[pygame.K_DOWN]:
            if not self.walking:
                if self.orient != 'down':
                    self.orient = 'down'
                    self.setSprite()
                self.holdTime += dt
        elif key[pygame.K_LEFT]:
            if not self.walking:
                if self.orient != 'left':
                    self.orient = 'left'
                    self.setSprite()
                self.holdTime += dt
        elif key[pygame.K_RIGHT]:
            if not self.walking:
                if self.orient != 'right':
                    self.orient = 'right'
                    self.setSprite()
                self.holdTime += dt
        else:
            self.holdTime = 0
            self.step = 'rightFoot'
        # Walking mode enabled if a button is held for 0.1 seconds
        if self.holdTime >= 100:
            self.walking = True
        lastRect = self.rect.copy()
        # Walking at 8 pixels per frame in the direction the player is facing
        if self.walking and self.dx < 64:
            if self.orient == 'up':
                self.rect.y -= 0
            elif self.orient == 'down':
                self.rect.y += 8
            elif self.orient == 'left':
                self.rect.x -= 8
            elif self.orient == 'right':
                self.rect.x += 8
            self.dx += 8
            # Collision detection:
            # Reset to the previous rectangle if player collides
            # with anything in the foreground layer
            # if len(game.tilemap.layers['triggers'].collide(self.rect,
            #                                                'solid')) > 0:
            self.rect = lastRect
            # Area entry detection:
            # elif len(game.tilemap.layers['triggers'].collide(self.rect,
            #                                                  'entry')) > 0:
            #     entryCell = game.tilemap.layers['triggers'].find('entry')[0]
            #     game.fadeOut()
            #     game.initArea(entryCell['entry'])

            return
        # Switch to the walking sprite after 32 pixels
        if self.dx == 32:
            # Self.step keeps track of when to flip the sprite so that
            # the character appears to be taking steps with different feet.
            if (self.orient == 'up' or
                self.orient == 'down') and self.step == 'leftFoot':
                self.image = pygame.transform.flip(self.image, True, False)
                self.step = 'rightFoot'
            else:
                self.image.scroll(-64, 0)
                self.step = 'leftFoot'
        # After traversing 64 pixels, the walking animation is done
        if self.dx == 64:
            self.walking = False
            self.setSprite()
            self.dx = 0

        # game.tilemap.set_focus(self.rect.x, self.rect.y)
