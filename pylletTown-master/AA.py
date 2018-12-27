import pygame
from lib import tmx


def start():
    tilemap = tmx.load("palletTown.tmx", screen.get_size())
    # startCell = self.tilemap.layers['triggers'].find('playerStart')[0]
    # self.player = Player((startCell.px, startCell.py),
    #                      startCell['playerStart'], self.players)
    # self.tilemap.layers.append(self.players)
    tilemap.set_focus(0, 0)
    clock = pygame.time.Clock()
    left = 0
    top = 0
    while 1:
        dt = clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
        event = pygame.key.get_pressed()

        if event[pygame.K_UP]:
            top -= 10
        if event[pygame.K_DOWN]:
            top += 10
        if event[pygame.K_LEFT]:
            left -= 10
        if event[pygame.K_RIGHT]:
            left += 10
        if left < 0:
            left = 0
        if top < 0:
            top = 0
        tilemap.update(dt)
        tilemap.draw(screen)
        pygame.display.flip()
        tilemap.set_focus(left, top)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Pyllet Town")
    start()
