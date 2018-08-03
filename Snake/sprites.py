import pygame
from settings import *


class Part(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.parts
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((PARTSIZE-1, PARTSIZE-1))
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.game = game

    def update(self):
        pass


class Snake:
    def __init__(self, game, x, y):
        self.body = [Part(game, i*PARTSIZE+x, y) for i in range(1)]
        self.size = len(self.body)

        self.game = game

        self.dir = (1, 0)
        self.x = x
        self.y = y

    def update(self):

        self.x += self.dir[0] * PARTSIZE
        self.y += self.dir[1] * PARTSIZE

        part = self.body.pop(0)
        part.kill()

        self.body.append(Part(self.game, self.x, self.y))

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.dir = (0, -1)

        if keystate[pygame.K_RIGHT]:
            self.dir = (1, 0)

        if keystate[pygame.K_DOWN]:
            self.dir = (0, 1)

        if keystate[pygame.K_LEFT]:
            self.dir = (-1, 0)
