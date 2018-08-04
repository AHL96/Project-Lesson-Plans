import pygame
from settings import *
from random import randint, choice


class Cell(pygame.sprite.Sprite):
    def __init__(self, game, t, x, y):
        self.groups = game.all_sprites, game.cells
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.type = t

        self.image = pygame.Surface((PARTSIZE-1, PARTSIZE-1))
        self.image.fill(cell[self.type]['color'])

        self.rect = self.image.get_rect()
        self.rect.x = x+1
        self.rect.y = y+1

        self.game = game

        if self.type == 'food':
            self.game.foods.add(self)
        elif self.type == 'part':
            self.game.parts.add(self)


class Snake:
    def __init__(self, game, x, y):
        self.body = [Cell(game, 'part', PARTSIZE+x, y)]
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
        self.body.append(Cell(self.game, 'part', self.x, self.y))

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

        head = self.body[-1]
        self.game.cells.remove(self.body[-1])
        hits = pygame.sprite.spritecollide(head, self.game.cells, False)
        if hits:
            for hit in hits:
                if hit.type == 'food':
                    hit.kill()
                    self.body.append(Cell(self.game, 'part', self.x, self.y))
                if hit.type == 'part':
                    self.alive = False

        self.game.cells.add(head)

    def grow(self):
        self.body.append(Cell(self.game, 'part', self.x, self.y))
        self.size = len(self.body)
