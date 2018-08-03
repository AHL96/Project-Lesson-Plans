import pygame
from settings import *
from random import randint


class Food(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.foods
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((PARTSIZE-1, PARTSIZE-1))
        self.image.fill(FOODCOLOR)

        self.rect = self.image.get_rect()

        self.rect.x = randint(0, WIDTH//PARTSIZE) * PARTSIZE + 1
        self.rect.y = randint(0, HEIGHT//PARTSIZE) * PARTSIZE + 1


class Part(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.parts
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((PARTSIZE-1, PARTSIZE-1))
        self.image.fill(SNAKECOLOR)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.game = game


class Snake:
    def __init__(self, game, x, y):
        self.body = [Part(game, i*PARTSIZE+x, y) for i in range(1)]
        self.size = len(self.body)

        self.game = game

        self.dir = (1, 0)
        self.x = x
        self.y = y

        self.alive = True

    def update(self):

        # movement
        # print(self.dir)
        self.x += self.dir[0] * PARTSIZE
        self.y += self.dir[1] * PARTSIZE
        part = self.body.pop(0)
        part.kill()
        self.body.append(Part(self.game, self.x, self.y))

        # player controls
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP] and self.dir != (0, 1):
            self.dir = (0, -1)
        if keystate[pygame.K_RIGHT] and self.dir != (-1, 0):
            self.dir = (1, 0)
        if keystate[pygame.K_DOWN] and self.dir != (0, -1):
            self.dir = (0, 1)
        if keystate[pygame.K_LEFT] and self.dir != (1, 0):
            self.dir = (-1, 0)

        # gets food
        hits = pygame.sprite.groupcollide(
            self.game.parts, self.game.foods, False, True)
        if hits:
            for hit in hits:
                self.grow()
                Food(self.game)

    def grow(self):
        self.body.append(Part(self.game, self.x, self.y))
        self.size = len(self.body)
