import json


import pygame as pg
import pytmx


pg.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1020
FPS = 80
TILE_SCALE = 2
font = pg.font.Font(None, 36)

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
        self.gravity = 1

        self.is_jumping = False

        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE

        self.timer = pg.time.get_ticks()
        self.interval = 200

        self.hp = 10
        self.damage_timer = pg.time.get_ticks()
        self.damage_interval = 1000
        self.hitbox = pg.Rect(self.rect.x, self.rect.y, 16 * TILE_SCALE, 16 * TILE_SCALE * 1.5 + 8 )

    def load_animations(self):
        tile_size = 32
        tile_scale = TILE_SCALE * 3.5

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
        self.velocity_y = -17
        self.is_jumping = True
    def update(self, platforms):
        keys = pg.key.get_pressed()
        # if keys[pg.K_SPACE]and not self.is_jumping:
        if keys[pg.K_SPACE]:
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
        new_x = self.hitbox.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.hitbox.width:
            self.hitbox.x = new_x
        self.velocity_y += self.gravity
        self.hitbox.y += self.velocity_y


        for platform in platforms:
            if platform.rect.collidepoint(self.hitbox.midbottom):
                self.hitbox.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False
                # print(platform)
            if platform.rect.collidepoint(self.hitbox.midtop):
                self.hitbox.top = platform.rect.bottom
                self.velocity_y = 0
                # print(platform)
            if platform.rect.collidepoint(self.hitbox.midright):
                self.hitbox.right = platform.rect.left
                # print(platform)
            if platform.rect.collidepoint(self.hitbox.midleft):
                self.hitbox.left = platform.rect.right
                # print(platform)

        self.rect.center = (self.hitbox.centerx, self.hitbox.centery + 4)

        
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()
class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        super(Coin, self).__init__()
        self.load_animations()
        self.image = self.images[0]
        self.rect = self.image.get_rect(x=x*TILE_SCALE, y=y*TILE_SCALE)

        self.current_image = 0
        self.interval = 200
        self.timer = pg.time.get_ticks()

    def load_animations(self):
        tile_size = 16
        self.images= []

        num_images = 5
        spriteSheet = pg.image.load("maps/MonedaR.png")

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spriteSheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * TILE_SCALE, tile_size * TILE_SCALE))
            self.images.append(image)

    def update(self):
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.images):
                self.current_image = 0
            self.image = self.images[self.current_image]
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
        self.one_coin = pg.image.load("maps/MonedaR.png")
        rect = pg.Rect(0, 0,  16, 16)
        image = self.one_coin.subsurface(rect)
        self.one_coin = pg.transform.scale(image, (16 * TILE_SCALE, 16 * TILE_SCALE))
        self.tmx_map = pytmx.load_pygame("maps/LVL_2.tmx")
        self.map_pixel_width = self.tmx_map.width * self.tmx_map.tilewidth * TILE_SCALE
        self.map_pixel_height = self.tmx_map.height * self.tmx_map.tileheight * TILE_SCALE
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.player = Player(self.map_pixel_width, self.map_pixel_height)
        self.all_sprites.add(self.player)
        self.collected_coins = 0
        for layer in self.tmx_map:
            if layer.name == "карта":
                for x, y, gid in layer:
                    tile = self.tmx_map.get_tile_image_by_gid(gid)

                    if tile:
                        platform = Platform(tile, x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight,
                                            self.tmx_map.tilewidth,
                                            self.tmx_map.tileheight)
                        self.all_sprites.add(platform)
                        self.platforms.add(platform)
            elif layer.name == "монеты":
                for x, y, gid in layer:
                    tile = self.tmx_map.get_tile_image_by_gid(gid)

                    if tile:
                        coin = Coin( x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight)
                        self.all_sprites.add(coin)
                        self.coins.add(coin)
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
        self.coins.update()
        for coin in self.coins:
            if coin.rect.colliderect(self.player.hitbox):
                self.collected_coins += 1
                coin.kill()

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
        # pg.draw.rect(self.screen, "red", self.player.hitbox, 3)
        self.count_attribute_draw()
        pg.display.flip()
    def count_attribute_draw(self):
        self.screen.blit(self.one_coin, [10,10])
        text = font.render(str(self.collected_coins), True, (255, 255, 255))
        text_rect = text.get_rect(x=40, y=15)
        self.screen.blit(text, text_rect)

if __name__ == "__main__":
    game = Game()