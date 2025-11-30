import json


import pygame as pg


pg.init()
pg.mixer.init()
from constanta import *
from load_layer import load_layer
from player import Player
from enemy import Orc

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("игра")

        self.setup()

    # noinspection PyAttributeOutsideInit
    def setup(self):
        self.mode = "game"
        self.clock = pg.time.Clock()
        self.is_running = False
        self.level = 2
        self.background_1 = pg.image.load("./maps/free-swamp-game-tileset-pixel-art (1)/2 Background/Layers/2.png")
        self.background_1 = pg.transform.scale(self.background_1, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_2 = pg.image.load("./maps/free-swamp-game-tileset-pixel-art (1)/2 Background/Layers/5.png")
        self.background_2 = pg.transform.scale(self.background_2, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.one_coin = pg.image.load("maps/MonedaR.png")
        self.heart = pg.image.load("sprites/heart.png")
        self.heart = pg.transform.scale(self.heart, (22*TILE_SCALE, 22*TILE_SCALE))
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
        self.player = Player(self.map_pixel_width, self.map_pixel_height, self.arrows, self.all_sprites)
        self.all_sprites.add(self.player)

        self.collected_coins = 0

        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 2
        self.load_enemy()
        self.load_sounds()
        self.run()

    def load_sounds(self):
        self.sound_death = pg.mixer.Sound("sounds/classic-hurt.wav")
        self.sound_death.set_volume(0.2)
        # self.back_music = pg.mixer.Sound("sounds/")
        # self.back_music.set_volume(0.3)
        # self.back_music.play(-1)
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
        if self.player.hp <= 0:
            self.mode = "game over"
            return
        if not self.coins and not self.enemies and self.player.hp > 0:
             self.mode = "win"
             return

        for enemy in self.enemies.sprites():
            if pg.sprite.collide_mask(self.player, enemy):
                self.player.get_damage()
        self.player.update(self.platforms)
        self.coins.update()
        self.arrows.update()
        for coin in self.coins:
            if coin.rect.colliderect(self.player.hitbox):
                self.collected_coins += 1
                coin.kill()
        hit = pg.sprite.groupcollide(self.arrows, self.enemies, True, True)
        pg.sprite.groupcollide(self.arrows, self.platforms, True, False)
        for enemy in self.enemies.sprites():
            enemy.update(self.platforms)
        if hit:
            self.sound_death.play()
        self.camera_x = self.player.rect.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.rect.y - SCREEN_HEIGHT // 2
        self.camera_x = max(0, min(self.camera_x, self.map_pixel_width - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.map_pixel_height - SCREEN_HEIGHT))

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False


    def draw(self):
        if self.mode == "game":
            self.screen.fill("white")
            self.screen.blit(self.background_1, (0, 0))
            self.screen.blit(self.background_2, (0, 0))
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, sprite.rect.move(-self.camera_x, -self.camera_y))
            self.player.hitbox[0] -= self.camera_x
            self.player.hitbox[1] -= self.camera_y
            # pg.draw.rect(self.screen, "red", self.player.hitbox, 3)
            self.count_attribute_draw()
        elif self.mode == "game over":
            text = font.render("You Lose", True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            # self.back_music.fadeout(2000)
        elif self.mode == "win":
            text = font.render("You WiN!!!", True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            # self.back_music.fadeout(2000)
        pg.display.flip()
    def count_attribute_draw(self):
        self.screen.blit(self.one_coin, [10,50])
        text = font.render(str(self.collected_coins), True, (255, 255, 255))
        text_rect = text.get_rect(x=40, y=55)
        self.screen.blit(text, text_rect)
        for i in range(self.player.hp):
            x = (16 * TILE_SCALE  + 15 * TILE_SCALE * i) - 30
            y = 16 * TILE_SCALE - 20
            self.screen.blit(self.heart, [x, y])



if __name__ == "__main__":
    game = Game()