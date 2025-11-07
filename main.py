import json


import pygame as pg
import pytmx
import os

pg.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1020
FPS = 80
TILE_SCALE = 1.5
win = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Platform (pg.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super(Platform, self).__init__()

        self.image = pg.transform.scale(image, (width * TILE_SCALE, height * TILE_SCALE))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE
class Player(pg.sprite.Sprite):
    def __init__(self, map_width, map_height):
        super(Player, self).__init__()

        self.load_animations()

        self.current_animation = self.idle_animations_right
        self.image = self.current_animation[0]
        self.current_image = 0

        self.rect = self.image.get_rect()
        self.rect.center = (300, 200)  # Начальное положение персонажа

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 0.01

        self.is_jumping = False

        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE

        self.timer = pg.time.get_ticks()
        self.interval = 200

        self.hp = 10
        self.damage_timer = pg.time.get_ticks()
        self.damage_interval = 1000
        self.hitbox = [self.rect.x, self.rect.y, 18 * 3, 18 * 5 ]

    def load_animations(self):
        tile_size = 32
        tile_scale = 9

        self.idle_animations_right = []
        num_images = 4
        for i in range(1, num_images + 1):
            image = pg.image.load(f"sprites/idle_Hobbit/Hobbit - Idle{i}.png")
            image = pg.transform.scale(image, (tile_size * tile_scale,tile_size * tile_scale))
            self.idle_animations_right.append(image)
        self.idle_animations_left = [pg.transform.flip(image, True, False) for image in self.idle_animations_right]

        self.move_animations_right = []

        num_images = 10
        for i in range(1, num_images + 1):
            image = pg.image.load(f"sprites/move_Hobbit/Hobbit - run{i}.png")
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            self.move_animations_right.append(image)

        self.move_animations_left = [pg.transform.flip(image, True, False) for image in self.move_animations_right]
    def jump(self):
        self.velocity_y = -12
        self.is_jumping = True
    def update(self, platforms):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and not self.is_jumping:
            self.jump()
        if keys[pg.K_a]:
            if self.current_animation != self.move_animations_left:
                self.current_animation = self.move_animations_left
                self.current_image = 0
            self.velocity_x = -5
        elif keys[pg.K_d]:
            if self.current_animation != self.move_animations_right:
                self.current_animation = self.move_animations_right
                self.current_image = 0

            self.velocity_x = 5
        else:
            if self.current_animation == self.move_animations_right:
                self.current_animation = self.idle_animations_right
                self.current_image = 0
            elif self.current_animation == self.move_animations_left:
                self.current_animation = self.move_animations_left
                self.current_image = 0
            self.velocity_x = 0
        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x
        self.velocity_y += self.gravity


        for platform in platforms:
            if platform.rect.collidepoint((self.hitbox[0] + self.hitbox[2] // 2, self.hitbox[1] + self.hitbox[3])  ):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False
            if platform.rect.collidepoint((self.hitbox[0] + self.hitbox[2] // 2, self.hitbox[1] )):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0
            if platform.rect.collidepoint((self.hitbox[0] + self.hitbox[2], self.hitbox[1] + self.hitbox[3] // 2 )):
                self.rect.right = platform.rect.left
            if platform.rect.collidepoint((self.hitbox[0], self.hitbox[1] + self.hitbox[3] // 2 )):
                self.rect.left = platform.rect.right
        self.rect.y += self.velocity_y
        self.hitbox[0] = self.rect.centerx - self.hitbox[2] // 2
        self.hitbox[1] = self.rect.centery - self.hitbox[3] // 2
        
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()
class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("игра")
        self.mode = "game"
        self.clock = pg.time.Clock()
        self.is_running = False
        self.background_1 = pg.image.load("./maps/free-swamp-game-tileset-pixel-art (1)/2 Background/Layers/2.png")
        self.background_1 = pg.transform.scale(self.background_1, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_2 = pg.image.load("./maps/free-swamp-game-tileset-pixel-art (1)/2 Background/Layers/5.png")
        self.background_2 = pg.transform.scale(self.background_2, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.tmx_map = pytmx.load_pygame("maps/LVL_1.tmx")
        self.map_pixel_width = self.tmx_map.width * self.tmx_map.tilewidth * TILE_SCALE
        self.map_pixel_height = self.tmx_map.height * self.tmx_map.tileheight * TILE_SCALE
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self.map_pixel_width, self.map_pixel_height)
        self.all_sprites.add(self.player)
        for layer in self.tmx_map:
            if layer.name == "болото":
                for x, y, gid in layer:
                    tile = self.tmx_map.get_tile_image_by_gid(gid)

                    if tile:
                        platform = Platform(tile, x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight,
                                            self.tmx_map.tilewidth,
                                            self.tmx_map.tileheight)
                        self.all_sprites.add(platform)
                        self.platforms.add(platform)
        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 2
        self.run()
    def run(self):
        self.is_running = True
        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pg.quit()
        quit()
    def update(self):
        self.player.update(self.platforms)

        self.camera_x = self.player.rect.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.rect.y - SCREEN_HEIGHT // 2

        self.camera_x = max(0, min(self.camera_x, self.map_pixel_width - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.map_pixel_height - SCREEN_HEIGHT))

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

    def draw(self):
        self.screen.fill("white")
        self.screen.blit(self.background_1, (0, 0))
        self.screen.blit(self.background_2, (0, 0))


        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.move(-self.camera_x, -self.camera_y))
        self.player.hitbox[0] -= self.camera_x
        self.player.hitbox[1] -= self.camera_y
        pg.draw.rect(win, "red", self.player.hitbox, 3)
        pg.display.flip()
if __name__ == "__main__":
    game = Game()