
import pygame
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
        self.parts = pygame.sprite.Group()
        self.foods = pygame.sprite.Group()
        self.cells = pygame.sprite.Group()

        self.snake = Snake(self, WIDTH//2, HEIGHT//2)

        for i in range(25):
            # Food(self)
            Cell(self, 'food',
                 randint(0, WIDTH//PARTSIZE) * PARTSIZE,
                 randint(0, HEIGHT//PARTSIZE) * PARTSIZE
                 )

        self.run()

    def run(self):
        self.playing = True
        while self.playing and self.snake.alive:
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

    def update(self):
        self.all_sprites.update()
        self.snake.update()

    def draw(self):
        self.screen.fill(BACKGROUND)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def draw_grid(self):
        pass


g = Game()
while g.running:
    g.new()

pygame.quit()
