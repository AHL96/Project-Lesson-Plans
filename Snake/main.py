
import pygame
from random import random
from sprites import *
from settings import *


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.running = True

        self.clock = pygame.time.Clock()

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.cells = pygame.sprite.Group()

        self.snake1 = Snake(self, 0, 0)
        #    randint(0, WIDTH//PARTSIZE) * PARTSIZE,
        #    randint(0, HEIGHT//PARTSIZE) * PARTSIZE
        #    )
        self.snake2 = Snake(self, WIDTH-PARTSIZE, HEIGHT-PARTSIZE)

        for i in range(100):
            # Food(self)
            Cell(self, 'food',
                 randint(0, WIDTH//PARTSIZE) * PARTSIZE,
                 randint(0, HEIGHT//PARTSIZE) * PARTSIZE
                 )

        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False

                # snake1 controls
                if event.key == pygame.K_UP:
                    self.snake1.direction(0, 1)
                if event.key == pygame.K_RIGHT:
                    self.snake1.direction(-1, 0)
                if event.key == pygame.K_DOWN:
                    self.snake1.direction(0, -1)
                if event.key == pygame.K_LEFT:
                    self.snake1.direction(1, 0)

                # snake2 controls
                if event.key == pygame.K_w:
                    self.snake2.direction(0, 1)
                if event.key == pygame.K_d:
                    self.snake2.direction(-1, 0)
                if event.key == pygame.K_s:
                    self.snake2.direction(0, -1)
                if event.key == pygame.K_a:
                    self.snake2.direction(1, 0)

    def update(self):
        self.all_sprites.update()
        self.snake1.update()
        self.snake2.update()

    def draw(self):
        self.screen.fill(BACKGROUND)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(str(len(self.snake1.body)), 16, WHITE,
                       self.snake1.x+PARTSIZE/2, self.snake1.y+PARTSIZE/2)
        self.draw_text(str(len(self.snake2.body)), 16, WHITE,
                       self.snake2.x+PARTSIZE/2, self.snake2.y+PARTSIZE/2)
        pygame.display.flip()

    def draw_grid(self):
        for x in range(0, WIDTH, PARTSIZE):
            pygame.draw.line(self.screen, BLACK, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, PARTSIZE):
                pygame.draw.line(self.screen, BLACK, (0, y), (WIDTH, y))

    def draw_text(self, text, size, color, x, y):
        font_name = pygame.font.get_default_font()
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
while g.running:
    g.new()

pygame.quit()
