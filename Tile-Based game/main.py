import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *


def draw_player_health(surface, x, y, precent):
    '''heads up display (hud)'''
    if precent < 0:
        precent = 0

    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = precent * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)

    if precent > 0.6:
        col = GREEN
    elif precent > 0.3:
        col = YELLOW
    else:
        col = RED

    pg.draw.rect(surface, col, fill_rect)
    pg.draw.rect(surface, WHITE, outline_rect, 2)


class Game:

    def __init__(self):
        pg.mixer.pre_init(44100,-16,1,2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        # set folder paths
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'sounds')
        effect_folder = path.join(snd_folder, 'snd')
        music_folder = path.join(snd_folder, 'music')
        map_folder = path.join(game_folder, 'maps')

        # get font
        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        # get map
        self.map = TiledMap(path.join(map_folder, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        self.player_img = pg.image.load(
            path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(
            path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(
            self.bullet_images['lg'], (10, 10))
        self.mob_img = pg.image.load(
            path.join(img_folder, MOB_IMG)).convert_alpha()
        self.splat = pg.image.load(
            path.join(img_folder, SPLAT)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (TILESIZE, TILESIZE))

        # load gun flashes
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(
                path.join(img_folder, img)).convert_alpha())

        # load background music
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))

        # load sound effects
        self.effect_sounds = {}
        for effect in EFFECTS_SOUNDS:
            self.effect_sounds[effect] = pg.mixer.Sound(
                path.join(effect_folder, EFFECTS_SOUNDS[effect]))

        # load weapon sounds
        self.weapon_sounds = {}
        # self.weapon_sounds['gun'] = []
        # for snd in WEAPON_SOUNDS_GUN:
        #     self.weapon_sounds['gun'].append(
        #         pg.mixer.Sound(path.join(effect_folder, snd)))
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(effect_folder, snd))
                s.set_volume(0.3)
                self.weapon_sounds[weapon].append(s)

        # load zombie sounds
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(effect_folder, snd))
            s.set_volume(0.1)
            self.zombie_moan_sounds.append(s)

        # load player hit sounds
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(effect_folder, snd))
            # s.set_volume(0.1)
            self.player_hit_sounds.append(s)

        # load zombie hit sounds
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(effect_folder, snd))
            # s.set_volume(0.1)
            self.zombie_hit_sounds.append(s)

    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Tile(self, tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height)
            if tile_object.name in ['health']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.effect_sounds['level_start'].play()

    def run(self):
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        # player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effect_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
        # mobs hit player
        hits = pg.sprite.spritecollide(
            self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            random.choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            # hit.health -= BULLET_DAMAGE
            hit.health -= WEAPONS[self.player.weapon]['damage'] * \
                len(hits[hit])
            hit.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption('{:.2f}'.format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        # self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:

            if isinstance(sprite, Mob):
                sprite.draw_health()

            self.screen.blit(sprite.image, self.camera.apply(sprite))

            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN,
                             self.camera.apply_rect(sprite.hit_rect), 1)

        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN,
                             self.camera.apply_rect(wall.rect), 1)
        # pg.draw.rect(self.screen, WHITE, self.camera.apply(self.player), 2)
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # for b in self.bullets:
            # pg.draw.rect(self.screen, WHITE, self.camera.apply(b), 2)

        draw_player_health(self.screen, 10, 10,
                           self.player.health / PLAYER_HEALTH)

        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED,
                           WIDTH/2, HEIGHT/2, align='center')
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    def draw_text(self, text, font_name, size, color, x, y, align='nw'):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()

pg.quit()
