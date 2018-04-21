import pygame
import random
from os import path

# set up assets folders
game_dir = path.dirname(__file__)
img_dir = path.join(game_dir, "img")
sound_dir = path.join(game_dir, "snd")

WIDTH = 480
HEIGHT = 600
FPS = 60
POWER_TIME = 5000  # in milliseconds

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

font_name = pygame.font.get_default_font()
# font_name = pygame.font.match_font('arial')
# print(font_name)


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def new_meteor():
    m = Meteor()
    all_sprites.add(m)
    meteors.add(m)


def draw_shield_bar(surface, x, y, precent):
    if precent < 0:
        precent = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (precent / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)


def draw_lives(surface, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surface.blit(img, img_rect)


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Space Shooter", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow Keys move, Space to fire",
              22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to start", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        # self.image = pygame.Surface((50, 40))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hidden_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.ammo = 100

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # timeout for power-ups inheritance
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWER_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hidden_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -6
        if keystate[pygame.K_RIGHT]:
            self.speedx = 6
        self.rect.x += self.speedx

        if keystate[pygame.K_SPACE]:
            self.shoot()

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        # print(self.ammo)
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay and self.ammo > 0:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
                self.ammo -= 1
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
                self.ammo -= 2

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        # self.image = pygame.Surface((30, 40))
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -48)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.kill()
            new_meteor = Meteor()
            all_sprites.add(new_meteor)
            meteors.add(new_meteor)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_img
        # self.image = pygame.Surface((10, 20))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill it if it moves off the screen
        if self.rect.bottom < 0:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun', 'ammo'])
        self.image = powerup_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # kill it if it moves off the screen
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect.center = center


# load all game graphics
background = pygame.image.load(
    path.join(img_dir, "black.png")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
laser_img = pygame.image.load(path.join(img_dir, "laserGreen.png")).convert()
meteor_images = []
meteor_list = [
    "meteorBrown_big1.png", "meteorBrown_big2.png",
    "meteorBrown_big3.png", "meteorBrown_big4.png",
    "meteorBrown_med1.png", "meteorBrown_med3.png",
    "meteorBrown_small1.png", "meteorBrown_small2.png",
    "meteorBrown_tiny1.png", "meteorBrown_tiny2.png",
    "meteorGrey_big1.png", "meteorGrey_big2.png",
    "meteorGrey_big3.png", "meteorGrey_big4.png",
    "meteorGrey_med1.png", "meteorGrey_med2.png",
    "meteorGrey_small1.png", "meteorGrey_small2.png",
    "meteorGrey_tiny1.png", "meteorGrey_tiny2.png"
]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(8):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename))
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
powerup_imgs = {}
powerup_imgs['shield'] = pygame.image.load(
    path.join(img_dir, 'powerupGreen_shield.png')).convert()
powerup_imgs['gun'] = pygame.image.load(
    path.join(img_dir, 'powerupGreen_bolt.png')).convert()
# powerup_imgs['ammo'] = pygame.Surface((30, 30))
# powerup_imgs['ammo'].fill(GREEN)
powerup_imgs['ammo'] = pygame.image.load(
    path.join(img_dir, 'powerupGreen_star.png')).convert()

# load game sounds
shoot_sound = pygame.mixer.Sound(path.join(sound_dir, 'laser.wav'))
explosion_sound = pygame.mixer.Sound(path.join(sound_dir, 'explosion.wav'))
pygame.mixer.music.load(path.join(sound_dir, 'background.mp3'))
# pygame.mixer.music.set_volume(0.4)
shoot_sound.set_volume(0.3)
explosion_sound.set_volume(0.3)

all_sprites = pygame.sprite.Group()
meteors = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(10):
    new_meteor()

score = 0
pygame.mixer.music.play(loops=-1)

# Game loop
game_over = True
running = True
while running:

    if game_over:
        show_go_screen()
        game_over = False

        all_sprites = pygame.sprite.Group()
        meteors = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(10):
            new_meteor()

        score = 0

    clock.tick(FPS)
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         player.shoot()

    # update
    all_sprites.update()

    # check to see if a bullet hit a Meteor
    hits = pygame.sprite.groupcollide(meteors, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        explosion_sound.play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = PowerUp(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        new_meteor()

    # check to see if a player collided with a Meteor
    hits = pygame.sprite.spritecollide(
        player, meteors, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        new_meteor()
        if player.shield <= 0:
            explosion_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            # player.kill()
            player.hide()
            player.lives -= 1
            player.shield = 100
            player.ammo = 100

    # check to see if a player hit a power-up
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += 20
            if player.shield > 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()

        # ammo power-up
        if hit.type == 'ammo':
            player.ammo += 50

    if player.lives == 0 and not death_explosion.alive():
        # running = False
        game_over = True

    # draw and render
    # screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_text(screen, "AMMO: " + str(player.ammo), 18, 60, HEIGHT * .95)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    pygame.display.flip()

pygame.quit()
