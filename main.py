import json


import pygame as pg


pg.init()
from constanta import *
from load_layer import load_layer
from player import Player
from enemy import Orc

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("игра")
        self.mode = "game"
        self.clock = pg.time.Clock()
        self.is_running = False
        self.level = 2
        self.background_1 = pg.image.load("./maps/free-swamp-game-tileset-pixel-art (1)/2 Background/Layers/2.png")
        self.background_1 = pg.transform.scale(self.background_1, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_2 = pg.image.load("./maps/free-swamp-game-tileset-pixel-art (1)/2 Background/Layers/5.png")
        self.background_2 = pg.transform.scale(self.background_2, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.one_coin = pg.image.load("maps/MonedaR.png")
        rect = pg.Rect(0, 0,  16, 16)
        image = self.one_coin.subsurface(rect)
        self.one_coin = pg.transform.scale(image, (16 * TILE_SCALE, 16 * TILE_SCALE))

        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.arrows = pg.sprite.Group()

        self.tmx_map = load_layer(self.all_sprites, self.platforms, self.coins, self.level)
        self.map_pixel_width = self.tmx_map.width * self.tmx_map.tilewidth * TILE_SCALE
        self.map_pixel_height = self.tmx_map.height * self.tmx_map.tileheight * TILE_SCALE
        self.player = Player(self.map_pixel_width, self.map_pixel_height)
        self.all_sprites.add(self.player)

        self.collected_coins = 0

        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 2
        self.load_enemy()
        self.run()

    def load_enemy(self):
        with open(f"lvl{self.level}_enemies.json", "r") as json_file:
            data = json.load(json_file)
        for enemy in data["enemies"]:
            if enemy["name"] ==  "Orc":
                x1 = enemy["start_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                y1 = enemy["start_pos"][1] * TILE_SCALE * self.tmx_map.tileheight

                x2 = enemy["final_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                y2 = enemy["final_pos"][1] * TILE_SCALE * self.tmx_map.tileheight
                orc = Orc(self.map_pixel_width, self.map_pixel_height, [x1, y1], [x2, y2])
                self.all_sprites.add(orc)
                self.enemies.add(orc)

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
        self.enemies.update(self.platforms)

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