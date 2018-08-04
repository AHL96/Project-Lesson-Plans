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


class Snake:
    def __init__(self, game, x, y, dir=(1, 0)):
        self.body = [Cell(game, 'part', i*PARTSIZE+x, y) for i in range(1)]
        self.size = len(self.body)

        self.game = game

        self.dir = dir
        self.x = x
        self.y = y

        self.alive = True

    def update(self):

        # movement
        # print(self.dir)
        self.x += self.dir[0] * PARTSIZE
        self.y += self.dir[1] * PARTSIZE

        if self.x < 0:
            self.x = WIDTH - PARTSIZE
        if self.x > WIDTH - PARTSIZE:
            self.x = 0

        if self.y < 0:
            self.y = HEIGHT - PARTSIZE
        if self.y > HEIGHT - PARTSIZE:
            self.y = 0

        part = self.body.pop(0)
        part.kill()
        self.body.append(Cell(self.game, 'part', self.x, self.y))

        head = self.body[-1]
        self.game.cells.remove(self.body[-1])
        hits = pygame.sprite.spritecollide(head, self.game.cells, False)
        if hits:
            for hit in hits:
                if hit.type == 'food':
                    hit.kill()
                    self.body.append(Cell(self.game, 'part', self.x, self.y))
                    Cell(self.game, 'food',
                         randint(0, WIDTH//PARTSIZE) * PARTSIZE,
                         randint(0, HEIGHT//PARTSIZE) * PARTSIZE
                         )
                if hit.type == 'part':
                    self.alive = False
                    # print('dead')
                    for part in self.body:
                        part.kill()
                    self.__init__(self.game, self.x, self.y, self.dir)

        self.game.cells.add(head)

    def grow(self):
        self.body.append(Cell(self.game, 'part', self.x, self.y))
        self.size = len(self.body)

    def direction(self, x, y):
         # player controls
        if y == 1 and self.dir != (0, 1):
            self.dir = (0, -1)
        if x == -1 and self.dir != (-1, 0):
            self.dir = (1, 0)
        if y == -1 and self.dir != (0, -1):
            self.dir = (0, 1)
        if x == 1 and self.dir != (1, 0):
            self.dir = (-1, 0)
