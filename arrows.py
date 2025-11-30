from constanta import *
import pygame as pg


class Arrow(pg.sprite.Sprite):
    def __init__(self, player_rect, direction):
        super(Arrow, self).__init__()

        self.direction = direction
        self.speed = 3

        self.image = pg.image.load("sprites/New Piskel.png")
        self.image = pg.transform.scale(self.image, (18 * TILE_SCALE, 18 * TILE_SCALE))
        if self.direction == "left":
            self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()

        self.rect.x = player_rect.right if direction == "right" else player_rect.left
        self.rect.y = player_rect.centery - 14
        # self.rect.center = player_rect.center


    def update(self):
        self.rect.x += self.speed if self.direction == "right" else -self.speed
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH:
            self.kill()